
1.
REQUIREMENTS:

django 2.2
djangorestframework 3.9.2

--- DESCRIPTION ---

2. Some unittest are available: python3 manage.py test

3. LIST OF ENDPOINTS:

A. /movies
Get all saved movies:
[GET] - http://127.0.0.1:8000/api/1.0/movies/

You can filter by title for example(Case sensitive):
http://127.0.0.1:8000/api/1.0/movies/?title=Fast

Save new film in db
[POST] - requires mandatory 'title'(text) parameter.
http://127.0.0.1:8000/api/1.0/movies/


B. /comments
Get all comments
[GET] - http://127.0.0.1:8000/api/1.0/comments/

You can filter by id of movie:
[GET] - http://127.0.0.1:8000/api/1.0/comments/?id=28

Save new comment in db
[POST] - requires 'film'(int) and 'comment'(text) field
http://127.0.0.1:8000/api/1.0/comments/


C. /top
Get all top
[GET] - http://127.0.0.1:8000/api/1.0/top/

You can filter by comments based on time by passing timestamp as begin and end scope
[GET] - http://127.0.0.1:8000/api/1.0/top/?begin_scope=1&end_scope=123

