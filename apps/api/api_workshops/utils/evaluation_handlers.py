from django.db.models import Sum

from apps.evaluations.models import WorkshopEvaluationModel


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['sum_averages_evaluations', 'save_workshop_evaluation',]


def save_workshop_evaluation(user, average, topic=None):
    """
    This function save the evaluations of the user about a workshop

    :param average: average of the user
    :param user: User instace found
    :param topic: Topic instance found
    """

    WorkshopEvaluationModel.objects.create(average=average, user_id=user, topic_id=topic)


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
