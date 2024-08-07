from django.test import TestCase

from maestros_joyeros.users.models import UserModel
from maestros_joyeros.branches.models import BranchModel
from maestros_joyeros.documents.models import TopicModel, DocumentModel
from maestros_joyeros.evaluations.models import MetricModel, SimulationModel, WorkshopEvaluationModel, ScoreModel


class ModelsTestCase(TestCase):

    def setUp(self):

        self.branch = BranchModel.objects.create(
            branch_name="Sample Branch",
            state="NY"
        )

        self.user = UserModel.objects.create(
            first_name="John",
            middle_name="Doe",
            last_name="Smith",
            username="johnsmith",
            email="johnsmith@example.com",
            is_staff=False,
            is_active=True,
            is_superuser=False,
            password="password123",
            branch_id=self.branch
        )
        self.user.set_password('password123')
        self.user.save()

        self.topic = TopicModel.objects.create(
            topic_name="Sample Topic"
        )

        self.metric = MetricModel.objects.create(
            metric_name="Sample Metric"
        )

        self.simulation = SimulationModel.objects.create(
            average=8,
            user_id=self.user,
            conversation="Sample conversation",
        )

        self.workshop_evaluation = WorkshopEvaluationModel.objects.create(
            average=9,
            topic_id=self.topic,
            user_id=self.user
        )

        self.document = DocumentModel.objects.create(
            document_name="Sample Document",
            content="Sample content",
            weight=5,
            for_workshop=True,
            for_simulation=False,
            topic_id=self.topic
        )

        self.score = ScoreModel.objects.create(
            simulation_id=self.simulation,
            metric_id=self.metric,
            score=9
        )

    def test_user_creation(self):

        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.username, "johnsmith")

    def test_topic_creation(self):

        self.assertEqual(self.topic.topic_name, "Sample Topic")

    def test_metric_creation(self):

        self.assertEqual(self.metric.metric_name, "Sample Metric")

    def test_simulation_creation(self):

        self.assertEqual(self.simulation.average, 8)
        self.assertEqual(self.simulation.conversation, "Sample conversation")
        self.assertEqual(self.simulation.user_id, self.user)

    def test_workshop_evaluation_creation(self):

        self.assertEqual(self.workshop_evaluation.average, 9)
        self.assertEqual(self.workshop_evaluation.topic_id, self.topic)
        self.assertEqual(self.workshop_evaluation.user_id, self.user)

    def test_score_creation(self):

        self.assertEqual(self.score.simulation_id, self.simulation)
        self.assertEqual(self.score.metric_id, self.metric)
        self.assertEqual(self.score.score, 9)
