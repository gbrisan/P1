'''

PRÁCTICA 1: PRODUCTOR/CONSUMIDOR PARTE OPCIONAL

CURSO: 2022/2023

'''

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import randint
from random import random


M = 3       #Capacidad de cada buffer
N = 10      #Número de procesos de cada productor
NPROD = 4   #Número de productores
NCONS = 1   #Número de consumidores

def delay(factor = 3):
    sleep(random()/factor)

def producto(producto):
    producto += randint(0,10)
    return producto

def produciendo(pid, empty, non_empty,almacen,mutex):
    new_product = 0
    i_esc = 0 #Índice de escritura

    for v in range(N): #Para cada productor hay N procesos
        print (f"producer {current_process().name} produciendo")

        empty.acquire() #Espera hasta que alguna posición esté vacía
        
        mutex.acquire()
        new_product = producto(new_product)
        almacen[i_esc] = new_product #Almacena el producto en la pos. indicada
                                     #por el índice de escritura módulo M
        i_esc = (i_esc + 1) % M #La posición de escritura se incrementa en una unidad
        mutex.release()
            
        non_empty.release() #Se avisa al consumidor de que el almacén no está vacío

    print (f"producer {current_process().name} almacenado {list(almacen)}")

    #Cuando ya no hay más producciones en la posición en la que iría el nuevo
    #producto se añade un -1 y así no se vuelve a consultar ese almacén
    
    empty.acquire()  #Espera a que el almacén esté vacía
    almacen[i_esc] = -1
    
    non_empty.release()
   

def consumer(empty, non_empty, almacenes, mutex):
    lista_ordenada = [] #Lista con los valores ordenados de menor a mayor

    i_lec = [0 for _ in range(NPROD)]     #Lista de índices de lectura
    lista = [-1 for _ in range(NPROD)]    #Lista de dim NPROD de -1

    #Esperamos a que todos los productores hayan producido y almacenado
    for i in range(NPROD):
        non_empty[i].acquire()

    #Comprobamos que alguna de los elementos del almacén de la posición de lec sea
    #distinto de -1
    leer =[]
    for i in range(NPROD):
        leer.append(almacenes[i][0])

    while leer != lista:

        print (f"consumer {current_process().name} desalmacenando")
        #Buscamos el mínimo elemento de las posiciones de lectura
        (a,b) = minimo(leer, mutex)

        print (f"consumer {current_process().name} consumiendo {b}")
        #Añadimos el elemento a la lista ordenada


        i_lec[a] = (i_lec[a] + 1) % M #Incrementamos el índice de lectura para el almacén del
                      #del productor al que correspondía el elemento mínimo

        non_empty[a].acquire()
        empty[a].release()
        leer[a] = almacenes[a][i_lec[a]] #Cambiamos el elemento que estamos leyendo
        print(a)
        lista_ordenada.append(b)

    delay()

    print(lista_ordenada)

def minimo(lista, mutex):

    '''
    Esta función calcula el elemento mínimo no negativo de una lista

    Parámetro de entrada: lista
    Parámetro de salida : tupla

    La función devuelve una tupla en la que la primera componente muestra el
    índice de la lista en la que se encuentra el elemento buscado y en la segunda,
    el propio elemento

    '''
    mutex.acquire()
    a = 0
    b = lista[0]
    #Nos aseguramos de que el primer elemento con el que se compara no sea -1
    while b == -1:
        a += 1
        b = lista[a]
        
    #Escogemos el elemento más pequeño del almacén
    for i in range(len(lista)):
        if lista[i] <= b and lista[i] >= 0:
            a = i
            b = lista[i]
    mutex.release()

    return (a, b)


def merge():
    almacenes = []

    for i in range (NPROD):
        storage = Array('i', M)
        for i in range(M):
            storage[i] = -2
        almacenes.append(storage)

    #Generamos dos listas de semáforo
    non_empty = [Semaphore(0) for _ in range(NPROD)]
    #Cada elemento de la lista se asocia a un productor pid
    #Indica si el almacén asociado al productor pid no está vacío

    empty = [BoundedSemaphore(M) for _ in range(NPROD)]
    #Cada elemento de la lista se asocia a un productor pid
    #Indica si en el almacén de pid, que tiene capacidad M, hay espacio
    mutex = Lock()
    
    prodlst = [ Process(target=produciendo,
                        name=f'prod_{pid}',
                        args=(pid, empty[pid], non_empty[pid],almacenes[pid],mutex))
                for pid in range(NPROD) ]

    conslst = [ Process(target=consumer,
                      name=f"cons",
                      args=(empty, non_empty,almacenes,mutex))]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()


if __name__ == '__main__':
    merge()
