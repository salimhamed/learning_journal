from .forms import EntryCreateForm
from .models import DBSession, MyModel, Entry
from pyramid.exceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
import datetime


@view_config(route_name='home', renderer='templates/list.jinja2')
def index_page(request):
    entries = Entry.all()
    return {'entries': entries}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def blog_view(request):
    this_id = request.matchdict.get('id', -1)
    entry = Entry.by_id(this_id)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='action', match_param='action=create',
             renderer='templates/edit.jinja2')
def create(request):
    entry = Entry()
    form = EntryCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': 'create'}


@view_config(route_name='action', match_param='action=update',
             renderer='templates/edit.jinja2')
def update(request):
    this_id = request.GET['id']
    entry = Entry.by_id(this_id)
    form = EntryCreateForm(request.POST, title=entry.title, body=entry.body)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        entry.edited = datetime.datetime.utcnow()
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('detail', id=this_id))
    return {'form': form, 'action': 'update'}
