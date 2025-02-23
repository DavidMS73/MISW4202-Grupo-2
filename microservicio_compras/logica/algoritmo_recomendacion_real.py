import math


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


def obtener_recomendaciones_real(inventario_producto: int,
                                 ventas_proyectadas: int,
                                 eventos: [str]) -> int:
    proyeccion_ventas = 0

    for evento in eventos:
        proyeccion_ventas += ventas_proyectadas * __calcular_porcentaje_evento(evento)

    cantidad_necesaria = proyeccion_ventas - inventario_producto

    return math.ceil(cantidad_necesaria)
