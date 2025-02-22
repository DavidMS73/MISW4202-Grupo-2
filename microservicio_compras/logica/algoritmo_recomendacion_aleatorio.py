import math
import queue
import random


class ResultadoRecomendacion:
    def __init__(self, id: int, result: int):
        self.id = id
        self.result = result


def __calcular_porcentaje_evento(evento: str) -> float:
    """
    Calcula el porcentaje de incremento en las ventas de un producto dado un evento.\n
    - Evento grande: 50% - 100%
    - Evento mediano: 20% - 50%
    - Evento pequeño: 10% - 20%
    :param evento: El evento que se está considerando
    :return: El porcentaje de incremento en las ventas
    """
    match evento:
        case "evento_grande":
            return 1.5 + (random.random() * 0.5)

        case "evento_mediano":
            return 1.2 + (random.random() * 0.3)

        case _:
            return 1.1 + (random.random() * 0.1)


def obtener_recomendaciones_aleatorio(inventario_producto: int,
                                      ventas_proyectadas: int,
                                      eventos: [str],
                                      id: int,
                                      result_queue: queue.Queue[ResultadoRecomendacion]):
    proyeccion_ventas = 0

    for evento in eventos:
        proyeccion_ventas += ventas_proyectadas * __calcular_porcentaje_evento(evento)

    cantidad_necesaria = proyeccion_ventas - inventario_producto

    "Simular un error en la recomendación"
    if random.random() < 0.1:
        "10% de las veces se recomienda una cantidad menor a la necesaria"
        cantidad_necesaria *= 0.2
    elif random.random() < 0.2:
        "10% de las veces se recomienda una cantidad mayor a la necesaria"
        cantidad_necesaria *= 1.8

    result_queue.put(
        ResultadoRecomendacion(id, math.ceil(cantidad_necesaria))
    )
