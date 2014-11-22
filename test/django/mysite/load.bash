#!/bin/bash
python manage.py syncdb
python manage.py loaddata temp.json
