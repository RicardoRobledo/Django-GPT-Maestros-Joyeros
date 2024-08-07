from django.test import TestCase

from maestros_joyeros.documents.models import TopicModel, DocumentModel


class DocumentTestCase(TestCase):

    def setUp(self):

        self.topic = TopicModel.objects.create(
            topic_name="Sample Topic"
        )

        self.document = DocumentModel.objects.create(
            document_name="Sample Document",
            content="Sample content",
            weight=5,
            for_workshop=True,
            for_simulation=False,
            topic_id=self.topic
        )

    def test_topic_creation(self):

        self.assertEqual(self.topic.topic_name, "Sample Topic")

    def test_document_creation(self):

        self.assertEqual(self.document.document_name, "Sample Document")
        self.assertEqual(self.document.content, "Sample content")
        self.assertEqual(self.document.weight, 5)
        self.assertEqual(self.document.for_workshop, True)
        self.assertEqual(self.document.for_simulation, False)
        self.assertEqual(self.document.topic_id, self.topic)

    def test_document_read(self):

        document = DocumentModel.objects.get(document_name="Sample Document")
        self.assertEqual(document.document_name, "Sample Document")
        self.assertEqual(document.content, "Sample content")
        self.assertEqual(document.weight, 5)
        self.assertEqual(document.for_workshop, True)
        self.assertEqual(document.for_simulation, False)
        self.assertEqual(document.topic_id, self.topic)

    def test_document_update(self):

        self.document.document_name = "Updated Document"
        self.document.content = "Updated content"
        self.document.weight = 8
        self.document.for_workshop = False
        self.document.for_simulation = True
        self.document.save()

        updated_document = DocumentModel.objects.get(id=self.document.id)

        self.assertEqual(updated_document.document_name, "Updated Document")
        self.assertEqual(updated_document.content, "Updated content")
        self.assertEqual(updated_document.weight, 8)
        self.assertEqual(updated_document.for_workshop, False)
        self.assertEqual(updated_document.for_simulation, True)
        self.assertEqual(updated_document.topic_id, self.topic)

    def test_document_delete(self):

        document_id = self.document.id
        self.document.delete()

        with self.assertRaises(DocumentModel.DoesNotExist):
            DocumentModel.objects.get(id=document_id)
