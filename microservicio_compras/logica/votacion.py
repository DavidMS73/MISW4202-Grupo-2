import itertools
import math
import queue
import threading

# from .algoritmo_recomendacion import ResultadoRecomendacion
from .algoritmo_recomendacion_deterministico import obtener_recomendaciones_deterministico, ResultadoRecomendacion


def votar_recomendacion_compras(inventario_producto: int,
                                proyeccion_ventas: int,
                                eventos: [str]) -> tuple[int, list[ResultadoRecomendacion]]:
    result_queue: queue.Queue[ResultadoRecomendacion] = queue.Queue()

    recomendacion_1 = threading.Thread(target=obtener_recomendaciones_deterministico,
                                       args=(inventario_producto, proyeccion_ventas, eventos, 1, result_queue))
    recomendacion_2 = threading.Thread(target=obtener_recomendaciones_deterministico,
                                       args=(inventario_producto, proyeccion_ventas, eventos, 1, result_queue))
    recomendacion_3 = threading.Thread(target=obtener_recomendaciones_deterministico,
                                       args=(inventario_producto, proyeccion_ventas, eventos, 1, result_queue))

    recomendacion_1.start()
    recomendacion_2.start()
    recomendacion_3.start()

    recomendacion_1.join()
    recomendacion_2.join()
    recomendacion_3.join()

    results: list[ResultadoRecomendacion] = [result_queue.get() for _ in range(3)]
    combinations = list(itertools.combinations(results, 2))

    differences: list[tuple[int, int]] = [(i, abs(combinations[i][0].result - combinations[i][1].result)) for i in
                                          range(len(combinations))]

    least_different_result = min(differences, key=lambda x: x[1])
    index = least_different_result[0]

    return (math.ceil(sum([result.result for result in combinations[index]]) / 2),
            results)
