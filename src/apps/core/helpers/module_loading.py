import sys
from importlib import import_module


def _cached_import(module_path: str, class_name: str):
    modules = sys.modules
    module_in_cache = not (
        module_path not in modules
        or (
            # Module is not fully initialized.
            getattr(modules[module_path], "__spec__", None) is not None
            and getattr(modules[module_path].__spec__, "_initializing", False)
            is True
        )
    )

    if module_in_cache:
        return getattr(modules[module_path], class_name)

    import_module(module_path)


def import_string(dotted_path: str):
    """
    Import module by path.

    Import a dotted module path and return the attribute/class designated by
    the last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(
            "{0} doesn't look like a module path".format(dotted_path),
        ) from err

    try:
        return _cached_import(module_path, class_name)
    except AttributeError as attr_err:
        raise ImportError(
            'Module "{0}" does not define a "{1}" attribute/class'.format(
                module_path,
                class_name,
            ),
        ) from attr_err
