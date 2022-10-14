"""Flasker configuration tools."""

from typing import Callable, Mapping

from xit.web.flasker import Flask


FLASK_ARGS = Flask.__init__.__annotations__
SPECIAL_ARGS = {'import_name', 'instance_relative_config'}


def create_app(name: str, *sources: object, **kwargs: object) -> Flask:
    """Create and config the app.

    This function receives the same arguments as the `Flask`:class:
    constructor with two minor differences:

    - ``import_name`` is ignored as ``name`` is used as the first parameter
      here with the same meaning.

    - ``instance_relative_config`` uses ``True`` as default value
      (`Flask`:class: uses ``False`` instead).

    Additionally, you can use:

    :param sources: a collection of sources to configure the application.  All
           uppercase keyword arguments will be also used as an additional
           source.

    """
    import os
    from xit.tools.mappings import pop_items

    flask_args = pop_items(
        kwargs,
        *(arg for arg in FLASK_ARGS if arg not in SPECIAL_ARGS),
        instance_relative_config=True,
    )
    app = Flask(name, **flask_args)
    os.makedirs(app.instance_path, exist_ok=True)  # ensure instance folder
    # TODO: add support for blueprints in sources
    configure_app(app, *(*sources, kwargs), silent=True)
    return app


def import_loader(name: str, silent: bool = False) -> Callable | None:
    """Import a loader function for a given file-name or extension.

    The loader will read from the file and return a dictionary.  This function
    is used internally for `configure_app_from_file`:func: function.

    If `silent` is set to `True` import errors are ignored and `None` is
    returned instead.

    """
    import os
    import sys
    from xit.tools.objects import import_object

    ext = os.path.splitext(name)[-1] if os.path.extsep in name else name
    try:
        return import_object(f'{ext}.load')
    except ImportError as error:
        if silent:
            return None
        else:
            raise ImportError(
                f"'{ext}' loader not found", error
            ).with_traceback(sys.exc_info()[2]) from None


def configure_app(app: Flask, source: object, silent: bool = False) -> bool:
    """Update application configuration values from a given source.

    A configuration source can be of one of the following types:

    - a string - (see `configure_app_from_string`:func: for more information).

    - a mapping - updates the values of all upper-case keys.

    - a tuple, list - use as a collection of configuration sources.

    - a `flask.Blueprint`:class` instance.

    - any other object - load the uppercase attributes of the object,
      `pydantic` models are managed specially.

    """
    from xit.web.flasker import Blueprint

    match source:
        case str(_):
            return configure_app_from_string(app, source, silent=silent)
        case m if isinstance(m, Mapping):
            return configure_app_from_mapping(app, m, silent=silent)
        case bp if isinstance(bp, Blueprint):
            app.register_blueprint(bp)
            return True
        case [*sources]:
            return all(configure_app(app, s, silent=silent) for s in sources)
        case _:
            return configure_app_from_object(app, source, silent=silent)


def configure_app_from_string(
    app: Flask, source: str, silent: bool = False
) -> bool:
    """Configure an application from a given string.

    The value could be: an environment variable name or a prefix for
    environment variables, a file name (see `configure_app_from_file`:func:
    for more information), or an object representation.

    """
    from xit.tools.objects import short_repr as _

    res = (
        configure_app_from_envvar(app, source, silent=True)
        or configure_app_from_file(app, source, silent=True)
        or configure_app_from_object(app, source, silent=True)
    )
    if res or silent:
        return res
    else:
        raise RuntimeError(
            f"Couldn't load any configuration from the string {_(source)}."
        )


def configure_app_from_mapping(
    app: Flask, source: Mapping, silent: bool = False
) -> bool:
    """Configure an application from a given mapping."""
    from xit.tools.objects import short_repr as _

    cfg = app.config
    current = len(cfg)
    cfg.from_mapping(source)
    res = len(cfg) > current
    if res or silent:
        return res
    else:
        raise RuntimeError(
            f"Couldn't load any configuration from mapping {_(source)}."
        )


def configure_app_from_object(
    app: Flask, obj: str | object, silent: bool = False
) -> bool:
    """Configure an application from an object."""
    import sys
    from xit.tools.objects import import_object, short_repr as _
    from xit.tools.mappings import asdict

    try:
        if isinstance(obj, str):
            obj = import_object(obj, silent=False)
        configure_app_from_mapping(
            app, asdict(obj, filter_key=None), silent=False
        )
        return True
    except Exception as error:
        if silent:
            return False
        else:
            raise RuntimeError(
                f"Couldn't load any configuration from object {_(obj)}.",
                error,
            ).with_traceback(sys.exc_info()[2]) from None


def configure_app_from_envvar(
    app: Flask, name: str, silent: bool = False
) -> bool:
    """Configure an application from environment variables.

    The variable value could point to a configuration file; a valid JSON type,
    including dictionaries and lists; an import name for an object
    reference; or loaded as a literal string.

    If a single variable value does not exist, name is used as a prefix: all
    environment variables that start with ``<PREFIX>_`` will be processed,
    dropping the prefix from the configuration key.  An empty string is used
    as synonym of prefix ``'FLASK'``).

    """
    import os
    import json
    from xit.tools.objects import import_object

    cfg = app.config
    if value := os.environ.get(name):
        res = configure_app_from_file(app, value, silent=True)
        if not res:
            try:
                value = json.loads(value)
            except Exception:
                if aux := import_object(value, silent=True):
                    value = aux
                # else:  # the value remains as a string
            cfg[name] = value
            res = True
    else:
        current = len(cfg)
        cfg.from_prefixed_env(name)
        if len(cfg) > current:
            res = True
    if res or silent:
        return res
    else:
        raise RuntimeError(
            f"The variable {name!r} is not set or is not a valid prefix."
        )


def configure_app_from_file(
    app: Flask, name: str, silent: bool = False
) -> bool:
    """Try to configure an application from a file.

    Extensions '.py', '.json', '.toml', and '.yaml' are currently supported.

    When `silent` is set to True, errors are ignored, either because the file
    does not exist or due to an import error getting the loader.

    """
    if name.endswith('.py'):
        return app.config.from_pyfile(name, silent=silent)
    else:
        try:
            loader = import_loader(name, silent=False)
            return app.config.from_file(name, loader, silent=silent)
        except Exception:
            if silent:
                return False
            else:
                raise
