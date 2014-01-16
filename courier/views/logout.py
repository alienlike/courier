from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget

@view_config(route_name='logout')
def logout(request):
    # forget user and send to the index
    headers = forget(request)
    index = request.route_url('index')
    return HTTPFound(location=index, headers=headers)