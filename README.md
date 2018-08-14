# HappyPatent
![alt text](https://img.shields.io/badge/python-3.6-blue.svg)
![alt text](https://img.shields.io/badge/django-1.10-blue.svg)
![alt text](https://img.shields.io/badge/coverage-69%25-yellow.svg)
![alt text](https://img.shields.io/badge/Maintaining-False-red.svg)

## Introduction
The project is originally designed for a Taiwanese Patent and Trademark Office to manage thousands of patent and trademark applications
for many countries over the past 10+ years.
Check out [Demo](https://github.com/ktshen/happypatent#demo) to get a better understanding of every section.


## Features
- Friendly to Patent and Trademark Agency
- Automatically setup HTTPS service ([Caddy Server](https://caddyserver.com/))
- Perform full text search throughout the site ([ElasticSearch](https://elasticsearch-py.readthedocs.io/en/master/))
- Collect useful information in uploaded files, enabling users to search by key words ([Tika](https://github.com/chrismattmann/tika-python))
- Database: PostgreSQL, Redis

## Deployment & Commands
### Before running
1. Duplicate ".env.example" file and rename it to ".env". Fill out all necessary 
[fields](http://cookiecutter-django.readthedocs.io/en/latest/settings.html) in .env file.
2. Make sure that following folders are created and the user has the permission to access.
    - media/
    - static/
    - postgres_backup/
    - postgres_data/

### Deployment
-  Run
```
docker-compose build
docker-compose up
```
- Create Super User during the first deployment
```
docker exec -it <container-id-django> sh
python manage.py createsuperuser
```

### Database backup
Look up [cookiecutter backup](https://cookiecutter-django.readthedocs.io/en/latest/docker-postgres-backups.html)


### Test coverage
Before testing, you must install necessary packages (make sure that you have create a virtualenv workspace)
```
 pip install -r requirements/test.txt
```

To run the tests, check your test coverage, and generate an HTML coverage report::
```
coverage run manage.py test
coverage html
open htmlcov/index.html
```


## Demo
- Dashboard

<img width="250" border="0" alt="demo1" src="https://imgur.com/dNMk26p.png">

- Billboard

<img width="250" border="0" alt="demo1" src="https://imgur.com/psNlHYD.png">

- Application

<img width="250" border="0" alt="demo1" src="https://imgur.com/Baq45Fr.png">

- Proposal

<img width="250" border="0" alt="demo1" src="https://imgur.com/qvv0W4B.png">

- Inventor

<img width="250" border="0" alt="demo1" src="https://imgur.com/qJwhfjN.png">

- Agent

<img width="250" border="0" alt="demo1" src="https://imgur.com/mnxACDV.png">

- Profile

<img width="250" border="0" alt="demo1" src="https://imgur.com/eqcs31e.png">


## License 
Distributed under the MIT License.

Copyright (c) 2018 Kuan-Ting Shen, En-Han Chang
