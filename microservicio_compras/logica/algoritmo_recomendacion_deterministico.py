import math
import queue
import random
import time


class ResultadoRecomendacion:
    def __init__(self, id: int, result: int, return_time: float):
        self.id = id
        self.result = result
        self.return_time = return_time


def __calcular_porcentaje_evento(evento: str) -> float:
    """
    Calcula el porcentaje de incremento en las ventas de un producto dado un evento.\n
    - Evento grande: 50%
    - Evento mediano: 20%
    - Evento pequeño: 10%
    :param evento: El evento que se está considerando
    :return: El porcentaje de incremento en las ventas
    """
    match evento:
        case "evento_grande":
            return 1.5

        case "evento_mediano":
            return 1.2

        case _:
            return 1.1


def obtener_recomendaciones_deterministico(inventario_producto: int,
                                           ventas_proyectadas: int,
                                           eventos: [str],
                                           id: int,
                                           result_queue: queue.Queue[ResultadoRecomendacion],
                                           simular_error: bool = True):
    proyeccion_ventas = 0

    for evento in eventos:
        proyeccion_ventas += ventas_proyectadas * __calcular_porcentaje_evento(evento)

    cantidad_necesaria = proyeccion_ventas - inventario_producto

    "Simular un error en la recomendación"
    if simular_error and random.random() < 0.2:
        "20% de las veces se recomienda una cantidad errónea"
        cantidad_necesaria *= 0.2

    result_queue.put(
        ResultadoRecomendacion(id, math.ceil(cantidad_necesaria), time.perf_counter())
    )
