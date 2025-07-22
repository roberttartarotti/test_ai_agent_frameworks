Common Library Documentation
============================

A common library for AI agent frameworks testing that provides a standardized chatbot interface.

Features
--------

* Terminal-based chatbot interface
* Timestamp logging for all messages
* Configurable time intervals between messages
* Importable by other AI agent framework test libraries

Installation
------------

.. code-block:: bash

   pip install -e .

Usage
-----

.. code-block:: python

   from common.chatbot import ChatbotInterface

   chatbot = ChatbotInterface()
   chatbot.start()

API Reference
------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/chatbot

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 