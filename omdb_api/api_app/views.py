from django.shortcuts import render
from django.http import Http404
from django.utils.timezone import datetime

from rest_framework import viewsets
from rest_framework.response import Response

from collections import OrderedDict
from requests import get

from . import models
from . import serializers

import json

from pdb import set_trace

API_KEY_POSTFIX = '&apikey=45ee94c5'
OMDB_API_URL = 'http://www.omdbapi.com/'

class FilmViewSet(viewsets.ModelViewSet):
	queryset = models.Film.objects.all()
	serializer_class = serializers.FilmSerializer

	def perform_create(self, serializer):
		film_name = self.request.data['title']
		r = get(f'{OMDB_API_URL}?t={film_name}&plot=full{API_KEY_POSTFIX}')

		if 'Error' in r.json():
			raise Http404

		serializer.save(title=r.json()['Title'], response=r.text)

	def list(self, request):
		queryset = models.Film.objects.all()
		list_of_ordered_dicts = []

		if 'title' in self.request.query_params:
			for row in queryset:
				loaded_json = json.loads(row.response)
				if self.request.query_params['title'] in loaded_json['Title']:
					list_of_ordered_dicts.append(loaded_json)
		else:
			for row in queryset:
				list_of_ordered_dicts.append(json.loads(row.response))

		return Response(list_of_ordered_dicts)


class CommentViewSet(viewsets.ModelViewSet):
	queryset = models.Comment.objects.all()
	serializer_class = serializers.CommentSerializer

	def list(self, request):
		queryset = models.Comment.objects.all()
		list_of_ordered_dicts = []

		if 'id' in self.request.query_params:
			for row in queryset:
				if self.request.query_params['id'] == str(row.film.id):
					list_of_ordered_dicts.append(serializers.CommentSerializer(row).data)
		else:
			return Response(serializers.CommentSerializer(queryset, many=True).data)

		return Response(list_of_ordered_dicts)


class TopViewSet(viewsets.ModelViewSet):
	queryset = models.Film.objects.all()
	serializer_class = serializers.FilmSerializer

	def list(self, request):
		queryset = models.Film.objects.all()
		movies_with_amount_of_comment = []
		for row in queryset:
			comments_amount = len(row.comment_set.filter(
				added__gte=datetime.fromtimestamp(int(request.query_params['begin_scope']) if 'begin_scope' in request.query_params else 0), 
				added__lte=datetime.fromtimestamp(int(request.query_params['end_scope']) if 'end_scope' in request.query_params else 2147483647)
				)
			)
			movies_with_amount_of_comment.append({'movie_id':row.id, 'total_comments':comments_amount})

		movies_with_amount_of_comment.sort(key=lambda k: k['total_comments'], reverse=True)

		previous_total_comment = None
		pos = 0
		for movie in movies_with_amount_of_comment:
			pos += 1
			if previous_total_comment != None and movie['total_comments'] == previous_total_comment:
				pos -= 1
			movie['rank'] = pos
			previous_total_comment = movie['total_comments']

		return Response(movies_with_amount_of_comment)
