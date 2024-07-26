__author__ = 'Ricardo'
__version__ = '1.0'


def insert_initial_data(apps, schema_editor):

    MetricModel = apps.get_model('evaluations', 'MetricModel')

    initial_metrics = (
        '4Cs', 'Ortografía', 'Redacción', 'Promueve_acción',
        'No_forzado', 'Sinceridad', 'Empatía', 'Iniciativa',
        'Seguimiento', 'Cierre_conversación',
    )

    for metric_name in initial_metrics:
        MetricModel.objects.create(metric_name=metric_name)
