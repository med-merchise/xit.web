"""Flasker configuration tools."""

from xit.web.dasher import Dash


def create_app(name: str = None, **kwargs: object) -> Dash:
    """Create and configure a Dash application.

    This function receives the same arguments as the `Dash`:class:
    constructor.  The arguments to allow multiple pages change its default
    values: 'pages_folder' is set to an empty string and 'use_pages' to True.
    This will allow the use of our new pages (those registered with the
    `xit.web.dasher.pages.register_page`:func: decorator) to be always
    enabled.

    All arguments, but 'name', must be given using keyword parameters.

    """
    if name is not None:
        kwargs['name'] = name
    if 'pages_folder' not in kwargs and 'use_pages' not in kwargs:
        kwargs['use_pages'] = True
        kwargs['pages_folder'] = ''
    return Dash(**kwargs)
