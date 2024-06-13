import yaml

from .types import *


class GlobalConfig(object):
    __instance = None

    def __init__(self):
        if GlobalConfig.__instance is not None:
            raise InternalError(ERROR_COMMON_0001)

        # Get the configuarion information from yaml file
        cfg = self.__loadConfig('src/config.yaml')
        self.API = cfg['API']
        self.LOG = cfg['LOG']
        self.DB_CONNECTION = cfg['DB_CONNECTION']
        self.JWT_SECRET_KEY = cfg['JWT_SECRET_KEY']
        self.MAIL = cfg['MAIL']
        GlobalConfig.__instance = self

    @staticmethod
    def instance():
        """ Static access method. """
        if GlobalConfig.__instance is None:
            GlobalConfig()
        return GlobalConfig.__instance

    def __loadConfig(self, configPath: str):
        """
        Get the configuration information from yaml file

        Parameters
        ----------
        configPath : str
            Configuration file path (*.yaml)

        Returns
        -------
        : dict
            The configuration information
        """
        with open(configPath, 'r') as f:
            cfg = yaml.load(f, Loader=yaml.SafeLoader)
        return cfg
