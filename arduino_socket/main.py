import time

from .socket import Socket

def evens_worker():
    value = 0

    while True:
        yield {'worker': 'evens', 'value': 2 * value}
        value += 1
        time.sleep(0.1)

def odds_worker():
    value = 0

    while True:
        yield {'worker': 'odds', 'value': 2 * value + 1}
        value += 1
        time.sleep(0.1)

socket = Socket(__name__)
socket.add_worker(evens_worker())
socket.add_worker(odds_worker())
socket.start_workers()
app = socket.get_app()

if __name__ == '__main__':
    socket.start_server()
