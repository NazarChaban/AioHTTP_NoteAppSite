from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from aiohttp import web

from src.models import Base

async def pg_context(app: web.Application):
    conf = app['config']['postgres']
    url_db = f"postgresql://{conf['user']}:{conf['password']}@{conf['host']}/{conf['database']}"
    app['engine'] = create_engine(url_db)
    DBSession = sessionmaker(bind=app['engine'])
    session = DBSession()
    app['db_session'] = session
    Base.metadata.create_all(app['engine'])
    yield
    app['db_session'].close()
