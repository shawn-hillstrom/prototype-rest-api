# import Flask and associated dependencies
import flask
from flask import request, jsonify, g, abort
import sqlite3

# Create the app
app = flask.Flask(__name__)

def dictFactory(cursor, row):
	''' Factory for sqlite3 connection to convert query results into dictionaries
	:param cursor: defined in sqlite3 row_factory
	:param row: defined in sqlite3 row_factory
	:return: dictionary representing a query row
	'''
	mydict = {}
	for i, c in enumerate(cursor.description):
		mydict[c[0]] = row[i]
	return mydict

def get_db():
	''' Generate a temporary Flask database
	:return: Database stored in g
	'''
	if 'db' not in g:
		g.db = sqlite3.connect(app.config['DATABASE'])
		g.db.row_factory = dictFactory
	return g.db

@app.teardown_appcontext
def close_db(e):
	''' Close the Flask database once the appcontext goes into teardown
	:param e: optional exception
	'''
	db = g.pop('db', None)
	if db is not None:
		db.close()

def init_db():
	''' Initialize the Flask database using a hard-coded shcema file '''
	db = get_db()
	with app.open_resource('testdb.sql') as schema:
		db.executescript(schema.read().decode('utf8'))

def queryDatabase(query, args=(), one=False):
	cur = get_db().execute(query, args)
	get_db().commit()
	qr = cur.fetchall()
	cur.close()
	return (qr[0] if qr else None) if one else qr

# Simple home page for app
@app.route('/', methods=['GET'])
def home():
	''' Route function for home page
	:return: Markup for simple HTML display, 200 on success
	'''
	return """<h1>Jetcake Interview Problem: REST API</h1>
	<p>This site is a prototype API for a community page.</p>"""

# Post questions
@app.route('/community/posts/questions', methods=['POST'])
def postQuestion():
	''' Route function for posting questions
	:return: Arguments, 200 on success, 400 on bad request, 409 on conflict
	'''
	rd = request.get_json(force=True)
	postid = rd['id'] if 'id' in rd else None
	user = rd['user'] if 'user' in rd else None
	postdate = rd['postdate'] if 'postdate' in rd else None
	content = rd['content'] if 'content' in rd else None
	if None in (postid, user, postdate, content):
		abort(400) # Bad request
	try:
		queryDatabase('INSERT INTO Questions VALUES (?, ?, ?, ?);', args=(postid, user, postdate, content))
		return rd # Success
	except:
		abort(409) # Conflict

# Get questions
@app.route('/community/posts/questions', methods=['GET'])
def getQuestion():
	''' Route function for getting questions
	:return: result of query or 400 on bad request
	'''
	qr = queryDatabase('SELECT * FROM Questions;')
	return jsonify(qr)

# Run the app
# app.run()
