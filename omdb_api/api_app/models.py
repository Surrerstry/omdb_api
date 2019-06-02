from django.db import models
from django.utils import timezone


class Film(models.Model):
	title = models.TextField()
	response = models.TextField()

	def __str__(self):
		return f'{self.id}.{self.title}'


class Comment(models.Model):
	film = models.ForeignKey(Film, on_delete=models.CASCADE)
	comment = models.TextField()
	added = models.DateTimeField(auto_now_add=True)