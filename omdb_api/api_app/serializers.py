from rest_framework import serializers

from . import models

class FilmSerializer(serializers.ModelSerializer):
	comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = models.Film
		fields = ('title', 'response', 'comment_set')
		extra_kwargs = {
			'response': {'read_only': True}
		}

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Comment
		fields = ('film', 'comment')