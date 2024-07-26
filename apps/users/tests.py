from django.test import TestCase
from .models import UserModel, EvaluationModel, MetricModel, ScoreModel
from apps.documents.models import TopicModel, DocumentModel
from apps.branches.models import BranchModel


class RecommenderTests(TestCase):


    def setUp(self):

        self.topics = TopicModel.objects.all()
        self.branch = BranchModel.objects.create(branch_name='Branch 1', state='sdsd')
        self.user = UserModel.objects.create(username='John', name='John', middle_name='Doe', last_name='Smith', email='john@gmail.com', branch_id=self.branch)


    def test(self):

        metrics = (
            '4Cs', 'Ortografía', 'Redacción', 'Promueve la acción',
            'No forzado', 'Sinceridad', 'Empatía', 'Iniciativa',
            'Seguimiento', 'Cierre de conversación',
        )

        for i in metrics:
            MetricModel.objects.create(metric_name=i)

        new_metrics = MetricModel.objects.all()

        scores = (1, 1, 1, 2, 2, 2, 3, 3, 3, 3)
        evaluation = EvaluationModel.objects.create(average=sum(scores)/len(scores), topic_id=self.topics[0])

        for i, j in zip(new_metrics, scores):
            ScoreModel.objects.create(metric_id=i, user_id=self.user, evaluation_id=evaluation, score=j)
        print()
        print(evaluation.average)

        scores = (2, 1, 2, 2, 3, 3, 3, 1, 1, 1)
        evaluation = EvaluationModel.objects.create(average=sum(scores)/len(scores), topic_id=self.topics[1])

        for i, j in zip(new_metrics, scores):
            ScoreModel.objects.create(metric_id=i, user_id=self.user, evaluation_id=evaluation, score=j)

        print()
        print(evaluation.average)

        from django.db.models import Count, F, Min

        subquery = ScoreModel.objects.filter(user_id=self.user.id).select_related('evaluation_id')
        subquery2 = subquery.values('evaluation_id').annotate(average=F('evaluation_id__average'), topic=F('evaluation_id__topic_id')).distinct()

        sub = subquery2.aggregate(min_score=Min('score'))
        
        documents = DocumentModel.objects.filter(for_mystery_shopping=True).select_related('topic_id')

        print(len(documents))

        print(DocumentModel.objects.filter(id__gt=10).select_related('topic_id').update(for_mystery_shopping=False))

        documents = DocumentModel.objects.filter(for_mystery_shopping=False).select_related('topic_id')
        print(TopicModel.objects.exclude(id__in=[i['id'] for i in documents.values('id')]))

        #strong_points_subquery = StrongPointModel.objects.filter(user_id=self.user.id).select_related('topic_id')
        #topics_with_counts = strong_points_subquery.values('topic_id').annotate(topic_name=F('topic_id__topic_name'), strong_point_count=Count('topic_id')).values('topic_id', 'topic_name', 'strong_point_count')

        #lower_strong_point_topic = topics_with_counts.order_by('strong_point_count').first()
        #print(lower_strong_point_topic)

        #strong_point_topic_ids = [strong_point_topic['topic_id'] for strong_point_topic in top_strong_point_topics]
        #print(topics_with_counts.order_by('strong_point_count').first())
        #print(TopicModel.objects.exclude(id__in=strong_point_topic_ids))
            #print(i.topic_id.topic_name)
                #for i in self.weak_points:
                #    print(i.topic_id.topic_name
