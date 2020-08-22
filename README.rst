==============
Arduino Socket
==============

An excuse for writing some Python that started as a scaffold for a websocket
interface for some Arduino project.

Installation
============

.. code-block:: console

    $ pip install poetry
    $ poetry install
    $ echo 'SECRET_KEY=Zakusimba Saulula' > .env

Running
=======

.. code-block:: console

    $ poetry run gunicorn -k flask_sockets.worker arduino_socket.main:app
