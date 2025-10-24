import platform
import inspect
import logging

logger = logging.getLogger(__name__)


def full_platform_info():
    ignored_methods = []
    dic = dict()
    for name in dir(platform):

        obj = getattr(platform, name)

        if not (name.startswith('__') or name.startswith('_')) and callable(obj):

            # Use inspect to check if the object is a named tuple type
            # Named tuples are also classes, so a simple callable() check is not enough

            if inspect.isclass(obj) and issubclass(obj, tuple) and hasattr(obj, '_fields'):
                continue

            if name in ignored_methods:
                continue

            try:
                # print(f"Calling: platform.{name}()")
                result = obj()
                dic[name] = result
            except Exception as e:
                logger.debug(f"Error calling platform.{name}(): {e}\n")

    return dic
