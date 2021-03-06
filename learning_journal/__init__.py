from .models import DBSession, Base
from .security import EntryFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import os


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    secret = os.environ.get('AUTH_SECRET', 'somesecret')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy(secret),
        authorization_policy=ACLAuthorizationPolicy(),
        default_permission='view'
    )

    # include jinja2 templates
    config.include('pyramid_jinja2')

    # add static view for static assets
    config.add_static_view('static', 'static', cache_max_age=3600)

    # configure routes
    config.add_route('home', '/', factory=EntryFactory)
    config.add_route('detail', '/journal/{id:\d+}', factory=EntryFactory)
    config.add_route('action', '/journal/{action}', factory=EntryFactory)
    config.add_route('auth', '/sign/{action}', factory=EntryFactory)

    # scan for views that map to routes in project
    config.scan()

    return config.make_wsgi_app()
