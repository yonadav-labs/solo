#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "solo.settings.prod")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

"""
can run locally by running: 
python manage.py runserver --settings=<django_project_name>.settings.dev

"""	
	
	