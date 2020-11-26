from multiprocessing import Process, Value
from gui import startgui
from server import start_server

if __name__ == '__main__':
    print("running local crypto server...")
    serverp = Process(target=start_server)
    serverp.start()
    print("running gui...")
    guip = Process(target=startgui)
    guip.start()
    guip.join()
    print("terminating local crypto server...")
    serverp.terminate()
    serverp.join()
    print("wrapper terminated. bye!")
