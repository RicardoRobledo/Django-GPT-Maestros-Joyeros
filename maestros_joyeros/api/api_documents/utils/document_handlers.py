import random

from maestros_joyeros.evaluations.models import WorkshopEvaluationModel
from maestros_joyeros.documents.models import TopicModel, DocumentModel
from maestros_joyeros.products.models import ProductModel


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['get_context_documents', 'get_documents',
           'get_document', 'get_documents_not_evaluated']


def get_context_documents():
    """
    This function return two context documents for the simulation with high weights

    :return: QuerySet of context documents
    """

    documents = DocumentModel.objects.filter(for_simulation=True)

    document_names = []
    document_weights = []

    for document in documents:
        document_names.append(document.document_name)
        document_weights.append(document.weight)

    document_names_selected = random.choices(
        document_names, weights=document_weights, k=2)
    documents_selected = DocumentModel.objects.filter(
        document_name__in=document_names_selected)

    return documents_selected


def get_documents(topics):
    """
    This function return supporting documents for a simulation
    """

    documents_gotten = []
    topics = TopicModel.objects.filter(id__in=[l['topic_id'] for l in topics])

    for topic in topics:
        topic_documents = DocumentModel.objects.filter(
            topic_id=topic.id, for_mystery_shopping=True)
        documents_gotten.append(random.choice(topic_documents))

    return documents_gotten


def get_document(topic):
    """
    This function return a main document about a topic for a simulation
    """

    topic = TopicModel.objects.filter(id=topic['topic_id']).first()
    topic_documents = DocumentModel.objects.filter(
        topic_id=topic.id, for_mystery_shopping=True)
    document = random.choice(topic_documents)

    return document


def get_documents_not_evaluated(user, start_date, **options):
    """
    Get the documents in which the user has not done an evaluation

    :param user: UserModel instance
    :param start_date: start date to get the evaluations
    :param options: options to filter the documents (for_simulation, for_workshop)
    """

    # Getting our workshop evaluations done and topic of that evaluations
    topic_evaluations_done = WorkshopEvaluationModel.objects.filter(
        user_id=user.id,
        created_at__gte=start_date
    ).values(
        'topic_id'
    ).distinct()

    # Getting the documents in which we can do a an evaluation and removing the ones we have already done
    documents_not_evaluated = DocumentModel.objects.filter(
        **options
    ).prefetch_related(
        'topic_id'
    ).values(
        'id', 'topic_id'
    ).distinct(
    ).exclude(
        topic_id__in=[evaluation['topic_id']
                      for evaluation in topic_evaluations_done]
    )

    return documents_not_evaluated
