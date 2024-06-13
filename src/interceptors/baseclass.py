from src.logger import Logger


class BaseClass(object):
    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                # Intercept at before calling
                if hasattr(attr, '__self__') and hasattr(attr, '__name__'):
                    className = type(attr.__self__).__name__
                    funcName = attr.__name__
                    Logger.instance() \
                        .info(f'Call {className}.{funcName} function.')

                # Execute function
                result = attr(*args, **kwargs)

                # Intercept at done calling
                if hasattr(attr, '__self__') and hasattr(attr, '__name__'):
                    Logger.instance() \
                        .info(f'End {className}.{funcName} function.')
                return result
            return newfunc
        else:
            return attr
