# P1

En este repositorio se pueden encontrar dos archivos en los que se resuelve un problema de productor- conusmidor.
En ambas soluciones se implementa un merge concurrente en el que NPRO procesos producen números no negativos de forma creciente.
Por otra parte, habrá un NCONS que toma los números, también de forma creciente, y los va colocando en una única lista ordenadamente.

Mientras que en el archivo practica1.py cada productor tiene que esperar a que el consumidor escoja el elemento que ha producido, es decir, el buffer de cada productor tiene capacidad 1.En el archivo opcinal_practica1.py el buffer correspondiente a cada productor tiene una capacidad fija, M,  que puede ser mayor que 1, en este caso concreto se utiliza M=3.

Al ejecutar el código se devolverá el almacén inicial, los procesos que se llevan a cabo durante la ejecución y el array con los elementos ordenados que se van consumiendo.
