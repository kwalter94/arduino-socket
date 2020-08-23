from typing import Any, Callable, Iterator, List, Optional 
from queue import Queue

import atexit
import json
import time

from flask import Flask
from flask_sockets import Sockets as FlaskSocket
from gevent import pywsgi, Greenlet
from geventwebsocket.handler import WebSocket, WebSocketHandler

import gevent

from . import settings

Worker = Iterator

class Socket:
    def __init__(self, name :str):
        self.app = Flask(name)
        self.app.config['SECRET_KEY'] = settings.SECRET_KEY
        self.socket = FlaskSocket(self.app)
        self.workers :List[Worker] = []
        self.worker_pool :List[Greenlet] = []
        self.queue :Queue[dict] = Queue()
        self.exiting = False
        self._load_routes(self.socket)

    def start_server(self, host :str = 'localhost', port :int = 5000):
        server = pywsgi.WSGIServer((host, port), self.app, handler_class=WebSocketHandler)
        server.serve_forever()

    def add_worker(self, worker :Worker):
        self.workers.append(worker)

        return self

    def start_workers(self):
        def run_worker(worker :Worker):
            while not self.exiting:
                data = next(worker)
                self.queue.put(data)

        print(f'Starting workers: {self.workers}...')
        self.worker_pool = [gevent.spawn(run_worker, worker) for worker in self.workers]
        atexit.register(self.stop_workers)  # We probably should handle SIGTERM too
 
    def stop_workers(self):
        print(f'Stopping workers: f{self.workers}')
        self.exiting = True
        gevent.joinall(self.worker_pool)

    def get_app(self):
        return self.app

    def _load_routes(self, socket: FlaskSocket):
        @socket.route('/')
        def on_connect(web_socket: WebSocket):
            print(f'Connected to socket: f{web_socket}')
            while not web_socket.closed:
                if self.queue.empty():
                    time.sleep(1)
                    continue
                
                data = self.queue.get()
                web_socket.send(json.dumps(data))

if __name__ == '__main__':
    Socket(__name__).add_worker(iter([{'message': 'Hello, world!'}])).start_server()
