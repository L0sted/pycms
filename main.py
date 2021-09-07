#!/usr/bin/python3
from bottle import abort, route, run, template, debug, request
import pymongo

mongoclient = pymongo.MongoClient('localhost', 27017)
database = mongoclient['pycms']
posts = database['posts']


@route('/post/<name>')
def post(name):
    '''
    Get post
    '''
    try:
        return posts.find_one({'name':name})['text']
    except TypeError:
        return abort(404, 'No such page')


@route('/post/<name>', method='POST')
def post(name):
    '''
    Insert/Update post
    '''
    body = request.forms.get('body')
    # If post exists, update it
    if posts.find_one({'name': name}):
        newPost = {'$set': {'text': body}}
        return str(posts.update_one({'name': name}, newPost))
    # Else - create new
    else:
        newPost = {'name': name, 'text': body}
        return str(posts.insert_one(newPost).inserted_id)


@route('/post/<name>', method='DELETE')
def post(name):
    '''
    Delete post by name
    '''
    return str(posts.delete_one({'name':name}))

@route('/posts')
def all_posts():
    '''
    Returns all posts
    '''
    dict_posts = list()
    for i in posts.find():
        dict_posts.append(i)

    return str(dict_posts)


@route('/')
def index():
    try:
        return posts.find_one({'name':'/'})['text']
    except TypeError:
        return abort(404, 'No such page')


if __name__ == '__main__':
    run(host='0.0.0.0', port=8081, reloader=True, debug=True)
