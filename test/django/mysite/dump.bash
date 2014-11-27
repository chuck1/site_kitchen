#!/bin/bash
python manage.py dumpdata kitchen > temp.json
python manage.py sqlclear kitchen | python manage.py dbshell
