#!/usr/bin/python3
from bottle import abort, route, run, request
import pymongo


class Config:
    """
    posts - public, posts table from MongoClient
    config: private, config for DB
        config.db.host
        config.db.port
        config.db.dbname
    """
    def __init__(self):
        """
        Init init
        """
        mongoclient = pymongo.MongoClient('localhost', 27017)
        database = mongoclient['pycms']
        posts = database['posts']
        self.posts = posts

    def readConfig():
        """
        Read config file, if not exists - call Init.createConfig()
        """
        pass

    def createConfig():
        """
        Create config file
        """
        pass


class Back():
    """
    All actions that will be triggered by http
    """
    def getRootPost(self):
        try:
            return posts.find_one({'name': '_root_'})['text']
        except TypeError:
            return abort(404, 'No such page')

    def getPost(self, name):
        try:
            return posts.find_one({'name': name})['text']
        except TypeError:
            return abort(404, 'No such page')

    def getAllPosts(self):
        dict_posts = list()
        for i in posts.find():
            dict_posts.append(i)
        return str(dict_posts)

    def updatePost(self, name, body):
        # If post exists, update it
        if posts.find_one({'name': name}):
            newPost = {'$set': {'text': body}}
            return str(posts.update_one({'name': name}, newPost))
        # Else - create new
        else:
            newPost = {'name': name, 'text': body}
            return str(posts.insert_one(newPost).inserted_id)

    def deletePost(self, name):
        return posts.delete_one({'name': name})


@route('/post/<name>')
def post(name):
    '''
    Get post
    '''
    return str(back.getPost(name))


@route('/post/<name>', method='POST')
def postUpd(name):
    '''
    Insert/Update post
    '''
    body = request.forms.get('body')
    return back.updatePost(name=name, body=body)


@route('/post/<name>', method='DELETE')
def postDel(name):
    '''
    Delete post by name
    '''
    # return str(posts.delete_one({'name':name}))
    return str(back.deletePost(name))


@route('/post')
def all_posts():
    '''
    Returns all posts
    '''
    return back.getAllPosts()


@route('/')
def index():
    return back.getRootPost()


if __name__ == '__main__':
    cfg = Config()
    back = Back()
    posts = cfg.posts
    run(host='0.0.0.0', port=8081, reloader=True, debug=True)
