web: gunicorn --timeout 300 --chdir core core.wsgi --log-file -
worker: python -m celery -A core.worker worker -l INFO
postdeploy: bash bin/post_deploy
