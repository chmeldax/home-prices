import os

name = os.environ.get('GUNICORN_NAME', 'server')
bind = 'unix:/app/tmp/app.sock'
workers = int(os.environ.get('GUNICORN_WORKERS', 3))
loglevel = 'info'
errorlog = '-'  # STDERR
accesslog = '-'  # STDOUT
capture_output = True
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 30))
