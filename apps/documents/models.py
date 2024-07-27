from django.db import models

from ..base.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator


__author__ = 'Ricardo'
__version__ = '0.1'


class TopicModel(BaseModel):
    """
    This model define a topic
    
    Attributes:
        topic_name (str): name of the topic
        created_at (datetime): creation date
    """

    topic_name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = 'topic'
        verbose_name_plural = 'topics'
    
    def __str__(self):
        return self.topic_name
    
    def __repr__(self):
        return f"TopicModel(id={self.id}, topic_name={self.topic_name}, created_at={self.created_at})"


class DocumentModel(BaseModel):
    """
    This model define a document
    
    Attributes:
        document_name (str): name of the document
        content (str): content of the document
        for_workshop (bool): if the document is used to do a workshop
        for_simulation (bool): if the document is used to do a simulation
        topic_id (TopicModel): topic of the document
    """

    document_name = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField()
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    for_workshop = models.BooleanField(default=True)
    for_simulation = models.BooleanField(default=True)
    topic_id = models.ForeignKey(TopicModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'document'
        verbose_name_plural = 'documents'

    def __str__(self):
        return self.document_name
    
    def __repr__(self):
        return f"DocumentModel(id={self.id}, document_name={self.document_name}, weight={self.weight}, for_workshop={self.for_workshop}, for_simulation={self.for_simulation}, topic_id={self.topic_id}, created_at={self.created_at})"
