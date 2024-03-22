# Glucose SAT solver

Esta carpeta contiene la implementación de [Glucose SAT Solver](https://www.labri.fr/perso/lsimon/research/glucose/) y la solución del problema planteado.
Los archivos de la implementación se encuentran en la carpeta simp. Existen los archivos:

    client.py: Se encarga de manejar la entrada y llamar al resto de las funciones

    decode.py: Se encarga de tomar el archivo con formato DIMACS y lo transforma en un archivo .ics

    library.py: Contiene todas las funciones que se encargan de leer los archivos json y generar las cláusulas del problema para la generación del archivo con formato DIMACS.

    CSP.py: Contiene una implementación del algoritmo CSP y posterior llamada a las funciones en decode.py para la generación del archivo .ics. Aunque contiene las restricciones necesarias, se realizaron las pruebas con las funciones en library.py debido a que la corrida de este archivo nunca terminó.

Los archivos json: file, test, test2, test3, test4 y test5, son los archivos de prueba que se utilizaron para probar library.py

# Cómo correr el programa

El archivo Makefile incluye un make clean para eliminar los archivos extra que se generan con la corrida de los algoritmos (.txt y .ics).
Para correr el programa se debe ejecutar el siguiente comando:

    python client.py JSON_NAME DIMACS_NAME OUTPUT_NAME CALENDAR_NAME

En donde 
    JSON_NAME es el nombre de un archivo json, por ej. file.json
    DIMACS_NAME es el nombre de un archivo txt en donde se alojará el formato DIMACS
    OUTPUT_NAME es el nombre de un archivo txt en donde se guarda el valor que retorna el glucose SAT solver
    CALENDAR_NAME es el nombre del archivo ics que se genera a partir del glucose SAT solver

Todos los archivos deben incluir la extensión para poder correr de manera correcta el programa.
Por ejemplo,

    python client.py file.json dimacs.txt output.txt calendar.ics

Es una corrida correcta

    python client.py file dimacs output calendar

No lo es