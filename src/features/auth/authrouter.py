from flask import Blueprint

from src.interceptors import loggedRequired

from .authcontroller import AuthController


feature = Blueprint('Auth', __name__)

authController = AuthController()


@feature.route('/api/request_sign_up', methods=['POST'])
def requestSignUp():
    return authController.requestSignUp()


@feature.route('/api/active_account/<token>')
def activeAccount(token: str):
    return authController.activeAccount(token)


@feature.route('/api/sign_in', methods=['POST'])
def signIn():
    return authController.signIn()


@feature.route('/api/request_reset_passwd', methods=['POST'])
def requestResetPasswd():
    return authController.requestResetPasswd()


@feature.route('/api/reset_passwd/<token>')
def resetPasswd(token: str):
    return authController.resetPasswd(token)


@feature.route('/api/change_passwd', methods=['POST'])
def changePasswd():
    return authController.changePasswd()


@feature.route('/api/verify_jwt')
@loggedRequired
def verifyJWT():
    return authController.verifyJWT()
