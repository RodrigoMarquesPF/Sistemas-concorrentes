import threading
import time
import random


mutex = threading.Semaphore(1)
wrt = threading.Semaphore(1)
read_count = 0
shared_data = []


def leitor(id):
    global read_count
    while True:
        time.sleep(random.uniform(0.5, 2))

        mutex.acquire()
        read_count += 1
        if read_count == 1:
            wrt.acquire()
        mutex.release()

        print(f"Leitor {id} lendo dados: {shared_data}")
        time.sleep(random.uniform(0.5, 1))

        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            wrt.release()
        mutex.release()

def escritor(id):
    global shared_data
    while True:
        time.sleep(random.uniform(1, 3))
        wrt.acquire()
        new_data = f"data_from_writer_{id}"
        shared_data.append(new_data)
        print(f"Escritor {id} escreveu: {new_data}")
        time.sleep(random.uniform(0.5, 1))
        wrt.release()


for i in range(3):
    t = threading.Thread(target=leitor, args=(i,))
    t.daemon = True
    t.start()


for i in range(2):
    t = threading.Thread(target=escritor, args=(i,))
    t.daemon = True
    t.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nEncerrando o programa...")
