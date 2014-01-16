from paste.deploy.loadwsgi import appconfig
from pkg_resources import resource_filename

settings = appconfig('config:' + resource_filename(__name__, 'scripts.ini'))
