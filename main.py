#!/usr/bin/python3
from bottle import abort, route, run, request
import pymongo
import time
# TODO: auth to /admin
# TODO: timestamps to posts
# TODO: author to posts and multiple users
# TODO: add bottle's params to config


class Config:
    """
    posts - table with posts
    config structure:
        DB:
            - host
            - port
            - dbname
    """
    def __init__(self):
        """
        Init config
        """
        self.readConfig()

        mongoclient = pymongo.MongoClient(self.host, self.port)
        if self.dbname not in mongoclient.list_database_names():
            print('DB not found, creating')
        database = mongoclient[self.dbname]

        # TODO: Create table if not exists
        if 'posts' not in database.list_collection_names():
            print('Table not fount, creating')
        posts = database['posts']
        self.posts = posts

    def readConfig(self):
        """
        Read config file, if not exists - call self.createConfig()
        """
        # TODO: Досоздавать недостающие ключи
        import configparser
        config = configparser.ConfigParser()
        if not config.read('config.ini'):
            self.createConfig(config)

        db = config['DB']
        self.host = db['host']
        self.port = int(db['port'])
        self.dbname = db['name']

        app = config['App']
        self.apphost = app['host']
        self.appport = int(app['port'])
        self.appdebug = bool(app['debug'])

    def createConfig(self, config):
        """
        Create config file
        """
        config['DB'] = {}
        db = config['DB']
        db['host'] = 'localhost'
        db['port'] = '27017'
        db['name'] = 'pycms'

        config['App'] = {}
        app = config['App']
        app['port'] = '8080'
        app['debug'] = 'True'
        app['host'] = '0.0.0.0'

        with open('config.ini', 'w') as cfgfile:
            config.write(cfgfile)


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
        # TODO: clear up output, remove '_id' and 'body',
        # now there should be only
        dict_posts = list()
        for i in posts.find():
            dict_posts.append(i)
        return str(dict_posts)

    def updatePost(self, name, body):
        # TODO: return RESTful error/success result
        # If post exists, update it
        if posts.find_one({'name': name}):
            newPost = {'$set': {'text': body}}
            return str(posts.update_one({'name': name}, newPost))
        # Else - create new
        else:
            newPost = {'name': name, 'text': body,
                       'create_timestamp': str(time.time())}
            return str(posts.insert_one(newPost).inserted_id)

    def deletePost(self, name):
        # TODO: return RESTful error/success result
        return bool(posts.delete_one({'name': name}).deleted_count)


class Metrics:
    def alive():
        return str("alive 1")


@route('/metrics')
def metrics():
    return Metrics.alive()


@route('/post/<name>')
def post(name):
    '''
    Get post
    '''
    return str(back.getPost(name))


@route('/admin/post/<name>', method='POST')
def postUpd(name):
    '''
    Insert/Update post
    '''
    body = request.forms.get('body')
    return back.updatePost(name=name, body=body)


@route('/admin/post/<name>', method='DELETE')
def postDel(name):
    '''
    Delete post by name
    '''
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
    print("Init")
    cfg = Config()
    print("Configured")
    back = Back()
    posts = cfg.posts
    run(host=cfg.apphost, port=cfg.appport, reloader=cfg.appdebug, debug=cfg.appdebug)
