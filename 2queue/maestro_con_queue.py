#!/usr/bin/env python3

import multiprocessing
import asyncio
import time
import random
import sys
import threading
import os

def worker(task_queue, result_queue, shutdown_event, worker_id):
    """
    Función que ejecuta cada proceso trabajador.
    Utiliza asyncio para manejar tareas de manera concurrente.
    """
    asyncio.run(worker_async(task_queue, result_queue, shutdown_event, worker_id))

async def worker_async(task_queue, result_queue, shutdown_event, worker_id):
    """
    Función asíncrona del trabajador que maneja las tareas.
    """
    loop = asyncio.get_event_loop()
    
    while not shutdown_event.is_set():
        try:
            # Obtener tarea de la cola en un hilo separado para no bloquear el loop
            task = await loop.run_in_executor(None, task_queue.get)
            
            if task is None:
                # Señal de apagado recibida
                print(f"Trabajador {worker_id}: Recibí señal de apagado.")
                break
            
            print(f"Trabajador {worker_id}: Ejecutando tarea {task}")
            # Ejecutar la tarea de manera asíncrona
            result = await execute_task(task)
            # Enviar el resultado de vuelta al maestro
            result_queue.put((worker_id, task, result))
        
        except Exception as e:
            # Manejo de excepciones durante el procesamiento de tareas
            error_message = f"Error: {e}"
            print(f"Trabajador {worker_id}: {error_message}")
            result_queue.put((worker_id, task, error_message))
    
    print(f"Trabajador {worker_id}: Apagando de manera ordenada.")

async def execute_task(task):
    """
    Ejecuta una tarea basada en su tipo.
    Soporta operaciones matemáticas y lectura de archivos.
    """
    task_type = task.get('tipo')
    
    if task_type == 'matematica':
        operation = task.get('operacion')
        operands = task.get('operandos', [])
        return perform_math_operation(operation, operands)
    
    elif task_type == 'leer_archivo':
        filepath = task.get('ruta_archivo')
        return await read_file_async(filepath)
    
    else:
        return f"Tipo de tarea desconocido: {task_type}"

def perform_math_operation(operation, operands):
    """
    Realiza una operación matemática básica.
    """
    try:
        if not operands:
            return "No se proporcionaron operandos."
        
        if operation == 'sumar':
            return sum(operands)
        elif operation == 'restar':
            result = operands[0]
            for num in operands[1:]:
                result -= num
            return result
        elif operation == 'multiplicar':
            result = 1
            for num in operands:
                result *= num
            return result
        elif operation == 'dividir':
            result = operands[0]
            try:
                for num in operands[1:]:
                    result /= num
                return result
            except ZeroDivisionError:
                return "Error: División por cero."
        else:
            return f"Operación matemática desconocida: {operation}"
    except Exception as e:
        return f"Error en operación matemática: {e}"

async def read_file_async(filepath):
    """
    Lee el contenido de un archivo de manera asíncrona.
    """
    try:
        # Verificar si el archivo existe
        if not os.path.isfile(filepath):
            return f"Error: El archivo '{filepath}' no existe."
        
        # Leer el archivo de manera asíncrona
        loop = asyncio.get_event_loop()
        with open(filepath, 'r') as file:
            content = await loop.run_in_executor(None, file.read)
        return content
    except Exception as e:
        return f"Error al leer el archivo: {e}"

def result_collector(result_queue, shutdown_event):
    """
    Función que ejecuta en un hilo separado para recoger y mostrar resultados.
    """
    while not shutdown_event.is_set() or not result_queue.empty():
        try:
            # Intentar obtener un resultado con timeout para permitir la verificación del shutdown_event
            worker_id, task, result = result_queue.get(timeout=1)
            print(f"\n[Resultado] Trabajador {worker_id} completó la tarea {task}: {result}\n> ", end='', flush=True)
        except multiprocessing.queues.Empty:
            continue
        except Exception as e:
            print(f"\n[Error en el colector de resultados]: {e}\n")

def master(num_workers, shutdown_event):
    """
    Función principal del maestro.
    Gestiona la entrada del usuario, distribución de tareas y recolección de resultados.
    """
    # Crear colas de tareas y resultados
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    
    # Lista para mantener referencias a los procesos trabajadores
    workers = []
    
    # Iniciar los procesos trabajadores
    for i in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(task_queue, result_queue, shutdown_event, i))
        p.start()
        workers.append(p)
        print(f"Maestro: Iniciado trabajador {i}")
    
    # Iniciar el hilo colector de resultados
    collector_thread = threading.Thread(target=result_collector, args=(result_queue, shutdown_event))
    collector_thread.start()
    
    print("\nBienvenido al sistema maestro-trabajador.")
    print("Ingrese sus tareas en los siguientes formatos:")
    print("  - Operaciones matemáticas: sumar 1 2 3 | restar 10 5 | multiplicar 4 5 | dividir 20 4")
    print("  - Lectura de archivos: leer_archivo ruta/al/archivo.txt")
    print("Escriba 'salir' para terminar.\n")
    
    try:
        while True:
            user_input = input("> ").strip()
            
            if user_input.lower() == 'salir':
                print("Maestro: Recibiendo señal de apagado.")
                shutdown_event.set()
                break
            
            if not user_input:
                continue  # Ignorar entradas vacías
            
            # Analizar la entrada del usuario en una tarea
            task = parse_user_input(user_input)
            
            if task:
                task_queue.put(task)
                print(f"Maestro: Tarea enviada: {task}")
            else:
                print("Maestro: Formato de tarea inválido.")
    
    except KeyboardInterrupt:
        print("\nMaestro: Interrupción por teclado recibida. Apagando...")
        shutdown_event.set()
    
    finally:
        # Enviar señales de apagado a los trabajadores
        for _ in workers:
            task_queue.put(None)
        
        # Esperar a que los trabajadores terminen
        for i, p in enumerate(workers):
            p.join()
            print(f"Maestro: Trabajador {i} ha terminado.")
        
        # Esperar a que el colector de resultados termine
        collector_thread.join()
        print("Maestro: Colector de resultados ha terminado.")
        print("Maestro: Todos los trabajadores han finalizado. Saliendo.")

def parse_user_input(user_input):
    """
    Funcion para analizar la entrada del usuario y convertirla en una tarea estructurada.
    """
    parts = user_input.split()
    if not parts:
        return None
    
    command = parts[0].lower()
    
    if command in ['sumar', 'restar', 'multiplicar', 'dividir']:
        if len(parts) < 3:
            print(f"Maestro: La operación '{command}' requiere al menos dos operandos.")
            return None
        try:
            operands = [float(part) for part in parts[1:]]
            return {
                'tipo': 'matematica',
                'operacion': command,
                'operandos': operands
            }
        except ValueError:
            print("Maestro: Los operandos deben ser números.")
            return None
    
    elif command == 'leer_archivo':
        if len(parts) != 2:
            print("Maestro: El comando 'leer_archivo' requiere exactamente un argumento (ruta del archivo).")
            return None
        filepath = parts[1]
        return {
            'tipo': 'leer_archivo',
            'ruta_archivo': filepath
        }
    
    else:
        print(f"Maestro: Comando desconocido '{command}'.")
        return None

if __name__ == "__main__":
    # Definir el número de trabajadores
    NUM_WORKERS = 4
    
    # Crear un evento de apagado compartido
    shutdown_event = multiprocessing.Event()
    
    # Iniciar el maestro
    master(NUM_WORKERS, shutdown_event)
