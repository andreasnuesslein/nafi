Dependencies
--------------------
* [django](https://github.com/django/django)
* [feedparser](https://code.google.com/p/feedparser)


Running the webservice
---------------------------------
1. `cd config/ && cp settings.py.example settings.py` && **customize**.
2. `./manage.py syncdb`  (if you want an admin-user for /admin, create one here.)
3. run `./manage.py runserver`
4. go to http://127.0.0.1:8000/

Using nginx as a proxy
-------------------------------
1. Do the above steps.
2. Use the example nginx config from `docs/`
