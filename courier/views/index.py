from pyramid.view import view_config

@view_config(route_name='index', renderer='../templates/index.pt')
def index(request):
    return {}