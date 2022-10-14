"""Xit interfaces and tools to Flask.

Flask_ is just a bridge to Werkzeug_ to implement a proper WSGI_ application
and to Jinja_ to handle templating.

.. _flask: https://flask.palletsprojects.com
.. _werkzeug: https://werkzeug.palletsprojects.com
.. _jinja: https://jinja.palletsprojects.com
.. _wsgi: https://wsgi.readthedocs.io

"""

import sys

try:
    from flask import *  # noqa
except ImportError as error:
    raise ImportError(
        "Flask not found, install 'xit.web' using 'pallets' extra.",
        error,
    ).with_traceback(sys.exc_info()[2]) from None
