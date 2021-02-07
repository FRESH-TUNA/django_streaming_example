#!/bin/sh

printf "postgres running check "

# until pg_isready -h production-db >/dev/null 2>&1; do  
#   printf "."
#   sleep 3
# done

# python3 manage.py migrate --settings=config.environments.production
# python3 manage.py compilescss --settings=config.environments.production
# python3 manage.py collectstatic --no-input --ignore=*.sass --settings=config.environments.production
# python3 manage.py compilescss --delete-files --settings=config.environments.production

supervisord
