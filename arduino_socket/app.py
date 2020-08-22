from threading import Semaphore, Thread
from typing import Any, Callable, Iterator, List, Optional 
from queue import Queue

import json
import time

from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi, Greenlet
from geventwebsocket.handler import WebSocket, WebSocketHandler

import gevent

from . import settings

Worker = Iterator

class App:
    def __init__(self, name :str):
        self.app = Flask(name)
        self.app.config['SECRET_KEY'] = settings.SECRET_KEY
        self.sockets = Sockets(self.app)
        self.workers :List[Worker] = []
        self.worker_pool :List[Greenlet] = []
        self.queue :Queue[dict] = Queue()
        self.exiting = False
        self._load_routes(self.sockets)

    def run(self, host :str = 'localhost', port :int = 5000):
        try:
            self._run_workers()
            server = pywsgi.WSGIServer((host, port), self.app, handler_class=WebSocketHandler)
            server.serve_forever()
        finally:
            self.exiting = True
            gevent.joinall(self.worker_pool)

    def add_worker(self, worker :Worker):
        self.workers.append(worker)

        return self

    def _load_routes(self, sockets: Sockets):
        @sockets.route('/')
        def on_connect(web_socket: WebSocket):
            print(f'Connected to socket: f{web_socket}')
            while not web_socket.closed:
                if self.queue.empty():
                    time.sleep(1)
                    continue
                
                data = self.queue.get()
                web_socket.send(json.dumps(data))

    def _run_workers(self):
        def run_worker(worker :Worker):
            while not self.exiting:
                data = next(worker)
                self.queue.put(data)

        print(f'Starting workers: {self.workers}...')
        self.worker_threads = [gevent.spawn(run_worker, worker) for worker in self.workers]
            

if __name__ == '__main__':
    App(__name__).add_worker(iter([{'message': 'Hello, world!'}])).run()
