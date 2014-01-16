import os
from pyramid.paster import get_app, setup_logging

# todo: use rel paths here
os.environ['PYTHON_EGG_CACHE'] = '/home/pyramid/courier/wsgi/python-eggs'
ini_path = '/home/pyramid/courier/production.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
