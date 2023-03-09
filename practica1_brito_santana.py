from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
from random import randint
from random import random



N = 5
NPROD = 3
NCONS = 1

def delay(factor = 3):
    sleep(random()/factor)

def producer(pid, storage, empty, non_empty):
    new_product = 0
    
    for v in range(N):
        print (f"producer {current_process().name} produciendo")
        new_product += randint(0,10)
        delay(6) #Esto se pone para esperar
        empty.acquire()
        storage[pid] = new_product
        non_empty.release()
        print (f"producer {current_process().name} almacenado {new_product}")
        
    empty.acquire()
    storage[pid] = -1
    non_empty.release()


def consumer(storage, empty, non_empty):
    lista_ordenada=[]
    lista = [-1 for _ in range(NPROD)]
    
    for i in range(NPROD):
        non_empty[i].acquire()  
        
    #dato =get_data(storage, index, mutex)
    while list(storage) != lista:
        print (f"consumer {current_process().name} desalmacenando")
        a = 0
        b = storage[0]
        #Nos aseguramos de que el primer elemeto con el que se compara no sea -1
        while b == -1:
            a += 1
            b = storage[a]
        #Escogemos el elemento más pequeño del almacén
        for i in range(len(storage)):
            if storage[i] <= b and storage[i] >= 0:
                a = i
                b = storage[i]
        print (f"consumer {current_process().name} consumiendo {b}")
        lista_ordenada.append(b)
        empty[a].release()
        non_empty[a].acquire()
        
    delay()

    print(lista_ordenada)
    
      
def main():

    storage = Array('i', NPROD)
    for i in range(NPROD):
        storage[i] = -2

    print ("almacen inicial", storage[:])
    
    non_empty = [Semaphore(0) for _ in range(NPROD)]
    empty = [BoundedSemaphore(1) for _ in range(NPROD)]
    prodlst = [ Process(target=producer,
                        name=f'prod_{pid}',
                        args=(pid, storage, empty[pid], non_empty[pid]))
                for pid in range(NPROD) ]
    
    conslst = [ Process(target=consumer,
                      name=f"cons",
                      args=(storage, empty, non_empty))]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()


if __name__ == '__main__':
    main()
