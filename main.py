#!/usr/bin/python3
from bottle import route, run, template, debug, request
import json
import os

database = dict(posts=dict(sdf='hello'))


# /post [GET]


@route('/post/<name>')
def post(name):
    # return template('<b>Hello {{name}}</b>!', name=database['posts'][name])
    return database['posts'][name]

# /post POST


@route('/post/<name>', method='POST')
def post(name):
    body = request.forms.get('body')
    newPost = {name: body}
    return database['posts'].update(newPost)


# /post [DELETE]

@route('/post/<name>', method='DELETE')
def post(name):
    return database['posts'].pop(name)

# /debug (database)


@route('/debug')
def debug():
    return database


@route('/')
def index():
    return "Hello"


# if __name__ == __main__:
run(host='0.0.0.0', port=8081, reloader=True, debug=True)
