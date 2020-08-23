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

Usage
=====

Go into arduino_socket/main.py and define a couple of workers (there should
a couple of example workers defined in there). A worker is just a function
that returns an iterator of json objects (anything that
`json.dumps <https://docs.python.org/3/library/json.html#json.dumps>`_ can
handle). Following is an example::

.. code-block:: python
    :linenos:

    import time

    from .socket import Socket

    def odds_worker():
        '''A worker that produces an infinite stream of odd numbers.'''

        x = 0

        while True:
            yield { 'number': 2 * x + 1 }
            x += 1

            time.sleep(1)   # Go to bed for a second

    def evens_worker(max = 1_000_000):
        '''A worker that produces even numbers starting from 0 upto *max*.'''

        return iter(2 * x for i in range(max))
    

    
    socket = Socket(__name__)

    # Notice *odds_worker* is being called before being passed to *add_worker*.
    # *odds_worker* needs to be called so that it outputs an iterator.
    # The worker is the iterator itself not the function that generates it
    # (although we are calling the function a worker).
    socket.add_worker(odds_worker())
    socket.add_worker(evens_worker())

    app = socket.get_app()   # Point gunicorn to this, if serving via gunicorn

    if __name__ == '__main__':
        socket.start_server()   # Use development server


Running
=======

.. code-block:: console

    # If using gunicorn

    $ poetry run gunicorn -k flask_sockets.worker arduino_socket.main:app

    # If using the development server

    $ poetry run python -m arduino_socket.main
