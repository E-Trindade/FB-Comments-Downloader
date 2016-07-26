import datetime

import facebook

from Database import get_session
from Database.Models import *

graph = facebook.GraphAPI(access_token = '<Meu Token :)>', version = '2.4')

page_fields = ['id', 'name', 'likes', 'about', 'link']
post_fields = ['id', 'message', 'link', 'created_time', 'type', 'name', 'likes', 'from']
# user_fields = ['id', 'first_name', 'last_name', 'name', 'age_range', 'gender', 'political', 'relationship_status', 'religion', 'location', 'about']
user_fields = ['id', 'name']
comment_fields = ['id', 'parent', 'message', 'like_count', 'comment_count', 'created_time', 'from']


def format_time (time):
	created_time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+0000')
	created_time = created_time + datetime.timedelta(hours = -3)
	return created_time.strftime('%Y-%m-%d %H:%M:%S')


def get_page_object (data):
	pagina = Page(id = data['id'],
				  name = data.get('name'),
				  about = data.get('about'),
				  likes = data.get('likes'),
				  link = data.get('link'))
	return pagina


def get_post (data):
	post = Post(id = data['id'],
				page_id = data.get('from', {}).get('id'),
				message = data.get('message'),
				link = data.get('link'),
				created_time = format_time(data.get('created_time')),
				type = data.get('type'),
				name = data.get('name'),
				likes = len(data.get('likes')))
	return post


def get_user (data):
	usuario = User(id = data['id'],
				   first_name = data.get('first_name'),
				   last_name = data.get('last_name'),
				   name = data.get('name'),
				   min_age_range = data.get('age_range', {}).get('min'),
				   max_age_range = data.get('age_range', {}).get('max'),
				   gender = data.get('gender'),
				   political = data.get('political'),
				   relationship_status = data.get('relationship_status'),
				   religion = data.get('religion'),
				   location = data.get('location'),
				   about = data.get('about'))
	return usuario


def download_post (page_id, post_id):
	page_id = str(page_id)

	post_id = page_id + '_' + str(post_id)
	log('Iniciando download de post')

	session = get_session()

	if session.query(Page).filter(Page.id == page_id).one_or_none() is None:
		page_data = graph.get_object(id = page_id, fields = ','.join(page_fields))
		page = get_page_object(page_data)
		session.add(page)
		log('Página Salvo com sucesso')

	if session.query(Post).filter(Post.id == post_id).one_or_none() is None:
		post_data = graph.get_object(id = post_id, fields = ','.join(post_fields))
		post = get_post(post_data)
		session.add(post)
		log('Post Salvo Com Sucesso')

	users = set()

	comments_salvos = [comment[0] for comment in session.query(Comment.id).filter(Comment.post_id == post_id).all()]
	obj_comments = graph.get_connections(id=post_id, connection_name='comments', fields=','.join(comment_fields), limit=500)
	comments = []

	contPaginasComm = 1
	for c in obj_comments['data']:
		users.add(c.get('from', {}).get('id'))
		if c.get('id') not in comments_salvos:
			comments.append(Comment(id = c['id'],
									post_id = post_id,
									user_id = c.get('from', {}).get('id'),

									parent = c.get('parent'),
									message = c.get('message'),

									like_count = c.get('like_count'),
									comment_count = c.get('comment_count'),
									created_time = format_time(c.get('created_time'))))
		if c.get('comment_count', 0) > 0:
			obj_replies = graph.get_connections(id=c.get('id'), connection_name='comments', fields=','.join(comment_fields), limit=500)
			for c_r in obj_replies['data']:
				users.add(c_r.get('from', {}).get('id'))
				if c_r.get('id') not in comments_salvos:
					comments.append(Comment(id = c_r['id'],
											post_id = post_id,
											user_id = c_r.get('from', {}).get('id'),

											parent = c['id'],
											message = c_r.get('message'),

											like_count = c_r.get('like_count'),
											comment_count = c_r.get('comment_count'),
											created_time = format_time(c_r.get('created_time'))))
		log('Famílias de comentários salvos: ' + str(contPaginasComm))
		contPaginasComm += 1

	'''
	id = Column(String(100), primary_key = True, autoincrement = False)
	post_id = Column(String(100))
	user_id = Column(String(100))
	parent = Column(String(100))

	message = Column(String(2000))

	like_count = Column(BigInteger)
	comment_count = Column(BigInteger)

	created_time
	'''

	session.add_all(comments)
	usuarios_salvos = session.query(User.id).all()
	users = [get_user(graph.get_object(id = u_id, fields=','.join(user_fields))) for u_id in users if u_id not in usuarios_salvos]
	session.add_all(users)

	log('Finalizando')
	log(str(len(comments)) + ' comentários Baixados ')
	log(str(len(users)) + ' Usuários Baixados ')

	session.commit()

	log('Post Baixado com sucesso')

def download_users(users_id):
	buff = 0
	session = get_session()
	to_add = []
	for id_ in users_id:
		log('Adicionando Usuario ' + str(id_))
		try:
			json = graph.get_object(id = id_, fields=','.join(user_fields))
			new_user = get_user(json)
			to_add.append(new_user)
		except Exception:
			log('Erro ao baixar os usuários')
			
	log('Salvando no BD')
	session.add_all(to_add)
	log('Comitando')
	session.commit()
	log('Salvo Com Sucesso')

def test():
	session = get_session()
	users = session.query(Comment.user_id).all()
	return users

def log (s):
	print(s)