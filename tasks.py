from engine import app
from celery import group, chord

@app.task(name="simple1")
def simple1():
    print("Simple 1")
    return {'status' : 1}

@app.task(name="simple2")
def simple2():
    print("Simple 2")
    return {'status' : 2}

@app.task(name="simple3")
def simple3():
    print("Simple 3")
    return {'status' : 3}

@app.task(name="callback", max_retries=10)
def callback(results):
    print("Callback {}".format(results))
    return {'status' : results}

@app.task(name="noop", max_retries=10)
def noop(results):
    return results



def simple_chain():
    return simple1.si() | simple2.si() | simple3.si()

def simple_chord():
    return chord([simple1.si(), simple2.si(), simple3.si()])

def simple_chord_with_callback():
    return chord([simple1.si(), simple2.si(), simple3.si()], callback.s())

def chord_of_chords():
    return chord([
        simple_chord_with_callback(),
        simple_chord_with_callback()
    ], callback.s())

def chord_of_chords_with_each_chord_followed_by_a_serial_task():
    return chord([
        chord([simple_chord_with_callback()] , noop.s()),
        chord([simple_chord_with_callback()] , noop.s())
    ], callback.s())

def chord_followed_by_a_serial_task():
    return simple_chord_with_callback() | callback.s()
`   

