freunde is OpenSocial RESTful API test server.

::

  pip install -r requirements.txt
  cd freunde
  python manage.py syncdb
  python manage.py loaddata people
  python manage.py runserver
