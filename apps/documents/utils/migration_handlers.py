import os
from apps.base.utils.file_handlers import read_document_files


__author__ = 'Ricardo'
__version__ = '1.0'


def insert_initial_data(apps, schema_editor):

    TopicModel = apps.get_model('documents', 'TopicModel')
    DocumentModel = apps.get_model('documents', 'DocumentModel')

    notifications_objects = TopicModel.objects.create(topic_name='Notificaciones')
    DocumentModel.objects.create(document_name='Notificaciones', content='No hay notificaciones nuevas', topic_id=notifications_objects)

    folder_paths = [
        'Información/Información_general/Información_de_la_empresa_y_general_de_producto',
        'Información/Información_general/Información_de_ventas_y_procesos',
        'Información/Información_general/Términos_y_condiciones',
    ]

    topic_names_classified = []
    topic_names = []

    for folder_path in folder_paths:
        folder_names = os.listdir(folder_path)
        topic_names_classified.append(folder_names)
        topic_names.extend(folder_names)
    
    topic_objects = []

    for topic_name in topic_names:
        topic_object = TopicModel(topic_name=topic_name)
        topic_objects.append(topic_object)
    
    # adding topics to the database
    TopicModel.objects.bulk_create(topic_objects)
    documents = []

    for folder_path, topic_classifieds in zip(folder_paths, topic_names_classified):

        for topic_classified in topic_classifieds:
            documents_gotten = read_document_files(f'{folder_path}/{topic_classified}', topic_classified)
            documents.extend(documents_gotten)

    # adding documents to the database
    DocumentModel.objects.bulk_create(documents)
