from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import datetime

from collections import OrderedDict

from .models import Film, Comment

client = Client()

class GetAllFilmViewSet(TestCase):

	def test_get_all_movies_zero_films(self):
		response = client.get(reverse('api:movies-list'))
		self.assertEqual(response.data, [])

	def test_get_all_movies_one_film(self):
		Film.objects.create(title='The Film X', response='{"Title":"The Film X"}')
		response = client.get(reverse('api:movies-list'))
		self.assertEqual(response.data, [{'Title': 'The Film X'}])

	def test_get_all_movies_two_films(self):
		Film.objects.create(title='The Film X', response='{"Title":"The Film X"}')
		Film.objects.create(title='The Film Z', response='{"Title":"The Film Z"}')
		response = client.get(reverse('api:movies-list'))
		self.assertEqual(response.data, [{'Title': 'The Film X'}, {'Title': 'The Film Z'}])

class CreateNewFilmViewSet(TestCase):

	def test_create_new_movie(self):
		response = client.post(
			reverse('api:movies-list'),
			data={'title':'the'},
			content_type='application/json'
			)

		self.assertEqual(response.data, {'title': 'The Shawshank Redemption', 'response': '{"Title":"The Shawshank Redemption","Year":"1994","Rated":"R","Released":"14 Oct 1994","Runtime":"142 min","Genre":"Drama","Director":"Frank Darabont","Writer":"Stephen King (short story \\"Rita Hayworth and Shawshank Redemption\\"), Frank Darabont (screenplay)","Actors":"Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler","Plot":"Chronicles the experiences of a formerly successful banker as a prisoner in the gloomy jailhouse of Shawshank after being found guilty of a crime he did not commit. The film portrays the man\'s unique way of dealing with his new, torturous life; along the way he befriends a number of fellow prisoners, most notably a wise long-term inmate named Red.","Language":"English","Country":"USA","Awards":"Nominated for 7 Oscars. Another 19 wins & 32 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"9.3/10"},{"Source":"Rotten Tomatoes","Value":"91%"},{"Source":"Metacritic","Value":"80/100"}],"Metascore":"80","imdbRating":"9.3","imdbVotes":"2,084,570","imdbID":"tt0111161","Type":"movie","DVD":"27 Jan 1998","BoxOffice":"N/A","Production":"Columbia Pictures","Website":"N/A","Response":"True"}', 'comment_set': []})

class GetAllCommentViewSet(TestCase):

	def test_get_all_comments_zero_comments(self):
		Film.objects.create(title='The Film X', response='{"Title":"The Film X"}')
		response = client.get(reverse('api:comments-list'))
		self.assertEqual(response.data, [])

	def test_get_all_comments_one_comment(self):
		Film.objects.create(title='The Film X', response='{"Title":"The Film X"}')
		film = Film.objects.all().first()
		Comment.objects.create(film=film, comment='Awesome!', added=datetime.now())
		response = client.get(reverse('api:comments-list'))
		self.assertEqual(response.data, [OrderedDict([('film', 1), ('comment', 'Awesome!')])])

	def test_get_all_comments_two_comments(self):
		Film.objects.create(title='The Film X', response='{"Title":"The Film X"}')
		film = Film.objects.all().first()
		Comment.objects.create(film=film, comment='Awesome!', added=datetime.now())
		Comment.objects.create(film=film, comment='Astonishing!', added=datetime.now())
		response = client.get(reverse('api:comments-list'))
		self.assertEqual(response.data, [OrderedDict([('film', 1), ('comment', 'Awesome!')]), OrderedDict([('film', 1), ('comment', 'Astonishing!')])])

class GetAllTopViewSet(TestCase):

	def test_get_all_top(self):
		Film.objects.create(title='The Film A', response='{"Title":"The Film A"}')
		Film.objects.create(title='The Film B', response='{"Title":"The Film B"}')

		first_film, second_film = Film.objects.all()

		Comment.objects.create(film=first_film, comment='Awesome!', added=datetime.now())

		Comment.objects.create(film=second_film, comment='Not bad :)', added=datetime.now())
		Comment.objects.create(film=second_film, comment='Astonishing!', added=datetime.now())

		response = client.get(reverse('api:top-list'))

		self.assertEqual(response.data, [{'movie_id': 2, 'total_comments': 2, 'rank': 1}, {'movie_id': 1, 'total_comments': 1, 'rank': 2}])


	def test_get_all_top_the_same_in_rank(self):
		Film.objects.create(title='The Film A', response='{"Title":"The Film A"}')
		Film.objects.create(title='The Film B', response='{"Title":"The Film B"}')

		first_film, second_film = Film.objects.all()

		Comment.objects.create(film=first_film, comment='Awesome!', added=datetime.now())
		Comment.objects.create(film=first_film, comment='Nice...', added=datetime.now())

		Comment.objects.create(film=second_film, comment='Not bad :)', added=datetime.now())
		Comment.objects.create(film=second_film, comment='Astonishing!', added=datetime.now())

		response = client.get(reverse('api:top-list'))

		self.assertEqual(response.data, [{'movie_id': 1, 'total_comments': 2, 'rank': 1}, {'movie_id': 2, 'total_comments': 2, 'rank': 1}])
