"""Xit interfaces and tools to Plotly Dash.

Dash_ is the original low-code framework for rapidly building data apps in
Python, R, Julia, and F# (experimental).

.. _dash: https://dash.plotly.com/

"""

import sys

try:
    from dash import *  # noqa
except ImportError as error:
    raise ImportError(
        "Dash not found, install 'xit.web' using 'dash' extra.",
        error,
    ).with_traceback(sys.exc_info()[2]) from None
