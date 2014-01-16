from pyramid.view import view_config

@view_config(route_name='compose', renderer='../templates/compose.pt')
def compose(request):
    return {}