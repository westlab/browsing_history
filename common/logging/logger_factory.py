import logging.config
from tempfile import TemporaryFile
from pkg_resources import resource_stream, resource_string, resource_filename


class LoggerFactory:
    DEFAULT_LOG_CONFIG = "logging.cfg"

    @staticmethod
    def create_logger(instance):
        if isinstance(instance, str):
            return logging.getLogger(instance)
        else:
            return logging.getLogger("%s.%s" % (instance.__module__, instance.__class__.__name__))

    @staticmethod
    def init(config_file=None):
        if config_file is None:
            config_path = resource_filename(__name__, LoggerFactory.DEFAULT_LOG_CONFIG)
        else:
            config_path = resource_filename(__name__, config_file)

        with open(config_path) as config:
            logging.config.fileConfig(config)
