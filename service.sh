#!/bin/sh
EXPOSE_PORT=8000

python3 manage.py runserver 0.0.0.0:$EXPOSE_PORT 
