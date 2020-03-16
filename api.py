# import Flask and associated dependencies
import flask
from flask import request, jsonify

# Create the app
app = flask.Flask(__name__)

# Simple home page for app
@app.route('/', methods=['GET'])
def home():
	return """<h1>Jetcake Interview Problem: REST API</h1>
	<p>This site is a prototype API for a community page.</p>"""

# Run the app
# app.run()
