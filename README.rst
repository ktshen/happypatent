HappyPatent
===========

The project provides a site for managing patents and cases.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
     :target: https://github.com/ktshen/happypatent

.. image:: https://img.shields.io/badge/django-1.10-blue.svg
     :target: https://www.djangoproject.com/

.. image:: https://img.shields.io/badge/coverage-69%25-yellow.svg
     :target: https://github.com/ktshen/happypatent

.. image:: https://img.shields.io/badge/Project-%20Commercial%20Use-red.svg
     :target: https://github.com/ktshen/happypatent

:DEMO: `HAPPYPATENT <https://happypatent.ddns.net/>`_


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------
Test coverage
^^^^^^^^^^^^^
Before testing, you must install necessary packages (make sure that you have create a virtualenv workspace)::

    pip install -r requirements/test.txt

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html


Deployment
----------

Please visit cookiecutter_ to set up basic needs for starting docker.

.. _cookiecutter: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html

env file
^^^^^^^^
Duplicate env.example and rename it to **.env**. Fill out all the necessary fields in .env file.

Necessary folders for docker-compose.yml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* media/
* static/
* postgres_backup/
* postgres_data/

Set up remote server git pull through local machine's ssh key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Please visit `Github SSH agent <https://developer.github.com/v3/guides/using-ssh-agent-forwarding/>`_ and follow its tutorial to set up proper configuration in order to let remote server to git pull through ssh.

* Set up ~/.ssh/config in local machine.
* Make sure that remote server's **/etc/ssh_config** has **ForwardAgent yes**.
* Make sure **ssh-add -L** has response.

Database backup
^^^^^^^^^^^^^^^
Look up `cookiecutter backup <https://cookiecutter-django.readthedocs.io/en/latest/docker-postgres-backups.html>`_.

Other Notices
^^^^^^^^^^^^^
* Make sure that **media/** has the privilege to store files.



Limitation
----------
``Commercial use. NOT OPEN SOURCE. Copyright (c) 2017, Kuanting Shen. All rights reserved.``
