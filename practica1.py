'''
PRÁCTICA 1: PRODUCTOR/CONSUMIDOR

CURSO: 2022/2023

'''

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import randint
from random import random



N = 5
NPROD = 3
NCONS = 1

def delay(factor = 3):
    sleep(random()/factor)

def producer(pid, storage, empty, non_empty, mutex):

    new_product = 0

    for v in range(N):
        #Ejecutamos el bucle para los N procesos

        print (f"producer {current_process().name} produciendo")
        #Generamos un número nuevo, mayor o igual al anterior
        new_product += randint(0,10)

        delay(6)
        #Esperamos a que el almacén del productor pid esté vacío
        empty.acquire()

        mutex.acquire()
        #Almacena el nuevo producto en la posición del almacén de pid
        storage[pid] = new_product

        #Avisa al consumidor de que no está vacío
        non_empty.release()
        print (f"producer {current_process().name} almacenado {new_product}")
        mutex.release()
    #Cuando ya ha hecho todos sus procesos almacena -1 para indicar que ya terminó
    empty.acquire()
    storage[pid] = -1
    non_empty.release()


def consumer(storage, empty, non_empty, mutex):
    lista_ordenada=[] #Lista ordenada de menor a mayor de los elem. consumidos
    lista = [-1 for _ in range(NPROD)]

    for i in range(NPROD):
        non_empty[i].acquire()

    #Mientras haya algún elemento en el almacén sigue consumiendo
    #Es decir, mientras algún elemento sea disntinto de -1

    while list(storage) != lista:

        print (f"consumer {current_process().name} desalmacenando")
        a = 0
        mutex.acquire()
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
        mutex.release()
        lista_ordenada.append(b) #Añadimos el elemento a la lista

        empty[a].release() #Avisamos al productor[a] que hemos consumido su producto
        non_empty[a].acquire() #Esperamos a que el productor[a] vuelva a almacenar

    delay()
    print(lista_ordenada) #Devolvemos la lista ordenada


def main():

    storage = Array('i', NPROD)
    #Inicializamos el almacén con -2 para cada posición
    for i in range(NPROD):
        storage[i] = -2

    print ("almacen inicial", storage[:])

    non_empty = [Semaphore(0) for _ in range(NPROD)]
    #Cada elemento de la lista se asocia a un productor pid
    #Indica si el almacén asociado a pid no está vacío

    empty = [BoundedSemaphore(1) for _ in range(NPROD)]
    #Cada elemento de la lista se asocia a un productor pid
    #Avisa que en el almacén asociado a pid, que solo tiene capacidad para un
    #producto, está vacío
    mutex = Lock()
    prodlst = [ Process(target=producer,
                        name=f'prod_{pid}',
                        args=(pid, storage, empty[pid], non_empty[pid], mutex))
                for pid in range(NPROD) ]

    conslst = [ Process(target=consumer,
                      name=f"cons",
                      args=(storage, empty, non_empty, mutex))]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()


if __name__ == '__main__':
    main()
