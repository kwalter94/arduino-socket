import time

from .app import App

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

app = App(__name__)
app.add_worker(evens_worker())
app.add_worker(odds_worker())
app.run()
