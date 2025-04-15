import threading
import time
import random

class BufferMonitor:
    def __init__(self, tamanho):
        self.buffer = []
        self.tamanho = tamanho
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def inserir(self, item, produtor_id):
        with self.not_full:
            while len(self.buffer) == self.tamanho:
                print(f"Produtor {produtor_id} esperando: buffer cheio\n")
                self.not_full.wait()

            self.buffer.append(item)
            print(f"Produtor {produtor_id} produziu: {item} | Buffer: {self.buffer}\n")

            self.not_empty.notify()  

    def remover(self, consumidor_id):
        with self.not_empty:
            while len(self.buffer) == 0:
                print(f"Consumidor {consumidor_id} esperando: buffer vazio\n")
                self.not_empty.wait()

            item = self.buffer.pop(0)
            print(f"Consumidor {consumidor_id} consumiu: {item} | Buffer: {self.buffer}\n")

            self.not_full.notify()  
            return item


buffer_monitor = BufferMonitor(5)


def produtor(id):
    while True:
        item = f"item_{id}_{random.randint(0, 100)}"
        time.sleep(random.uniform(0.5, 1))
        buffer_monitor.inserir(item, id)


def consumidor(id):
    while True:
        time.sleep(random.uniform(0.5, 2))
        buffer_monitor.remover(id)


for i in range(2):  
    t = threading.Thread(target=produtor, args=(i,))
    t.daemon = True
    t.start()

for i in range(3):  
    t = threading.Thread(target=consumidor, args=(i,))
    t.daemon = True
    t.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nEncerrando o programa...")
