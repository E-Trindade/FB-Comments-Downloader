from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None
def get_engine():
	global engine
	if engine is None:
		engine = create_engine('mssql+pymssql://sa:123456@localhost/RP_1?charset=utf8', echo=False)
		# engine = create_engine('postgresql+psycopg2://postgres:1@localhost:5432/RP_1', echo=True)
	return engine

Session = sessionmaker(bind=get_engine())

def get_session():
	return Session(autoflush=True)