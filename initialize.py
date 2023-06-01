import threading

from subprocess import call

def open_py_file():
    call(["python", "main.py"])

def open_py_file1():
    call(["python", "C:/Users/NotAdmin/PycharmProjects/pythonProject/backend/main.py"])


open_py_file() #import error????????????????????

#thread1 = threading.Thread(target=open_py_file, args=())
#thread2 = threading.Thread(target=open_py_file1, args=())

#thread1.start()
#thread2.start()