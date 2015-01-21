from ..models import DBSession, MyModel, Base, Entry, User
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
from cryptacular.bcrypt import BCRYPTPasswordManager as Manager
import os
import sys
import transaction


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        # create admin user
        manager = Manager()
        password = manager.encode(u'admin')

        # initalize database
        models = [
            MyModel(name='one', value=1),
            Entry(title=u'test title', body=u'this is the test body'),
            User(username=u'admin', password=password),
        ]
        DBSession.add_all(models)
