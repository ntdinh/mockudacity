from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.types import InternalError
from src.types.errorcode import *
from src.logger import Logger
from src.globalconfig import GlobalConfig
from src.router import registerRoutes


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# Router register
# registerRoutes(app)

# Setup JWT
app.config['JWT_SECRET_KEY'] = GlobalConfig.instance().JWT_SECRET_KEY
JWTManager(app)


@app.route('/ping')
def ping():
    return 'Pong !!!'


@app.before_request
def before_request_func():
    if request.method != 'OPTIONS':
        Logger.instance() \
            .info(f'[{request.remote_addr}][REQ][{request.method}] {request.path}')


@app.after_request
def after_request_func(response):
    if request.method != 'OPTIONS':
        Logger.instance() \
            .info(f'[{request.remote_addr}][RES][{request.method}] {request.path}')
    return response


@app.errorhandler(InternalError)
def internalExceptionHander(error: InternalError):
    Logger.instance() \
        .error(f'[INTERNAL_ERROR][{error.Code}] {error.Msg}')
    return make_response(
        jsonify({
            'Success': False,
            'Error': {
                'Code': error.Code,
                'Msg': error.Msg
            }
        })
    )


@app.errorhandler(Exception)
def exceptionHander(error: Exception):
    Logger.instance().error(str(error))
    return make_response(
        jsonify({
            'Success': False,
            'Error': {
                'Code': HTTP_ERROR_500,
                'Msg': str(error)
            }
        })
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=GlobalConfig.instance().API['PORT'],
            threaded=True,
            debug=True)
