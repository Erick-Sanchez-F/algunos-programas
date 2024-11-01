Sistema Maestro-Trabajador en Python

Tabla de Contenidos:
  1. Descripción
  2. Características
  3. Uso
  4. Formato de Tareas
  5. Ejemplos
  6. Estructura del Proyecto

1. Descripción:
El Sistema Maestro-Trabajador, es una implementación en Python que utiliza los módulos multiprocessing y asyncio para gestionar y ejecutar tareas de manera concurrente. Este sistema permite que un proceso maestro distribuya tareas a múltiples procesos trabajadores, los cuales procesan dichas tareas de forma asíncrona y devuelven los resultados al maestro, para mostrar al usuario.

¿Qué puede hacer?
Operaciones Matemáticas: Realizar sumas, restas, multiplicaciones y divisiones de números proporcionados por el usuario.
Lectura de Archivos: Leer el contenido de archivos especificados por el usuario.

2. Características:
a. Concurrencia y Paralelismo: Utiliza asyncio para la ejecución asíncrona dentro de cada trabajador, optimizando el rendimiento.
b. Permite al usuario ingresar tareas de forma interactiva desde la línea de comandos.
c. Manejo de Errores: Gestiona errores comunes como divisiones por cero y archivos inexistentes, proporcionando retroalimentación clara al usuario.
d. Apagado Ordenado: Implementa un mecanismo para finalizar los procesos trabajadores de manera ordenada al cerrar el programa.
e. Módulos Utilizados:
   - multiprocessing
   - asyncio
   - time
   - random
   - sys
   - threading
   - os
   Estos módulos son parte de la biblioteca estándar de Python, por lo que no es necesario instalarlos por separado.

3. Uso:
a. Si deseas probar la funcionalidad de lectura de archivos, el archivo de texto ejemplo.txt, se encuentra en el mismo directorio del script.

b. Una vez que el programa esté en ejecución, podrás ingresar tareas en los siguientes formatos:

4. Formato de tareas:

Operaciones Matemáticas

sumar 10 20 30
restar 100 50
multiplicar 7 6
dividir 40 8

Lectura de Archivos
leer_archivo <ruta_al_archivo>, en este caso es: ejemplo.txt

Salir del Programa

5. Ejemplos:

- Sumar Números:
>sumar 10 20 30
Maestro: Tarea enviada: {'tipo': 'matematica', 'operacion': 'sumar', 'operandos': [10.0, 20.0, 30.0]}

- Restar Números:
>subtract 100 50
Maestro: Tarea enviada: {'tipo': 'matematica', 'operacion': 'restar', 'operandos': [100.0, 50.0]}

- Multiplicar Números:
>multiplicar 7 6
Maestro: Tarea enviada: {'tipo': 'matematica', 'operacion': 'multiplicar', 'operandos': [7.0, 6.0]}

- Dividir Números:
>dividir 40 8
Maestro: Tarea enviada: {'tipo': 'matematica', 'operacion': 'dividir', 'operandos': [40.0, 8.0]}

- Leer un Archivo:
>leer_archivo ejemplo.txt
Maestro: Tarea enviada: {'tipo': 'leer_archivo', 'ruta_archivo': 'ejemplo.txt'}

- Salir del Programa:
>salir
Maestro: Recibiendo señal de apagado.
Trabajador 1: Recibí señal de apagado.
Trabajador 1: Apagando de manera ordenada.
Trabajador 3: Recibí señal de apagado.
Trabajador 3: Apagando de manera ordenada.
Trabajador 2: Recibí señal de apagado.
Trabajador 2: Apagando de manera ordenada.
Trabajador 0: Recibí señal de apagado.
Trabajador 0: Apagando de manera ordenada.
Maestro: Trabajador 0 ha terminado.
Maestro: Trabajador 1 ha terminado.
Maestro: Trabajador 2 ha terminado.
Maestro: Trabajador 3 ha terminado.
Maestro: Colector de resultados ha terminado.
Maestro: Todos los trabajadores han finalizado. Saliendo.

6. Estructura del Proyecto

sistema-maestro-trabajador
├── maestro_con_queue.py
├── ejemplo.txt
├── README.md

maestro_con_queue.py: Archivo principal que contiene la implementación del sistema maestro-trabajador.
ejemplo.txt: Archivo de ejemplo para probar la funcionalidad de lectura de archivos.
README.md: Este archivo de documentación.
