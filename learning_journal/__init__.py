from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import DBSession, Base

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    # include jinja2 templates
    config.include('pyramid_jinja2')

    # add static view for static assets
    config.add_static_view('static', 'static', cache_max_age=3600)

    # configure routes
    config.add_route('home', '/')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('action', '/journal/{action}')

    # scan for views that map to routes in project
    config.scan()

    return config.make_wsgi_app()
