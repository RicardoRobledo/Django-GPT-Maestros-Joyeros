from typing import TypedDict, Iterable
import io

import matplotlib.pyplot as plt
import numpy as np


__author__ = 'Ricardo'
__version__ = '0.1'


class MetricDict(TypedDict):
    metric_average: float
    metric_name: str


def create_radar_chart(metrics: Iterable[MetricDict]):
    # Extraer nombres de las métricas y sus valores
    valores = [metric['metric_average'] for metric in metrics]

    categorias = [
        f"{metric['metric_name']}\n{metric['metric_average']}" for metric in metrics]
    # Asegurarse de que los valores sean un círculo completo
    angulos = np.linspace(
        0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    valores = np.concatenate((valores, [valores[0]]))
    angulos += angulos[:1]

    # Crear el gráfico de radar
    fig, ax = plt.subplots(
        figsize=(14, 14), subplot_kw=dict(polar=True))
    # Verde esmeralda con más transparencia
    ax.fill(angulos, valores, color='#23F4C4', alpha=0.2)
    # Verde oscuro para el borde
    ax.plot(angulos, valores, color='#26CFA8', linewidth=2)

    # Ajustes de las categorías
    # Mostrar ticks del 1 al 10
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='major', pad=145)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias, fontsize=40, color='#000000')

    # Mejora en el estilo
    # Líneas de cuadrícula en verde claro
    ax.grid(color='#B6B6B6', linestyle='solid')
    ax.set_facecolor('#444444')  # Fondo en un tono verde muy claro

    # Guardar el gráfico en un búfer en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    # Cerrar la figura
    plt.close(fig)

    return buffer
