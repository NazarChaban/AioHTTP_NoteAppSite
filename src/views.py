from aiohttp import web
import aiohttp_jinja2

from src.models import Note, Tag


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> web.Response:
    notes = request.app['db_session'].query(Note).all()
    return {'notes': notes}


@aiohttp_jinja2.template('tag.html')
async def tag(request: web.Request) -> web.Response:
    return {}


async def create_tag(request: web.Request) -> web.Response:
    data = await request.post()
    name = data['name']
    session = request.app['db_session']
    tag = session.query(Tag).filter(Tag.name == name).first()
    if tag is None:
        tag = Tag(name=name)
        request.app['db_session'].add(tag)
        request.app['db_session'].commit()
    return web.HTTPFound(location=request.app.router['index'].url_for())


@aiohttp_jinja2.template('note.html')
async def note(request: web.Request) -> web.Response:
    tags = request.app['db_session'].query(Tag).all()
    return {'tags': tags}


async def create_note(request: web.Request) -> web.Response:
    data = await request.post()
    tags = data.getall('tags')
    tags_obj = []
    for tag in tags:
        tags_obj.append(
            request.app['db_session'].query(
                Tag
            ).filter(Tag.name == tag).first()
        )
    note = Note(
        name=data["name"], description=data["description"], tags=tags_obj
    )
    request.app['db_session'].add(note)
    request.app['db_session'].commit()
    return web.HTTPFound(location=request.app.router['index'].url_for())


@aiohttp_jinja2.template('detail.html')
async def detail(request: web.Request) -> web.Response:
    note_id = request.match_info.get('note_id')
    note = request.app[
        'db_session'
    ].query(Note).filter(Note.id == note_id).first()
    if not note:
        return web.HTTPFound(location=request.app.router['index'].url_for())
    return {"note": note}


async def delete_note(request: web.Request) -> web.Response:
    note_id = request.match_info.get('note_id')
    session = request.app['db_session']
    note = session.query(Note).filter(Note.id == note_id).first()
    if note:
        session.query(Note).filter(Note.id == note_id).delete()
        session.commit()
    return web.HTTPFound(location=request.app.router['index'].url_for())


async def done_note(request: web.Request) -> web.Response:
    note_id = request.match_info.get('note_id')
    session = request.app['db_session']
    note = session.query(Note).filter(Note.id == note_id).first()
    if note:
        note.done = True
        session.commit()
    return web.HTTPFound(location=request.app.router['index'].url_for())
