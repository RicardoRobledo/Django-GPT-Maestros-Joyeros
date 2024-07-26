import random

from django.db.models import Q

from apps.documents.models import TopicModel, DocumentModel
from apps.products.models import ProductModel


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['prepare_documents', 'prepare_product', 'get_context_documents']


def prepare_product():
    """
    Select a random product from the database
    """

    products = ProductModel.objects.all()
    return random.choice(products)


def get_context_documents():
    """
    This function return the context documents for the simulation

    :return: QuerySet of context documents
    """

    context_documents = DocumentModel.objects.filter(
        Q(document_name="Información de comportamiento y de la empresa") |
        Q(document_name="Calidad del servicio") |
        Q(document_name="Negociación") |
        Q(document_name="Proceso de ventas") |
        Q(document_name="Oferta de servicios y capacidades") |
        Q(document_name="Política de comisiones") |
        Q(document_name="Cambios y devoluciones de productos") |
        Q(document_name="Cancelaciones") |
        Q(document_name="Disponibilidad y existencia") |
        Q(document_name="Envíos y entregas aseguradas") |
        Q(document_name="Facturación") |
        Q(document_name="Forma de pago") |
        Q(document_name="Garantía") |
        Q(document_name="Orden de compra digital") |
        Q(document_name="Precios") |
        Q(document_name="Productos y servicios") |
        Q(document_name="Promociones y cupones") |
        Q(document_name="Quejas y reclamaciones") |
        Q(document_name="Reembolso de dinero") |
        Q(document_name="Seguridad") |
        Q(document_name="Suscripción o registro de nuevos usuarios por internet")
    )

    return context_documents


def get_documents(topics):
    """
    This function return supporting documents for a simulation
    """

    documents_gotten = []
    topics = TopicModel.objects.filter(id__in=[l['topic_id'] for l in topics])

    for topic in topics:
        topic_documents = DocumentModel.objects.filter(topic_id=topic.id, for_mystery_shopping=True)
        documents_gotten.append(random.choice(topic_documents))

    return documents_gotten


def get_document(topic):
    """
    This function return a main document about a topic for a simulation
    """

    topic = TopicModel.objects.filter(id=topic['topic_id']).first()
    topic_documents = DocumentModel.objects.filter(topic_id=topic.id, for_mystery_shopping=True)
    document = random.choice(topic_documents)

    return document
