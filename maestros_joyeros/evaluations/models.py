from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from maestros_joyeros.base.models import BaseModel


__author__ = 'Ricardo'
__version__ = '0.1'


class MetricModel(BaseModel):
    """
    This model define a metric to evaluate the user

    Attributes:
        metric (str): metric to evaluate the user
    """

    class Meta:
        verbose_name = 'metric'
        verbose_name_plural = 'metrics'

    metric_name = models.CharField(max_length=50, null=False, blank=False,)

    def __str__(self):
        return self.metric_name

    def __repr__(self):
        return f"MetricModel(id={self.id}, metric={self.metric_name}, created_at={self.created_at}), updated_at={self.updated_at})"


class SimulationModel(BaseModel):
    """
    This model define a simulation

    Attributes:
        average (int): average of the evaluation gotten from the scores
        conversation (str): conversation of the evaluation
        user_id (int): user id of the user
    """

    average = models.IntegerField(null=False, blank=False, validators=[
                                  MinValueValidator(1), MaxValueValidator(10)])
    user_id = models.ForeignKey(
        'users.UserModel', null=False, blank=False, on_delete=models.DO_NOTHING, related_name='user_simulations')
    conversation = models.TextField(null=True)

    class Meta:
        verbose_name = 'simulation_evaluation'
        verbose_name_plural = 'simulation_evaluations'

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return f"SimulationEvaluationModel(id={self.id}, average={self.average}, conversation={self.conversation}, user_id={self.user_id}, created_at={self.created_at}), updated_at={self.updated_at})"


class WorkshopEvaluationModel(BaseModel):
    """
    This model define an evaluation about a workshop

    Attributes:
        average (int): average of the evaluation gotten from the scores
        topic_id (int): topic id of a topic
        user_id (int): user id of the user
    """

    average = models.IntegerField(null=False, blank=False, validators=[
                                  MinValueValidator(1), MaxValueValidator(10)])
    topic_id = models.ForeignKey('documents.TopicModel', blank=False,
                                 null=False, default=None, on_delete=models.DO_NOTHING, related_name='topic_workshop_evaluations')
    user_id = models.ForeignKey(
        'users.UserModel', null=False, blank=False, on_delete=models.DO_NOTHING, related_name='user_workshop_evaluations')

    class Meta:
        verbose_name = 'workshop_evaluation'
        verbose_name_plural = 'workshop_evaluations'

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return f"WorkshopEvaluationModel(id={self.id}, average={self.average}, topic_id={self.topic_id}, user_id={self.user_id}, created_at={self.created_at}), updated_at={self.updated_at})"


class ScoreModel(BaseModel):
    """
    This model define a score

    Attributes:
        user_id (UserModel): user that has the score
        metric_id (MetricModel): metric of the score
        simulation_id (SimulationModel): evaluation of the score
        created_at (datetime): creation date
    """

    class Meta:
        verbose_name = 'score'
        verbose_name_plural = 'scores'
        indexes = [
            models.Index(name='score_sim_id_idx', fields=['simulation_id']),
            models.Index(name='score_metric_id_idx', fields=['metric_id']),
            models.Index(name='score_id_idx', fields=['id']),
        ]

    simulation_id = models.ForeignKey(
        SimulationModel, null=False, blank=False, on_delete=models.DO_NOTHING, related_name='simulation_scores')
    metric_id = models.ForeignKey(
        MetricModel, null=False, blank=False, on_delete=models.DO_NOTHING, related_name='metric_scores')
    score = models.IntegerField(null=False, blank=False, validators=[
        MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return f'ScoreModel(id={self.id}, simulation_id={self.simulation_id}, metric={self.metric_id}, score={self.score}, created_at={self.created_at})'
