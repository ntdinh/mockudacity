import datetime
from flask_jwt_extended import create_access_token, decode_token

from src.interceptors import BaseClass
from src.models import DBRepository
from src.types import InternalError
from src.globalconfig import GlobalConfig
from src.mailer import Mailer
from src.helpers import CommonHelper

from ..types.errorcode import *
from ..models.dtos import UserDto
from ..models.entities import UserEntity


class AuthService(BaseClass):
    def __init__(self):
        self.__dbRepo = DBRepository()

    def requestSignUp(self, obj: dict) -> None:
        # Validate user information, throw exception when invalid
        self.__validateSignUp(obj)

        # Send an active link to the user's mail, this link will expire in one day
        token: str = create_access_token(identity=obj,
                                         expires_delta=datetime.timedelta(days=1))
        subject: str = f"[{GlobalConfig.instance().API['NAME']}] Verify your account"
        htmlContent: str = f"""\
            <html>
            <body>
                <p>
                    Hi {obj['Name']},
                    <br>
                    Please click on the link below to activate your account:
                    <br>
                    {GlobalConfig.instance().API['URL']}/api/active_account/{token}
                </p>
            </body>
            </html>
        """
        Mailer.instance().send(receiverEmail=obj['Email'],
                               subject=subject,
                               htmlContent=htmlContent)

    def activeAccount(self, token: str) -> bool:
        decode: dict = decode_token(token)
        obj: dict = decode['sub']

        # Validate user information, throw exception when invalid
        self.__validateSignUp(obj)

        # Put object to the database
        obj['Activate'] = True
        userEntity: UserEntity = self.__dbRepo.put(entityClass=UserEntity,
                                                   obj=obj)
        return userEntity is not None

    def __validateSignUp(self, obj: dict) -> None:
        exists: bool = self.__dbRepo.checkExists(entityClass=UserEntity,
                                                 filterSpec=[{
                                                     'field': 'Username',
                                                     'op': '==',
                                                     'value': obj['Username']
                                                 }])
        if exists == True:
            raise InternalError(ERROR_AUTH_0001)

        exists: bool = self.__dbRepo.checkExists(entityClass=UserEntity,
                                                 filterSpec=[{
                                                     'field': 'Email',
                                                     'op': '==',
                                                     'value': obj['Email']
                                                 }])
        if exists == True:
            raise InternalError(ERROR_AUTH_0002)

    def signIn(self, username: str, passwd: str) -> UserDto:
        userEntity: UserEntity = self.__dbRepo.getOne(entityClass=UserEntity,
                                                      filterSpec=[{
                                                          'field': 'Username',
                                                          'op': '==',
                                                          'value': username
                                                      }])
        if userEntity is None:
            raise InternalError(ERROR_AUTH_0003)
        if userEntity.verifyPasswd(passwd) == False:
            raise InternalError(ERROR_AUTH_0004)
        if userEntity.Activate == False:
            raise InternalError(ERROR_AUTH_0005)

        userDto = UserDto(userEntity)

        # Create an access token from user information
        userDto.Token = create_access_token(identity=userDto.toDict(),
                                            expires_delta=datetime.timedelta(days=1))
        return userDto

    def requestResetPasswd(self, email: str) -> None:
        # Validate user information, throw exception when invalid
        userEntity: UserEntity = self.__validateResetPasswd(email)

        userDto = UserDto(userEntity)

        # Send an active link to the user's mail, this link will expire in 5 minutes
        token: str = create_access_token(identity=userDto.toDict(),
                                         expires_delta=datetime.timedelta(minutes=5))
        subject: str = f"[{GlobalConfig.instance().API['NAME']}] Reset your password"
        htmlContent: str = f"""\
            <html>
            <body>
                <p>
                    Hi {userDto.Name},
                    <br>
                    Please click on the link below to reset your password:
                    <br>
                    {GlobalConfig.instance().API['URL']}/api/reset_passwd/{token}
                </p>
            </body>
            </html>
        """
        Mailer.instance().send(receiverEmail=userDto.Email,
                               subject=subject,
                               htmlContent=htmlContent)

    def resetPasswd(self, token: str) -> str:
        decode: dict = decode_token(token)
        obj: dict = decode['sub']

        # Validate user information, throw exception when invalid
        self.__validateResetPasswd(obj['Email'])

        # Put code and new password to the database
        newPasswd: str = CommonHelper.instance().genUID()
        userEntity: UserEntity = self.__dbRepo.put(entityClass=UserEntity,
                                                   obj={
                                                       'Code': obj['Code'],
                                                       'Passwd': newPasswd
                                                   })
        return newPasswd if userEntity is not None else None

    def changePasswd(self, username: str, currPasswd: str, newPasswd: str) -> bool:
        userEntity: UserEntity = self.__dbRepo.getOne(entityClass=UserEntity,
                                                      filterSpec=[{
                                                          'field': 'Username',
                                                          'op': '==',
                                                          'value': username
                                                      }])
        if userEntity is None:
            raise InternalError(ERROR_AUTH_0003)
        if userEntity.verifyPasswd(currPasswd) == False:
            raise InternalError(ERROR_AUTH_0004)

        # Put code and new password to the database
        userEntity: UserEntity = self.__dbRepo.put(entityClass=UserEntity,
                                                   obj={
                                                       'Code': userEntity.Code,
                                                       'Passwd': newPasswd
                                                   })
        return userEntity is not None

    def __validateResetPasswd(self, email: str) -> UserEntity:
        userEntity: UserEntity = self.__dbRepo.getOne(entityClass=UserEntity,
                                                      filterSpec=[{
                                                          'field': 'Email',
                                                          'op': '==',
                                                          'value': email
                                                      }])
        if userEntity is None:
            raise InternalError(ERROR_AUTH_0006)
        return userEntity
