from pyramid.view import view_config

@view_config(route_name='message', renderer='../templates/message.pt')
def message(request):
    return {}