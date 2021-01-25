#!/bin/sh

printf "postgres running check "

until pg_isready -h production-db >/dev/null 2>&1; do  
  printf "."
  sleep 3
done

export AWS_DEFAULT_REGION=ap-northeast-2

# python3 /logic/manage.py migrate --settings=config.environments.production
# python3 /logic/manage.py compilescss --settings=config.environments.production
# python3 /logic/manage.py collectstatic --no-input --ignore=*.sass --settings=config.environments.production
# python3 /logic/manage.py compilescss --delete-files --settings=config.environments.production

supervisord
