from django.db.models import Sum

from apps.evaluations.models import WorkshopEvaluationModel
from apps.documents.models import DocumentModel


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['get_documents_not_evaluated', 'sum_averages']


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
        topic_id__in=[evaluation['topic_id'] for evaluation in topic_evaluations_done]
    )

    return documents_not_evaluated


def sum_averages_evaluations(user, start_date):
    """
    This function will get the sum of the average of the evaluations done by the user and order them

    :param user: UserModel instance
    :param start_date: start date to get the evaluations
    :return: QuerySet of evaluations with sum averages
    """

    sum_averages_evaluations = WorkshopEvaluationModel.objects.filter(
        user_id=user.id, created_at__gte=start_date
    ).values(
        'topic_id'
    ).annotate(
        sum_average=Sum('average')
    ).order_by('sum_average')

    return sum_averages_evaluations
