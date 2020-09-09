command = '/home/wiki/code/project1/env/bin/gunicorn'
pythonpath = '/home/wiki/code/project1/project1'
bind = '127.0.0.1:8001'
workers = 4
user = 'wiki'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=project1.settings'

