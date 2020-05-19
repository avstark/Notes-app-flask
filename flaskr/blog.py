import functools

from flask import (Blueprint, g, flash, redirect, render_template, request, session, url_for)

from flaskr.db import get_db

from flaskr.auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash

bp= Blueprint('blog', __name__ )

@bp.route('/')
def index():
	db= get_db()

	posts = db.execute(
		'SELECT p.id, title, body, created, author_id, username'
		' FROM post p JOIN user u ON p.author_id = u.id'
		' ORDER BY created DESC'
	).fetchall()

	# p_tuple= db.execute(
	# 	'SELECT * FROM post ORDER BY created DESCN').fetchall()
	# posts= []
	# for p in p_tuple:
	# 	post= {
	# 		'id' 		: 	p[0]
	# 		'title' 	:	p[3]
	# 		'body'		:	p[4]
	# 		'author_id'	:	p[1]	
	# 		'created'	:	p[2]
	# 	}
	# 	posts.append(post)

	return render_template('blog/index.html', posts= posts)

