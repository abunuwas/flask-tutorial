#!/bin/bash

/home/osboxes/Projects/flaskMegaTutorial/venv/bin/gunicorn --workers 3 --pid /run/flaskMegaTutorial/pid wsgi:app &>log/app.log

