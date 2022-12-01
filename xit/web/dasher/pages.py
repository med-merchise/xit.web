"""Xit Plotly Dash web pages."""


from typing import Callable

from xotl.tools.decorator import decorator


def _normalize_title(title: str) -> str:
    """Normalize page title if extracted from function documentation."""
    prefix = 'get '
    if title.lower().startswith(prefix):
        title = title[len(prefix):].capitalize()  # fmt: skip
    if title.endswith('.'):
        title = title[:-1]
    return title


def _infer_path(page: Callable) -> str:
    """Infer the path route when not given."""
    # TODO: see dash._pages._infer_path, & dash._configs.pages_folder_config
    import os
    from dash import get_app

    mod = page.__module__.replace('.', '/')
    pages_folder = get_app().pages_folder.replace(os.sep, '/').strip('/')
    if pages_folder and pages_folder in mod:
        module = mod.split(pages_folder)[-1].strip('/')
    else:
        module = None
    if not module:
        module = mod.split('/')[-1].strip('/')
    return f'/{module}/{ page.__name__}'.replace("_", "-").lower()


@decorator
def register_page(page: Callable, **kwargs: object) -> Callable:
    """Decorate a Dash layout page function.

    Function `dash.register_page`:func: is used internally, some parameters
    can be given explicitly, other are inferred from the page context:

    - module: this parameter is always calculated by joining the module and
      name of page function using a '-' as a separator.

    - layout: the page function.

    - title: if not given explicitly, the first line of the page function
      documentation is used.

    - description: if not given explicitly, the first paragraph of the page
      function documentation is used.

    See `dash.register_page`:func: for more details on parameters.

    """
    from xit.tools import get_paragraphs
    from dash import register_page as _register_page

    module = f'{page.__module__}.{page.__name__}'
    doc_paragraphs = get_paragraphs(page.__doc__ or '')
    if 'path' not in kwargs and 'path_template' not in kwargs:
        kwargs['path'] = _infer_path(page)
    if 'title' not in kwargs and doc_paragraphs:
        kwargs['title'] = doc_paragraphs[0]
    if 'description' not in kwargs and len(doc_paragraphs) > 1:
        kwargs['description'] = doc_paragraphs[1]
    _register_page(module=module, layout=page, **kwargs)
    return page
