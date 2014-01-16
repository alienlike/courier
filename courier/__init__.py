from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config
from .models import DBSession

def get_groups(username, request):
    return []

def main(global_config, **settings):

    # configure sqlalchemy session
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    # create policies
    authn_policy = AuthTktAuthenticationPolicy(
        'seekrit',
        callback=get_groups # should return a list of principals, if any
    )
    authz_policy = ACLAuthorizationPolicy()

    # create Configurator instance
    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy
    )

    # static views
    config.add_static_view('css', 'templates/css', cache_max_age=3600)
    config.add_static_view('img', 'templates/img', cache_max_age=3600)
    config.add_static_view('js', 'templates/js', cache_max_age=3600)

    # page routes
    config.add_route('index', '/')
    config.add_route('inbox', '/inbox')
    config.add_route('compose', '/compose')
    config.add_route('message', '/message')
    config.add_route('signup', '/signup')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # discover views decorated with @view_config
    config.scan()

    # return a Pyramid WSGI application
    return config.make_wsgi_app()
