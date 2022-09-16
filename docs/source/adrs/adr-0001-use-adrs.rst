.. _adr-0001:

ADR 1: Use Architecture Decision Records (ADRs)
===============================================


Status
------

Accepted


Context
-------

We need to record the architectural decisions made on this project.


Decision
--------

We will use ADRs as described by the `xit <xit-adr-1_>`__ project.

.. _xit-adr-1: https://github.com/med-merchise/xit/blob/main/docs/source/adrs/adr-0001-use-adrs.rst


Consequences
------------

This project will produce its own architectural documents, but also will
"inherit" ADRs from upper level projects.

Foundation and Common Systems:

  - `xit <xit-adrs_>`__
  - `xit.books <xit-books-adrs_>`__

Data Science and Data Analysis:

  - `xash <xash-adrs_>`__

.. _xit-adrs: https://github.com/med-merchise/xit/tree/main/docs/source/adrs
.. _xit-books-adrs: https://github.com/med-merchise/xit.books/tree/main/docs/source/adrs
.. _xash-adrs: https://github.com/med-merchise/xash/tree/main/docs/source/adrs
