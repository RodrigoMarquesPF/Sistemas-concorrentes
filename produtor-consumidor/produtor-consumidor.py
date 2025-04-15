import threading
import time
import random


buffer = []
N = 5

mutex = threading.Semaphore(1)            
empty = threading.Semaphore(N)  
full = threading.Semaphore(0)             

def produtor(id):
    while True:
        item = f"Item-{random.randint(0, 10)}"
        time.sleep(random.uniform(0.5, 10))  
        empty.acquire()
        mutex.acquire()     # Entra na seção crítica
        buffer.append(item)
        print(f"Produtor {id} produziu: {item}")
        print(f'Buffer: {buffer}\n')
        mutex.release()     # Sai da seção crítica
        full.release()      

def consumidor(id):
    while True:
        full.acquire()      
        mutex.acquire()     # Entra na seção crítica
        item = buffer.pop(0)
        print(f"Consumidor {id} consumiu: {item}")
        print(f'Buffer: {buffer}\n')
        mutex.release()     # Sai da seção crítica
        empty.release()     
        time.sleep(random.uniform(0.5, 5))  


for i in range(4): 
    t = threading.Thread(target=produtor, args=(i,))
    t.daemon = True
    t.start()
    time.sleep(2) 

for i in range(5):
    t = threading.Thread(target=consumidor, args=(i,))
    t.daemon = True
    t.start()
    time.sleep(1) 


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nFIM")
