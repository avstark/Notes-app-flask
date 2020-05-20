import functools

from flask import (Blueprint, g, flash, redirect, render_template, request, session, url_for)

from flaskr.db import get_db

from flaskr.auth import login_required

from werkzeug.exceptions import abort

bp= Blueprint('blog', __name__ )

@bp.route('/')
def index():
	db= get_db()

	p_tuple = db.execute(
		'SELECT p.id, title, body, created, author_id, username'
		' FROM post p JOIN user u ON p.author_id = u.id'
		' ORDER BY created DESC'
	).fetchall()

		
	# p_tuple= db.execute('SELECT * FROM post ORDER BY created DESC').fetchall()
	
	posts= []
	for p in p_tuple:
		post= {
			'id' 		: 	p[0],
			'title' 	:	p[1],
			'body'		:	p[2],
			'created'	:	p[3],
			'author_id'	:	p[4],
			'username'	:	p[5],	
		}
		posts.append(post)

	return render_template('blog/index.html', posts= posts)

@bp.route('/create', methods= ('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		title= 	request.form['title']
		body=	request.form['body']
		error= None

		if not title:
			error=	'Title is required.'
		elif not body:
			error= 	'Text is Required.'

		if error is None:
			db= get_db()
			db.execute(
				'INSERT INTO post (title, body, author_id)'
				'VALUES (?, ?, ?)', 
				(title, body, g.user['id'])
				)
			db.commit()
			return redirect(url_for('blog.index'))
			# return render_template('blog/index.html')

		flash(error)

	return render_template('blog/create.html')

def get_post(id, check_author= True):
	db= get_db()
	p_tuple= db.execute(
		'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
		).fetchone()

	if p_tuple is None:
		abort(404, f"Post id {id} doesn't exist.")

	if check_author and p_tuple[4] != g.user['id']:
		abort(403)
	post= {
			'id' 		: 	p_tuple[0],
			'title' 	:	p_tuple[1],
			'body'		:	p_tuple[2],
			'created'	:	p_tuple[3],
			'author_id'	:	p_tuple[4],
			'username'	:	p_tuple[5],	
		}
	return post

@bp.route('/<int:id>/update', methods= ('GET', 'POST'))
@login_required
def update(id):
	post= get_post(id)

	if request.method == 'POST':
		title= 	request.form['title']
		body=	request.form['body']
		error= None

		if not title:
			error=	'Title is required.'
		elif not body:
			error= 	'Text is Required.'

		# print(f'{title}, {id}')

		if error is None:
			db= get_db()
			db.execute(
				'UPDATE post SET title= ?, body= ?'
				'WHERE id= ?',(title, body, id)
			)
			db.commit()
			return redirect(url_for('blog.index'))

		flash(error)

	return render_template('blog/update.html', post= post)

@bp.route('/<int:id>/delete', methods= ('POST', ))
@login_required
def delete(id):
	post= get_post(id)
	error= None

	if post is None:
		error= 'cannot find this post'

	else:
		db=get_db()
		db.execute('DELETE FROM post WHERE id= ?',(id, ))
		db.commit()
		return redirect(url_for('blog.index'))

	flash(error)