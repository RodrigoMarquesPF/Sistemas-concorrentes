import threading
import time
import random

class bounded_buffer:
    def __init__(self, tamanho):
        self.buffer = []
        self.tamanho = tamanho
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def put_resource(self, item, produtor_id):
        with self.not_full:
            while len(self.buffer) == self.tamanho:
                print(f"Produtor {produtor_id} esperando: buffer cheio\n")
                self.not_full.wait()

            self.buffer.append(item)
            print(f"Produtor {produtor_id} produziu: {item}")
            print(f'Buffer: {self.buffer}\n')
            self.not_empty.notify()  

    def get_resource(self, consumidor_id):
        with self.not_empty:
            while len(self.buffer) == 0:
                print(f"Consumidor {consumidor_id} esperando: buffer vazio\n")
                self.not_empty.wait()

            item = self.buffer.pop(0)
            print(f"Consumidor {consumidor_id} consumiu: {item}")
            print(f'Buffer: {self.buffer}\n')

            self.not_full.notify()  
            return item


buffer_monitor = bounded_buffer(5)


def produtor(id):
    while True:
        item = f"item-{random.randint(0, 100)}"
        time.sleep(random.uniform(0.5, 1))
        buffer_monitor.put_resource(item, id)


def consumidor(id):
    while True:
        time.sleep(random.uniform(1, 2))
        buffer_monitor.get_resource(id)


for i in range(5):  
    t = threading.Thread(target=produtor, args=(i,))
    t.daemon = True
    t.start()

for i in range(1):  
    t = threading.Thread(target=consumidor, args=(i,))
    t.daemon = True
    t.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nFIM")
