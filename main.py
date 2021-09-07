#!/usr/bin/python3
from bottle import route, run, template, debug, request
import pymongo

mongoclient = pymongo.MongoClient('localhost', 27017)
database = mongoclient['pycms']
posts = database['posts']


# /post [GET]


@route('/post/<name>')
def post(name):
    '''
    Get post
    '''
    return posts.find_one({'name':name})['text']


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
    return "Hello"


# if __name__ == __main__:
run(host='0.0.0.0', port=8081, reloader=True, debug=True)
