#!/bin/sh
EXPOSE_PORT=8000

# for test purpose
# export AWS_ACCESS_KEY_ID=""
# export AWS_SECRET_ACCESS_KEY=""
# export AWS_DEFAULT_REGION=""

python3 manage.py runserver 0.0.0.0:$EXPOSE_PORT \
--settings=config.environments.production

# development purpose
# python3 manage.py runserver 0.0.0.0:$EXPOSE_PORT
