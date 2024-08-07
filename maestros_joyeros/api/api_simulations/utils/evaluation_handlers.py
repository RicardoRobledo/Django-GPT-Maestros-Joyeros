import math

from maestros_joyeros.evaluations.models import MetricModel, ScoreModel, SimulationModel


__author__ = 'Ricardo'
__version__ = '1.0'
__all__ = ['save_user_evaluation']


def round_average(average):
    integer_part = int(average)
    decimal_part = average - integer_part

    if integer_part <= 5:
        return integer_part  # Do not round if the integer part is less than or equal to 5

    if decimal_part <= 0.5:
        return math.floor(average)
    else:
        return math.ceil(average)


def save_simulation_evaluation(user, evaluations, conversation=None):
    """
    This function save the evaluations of the user about a simulation

    :param evaluations: list of evaluations
    :param user: User instance found
    """

    evaluation_values = tuple(evaluations.values())

    # Getting the average of the evaluation
    average = sum(evaluation_values)/len(evaluation_values)
    average = round_average(average)

    if average <= 5:
        evaluation = SimulationModel.objects.create(
            average=average, user_id=user, conversation=conversation)
    else:
        evaluation = SimulationModel.objects.create(
            average=average, user_id=user, conversation=None)

    # Making the scores up
    scores = []

    for evaluation_name, score in evaluations.items():
        metric = MetricModel.objects.filter(
            metric_name=evaluation_name).first()
        scores.append(ScoreModel(simulation_id=evaluation,
                      metric_id=metric, score=score))

    ScoreModel.objects.bulk_create(scores)
