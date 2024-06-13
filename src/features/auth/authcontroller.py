from flask import request, jsonify, make_response

from src.interceptors import BaseClass
from src.types.errorcode import *

from .models.dtos import UserDto
from .services import AuthService


class AuthController(BaseClass):
    def __init__(self):
        self.__authService = AuthService()

    def requestSignUp(self):
        obj: dict = request.json
        if 'Username' not in obj:
            raise Exception('Username is required.')
            # raise InternalError() # TODO Implement error object
        if 'Passwd' not in obj:
            raise Exception('Passwd is required.')
            # raise InternalError() # TODO Implement error object
        if 'Email' not in obj:
            raise Exception('Email is required.')
            # raise InternalError() # TODO Implement error object
        if 'Name' not in obj:
            raise Exception('Name is required.')
            # raise InternalError() # TODO Implement error object

        self.__authService.requestSignUp(obj)
        return make_response(
            jsonify({
                'Success': True,
            })
        )

    def activeAccount(self, token: str):
        res: bool = self.__authService.activeAccount(token)
        return 'Account activated successfully. Please return to the homepage to sign in.' if res == True \
            else 'Account activation failed. Please re-register.'

    def signIn(self):
        obj = request.json
        if 'Username' not in obj:
            raise Exception('Username is required.')
            # raise InternalError() # TODO Implement error object
        if 'Passwd' not in obj:
            raise Exception('Passwd is required.')
            # raise InternalError() # TODO Implement error object

        userDto: UserDto = self.__authService.signIn(obj['Username'],
                                                     obj['Passwd'])
        # Cast dto to dict
        user = userDto.toDict()
        return make_response(
            jsonify({
                'Success': True,
                'Payload': user
            })
        )

    def requestResetPasswd(self):
        obj = request.json
        if 'Email' not in obj:
            raise Exception('Email is required.')
            # raise InternalError() # TODO Implement error object

        self.__authService.requestResetPasswd(obj['Email'])
        return make_response(
            jsonify({
                'Success': True,
            })
        )

    def resetPasswd(self, token: str):
        newPasswd: str = self.__authService.resetPasswd(token)
        return f'Your new password is {newPasswd}.' if newPasswd is not None \
            else 'Your password could not be reset. Please try again!'

    def changePasswd(self):
        obj = request.json
        if 'Username' not in obj:
            raise Exception('Username is required.')
            # raise InternalError() # TODO Implement error object
        if 'CurrPasswd' not in obj:
            raise Exception('Current password is required.')
            # raise InternalError() # TODO Implement error object
        if 'NewPasswd' not in obj:
            raise Exception('New password is required.')
            # raise InternalError() # TODO Implement error object

        res: bool = self.__authService.changePasswd(obj['Username'],
                                                    obj['CurrPasswd'],
                                                    obj['NewPasswd'])
        return make_response(
            jsonify({
                'Success': res,
            })
        )

    def verifyJWT(self):
        return make_response(
            jsonify({
                'Success': True
            })
        )
