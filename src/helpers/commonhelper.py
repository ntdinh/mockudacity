from datetime import datetime
import pytz
import uuid

from src.types import InternalError
from src.types.errorcode import *


class CommonHelper:
    __instance = None

    def __init__(self):
        if CommonHelper.__instance is not None:
            raise InternalError(ERROR_COMMON_0001)

        CommonHelper.__instance = self

    @staticmethod
    def instance():
        """ Static access method. """
        if CommonHelper.__instance is None:
            CommonHelper()
        return CommonHelper.__instance

    def genUID(self, length=12):
        return str(uuid.uuid4().hex[-length:])

    def nowString(self, tz='Asia/Ho_Chi_Minh', fmt='%Y/%m/%d %H:%M:%S'):
        return datetime.now(pytz.timezone(tz)).strftime(fmt)
