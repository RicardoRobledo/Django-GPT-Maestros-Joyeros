from rest_framework import serializers

from maestros_joyeros.documents.models import DocumentModel


class DocumentSerializer(serializers.ModelSerializer):
    """
    This class serialize our Document model
    """

    class Meta:
        """
        This inner class define our fields to show and our model to use

        Attributes:
            model (DocumentModel): User instance to make reference
            field tuple(str): fields to show
        """

        model: DocumentModel = DocumentModel
        fields: tuple = ('document_name',)

    def to_representation(self, instance):
        """
        This method return us our json representation
        """

        return {
            'id': instance.id,
            'document_name': instance.document_name,
            'content': instance.content,
            'topic': instance.topic_id.topic_name,
        }
