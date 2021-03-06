# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os
basedir = os.path.abspath(os.path.dirname(__file__))


mail_formatter = logging.Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s
    Thread ID:          %(thread)d

    Message:

    %(message)s
    ''')

file_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(threadName)s:%(pathname)s:%(lineno)d]')


class BaseConfig(object):
    """Base Configuration"""
    LOGGER_STREAM = True
    SEND_FILE_MAX_AGE_DEFAULT = 600
    HOMEDIR = os.environ.get('HOME', basedir)
    ROOT = basedir
    EMAILS = os.path.join(HOMEDIR, 'emails.txt')
    MONGO_URI = 'mongodb://localhost'
    MONGO_DATABASE = 'test_db'
    MONGO_COLLECTION_PREFIX = 'test_flask_blog_'
    WTF_CSRF_ENABLED = True
    DEBUG = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MAIL_DEBUG = False


class DevelopmentConfig(BaseConfig):
    """ Development configuration """
    DEBUG = True
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    ROOT = os.path.abspath(os.path.join(basedir, '..', '..'))
    _tmpdir = os.path.join(ROOT, '.tmp')
    _db = os.path.join(_tmpdir, 'dev.sqlite')
    EMAILS = os.path.join(_tmpdir, 'emails.txt')
    LOGGER_FILE = True
    FLASK_BLOG_DIR = os.path.join(basedir, '..', 'test_blogs')


class TestConfig(BaseConfig):
    """ Test configuration """
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False
    DEBUG = True
    CANONICAL_SERVER = 'https://canonical.example.com'
    import tempfile
    MONGO_URI = 'mongodb://localhost:27027'
    HOMEDIR = tempfile.mkdtemp('flask_blog_test')
    EMAILS = os.path.join(HOMEDIR, 'emails.txt')
    MAIL_DEBUG = True
    TESTING = True
    SERVER_NAME = 'localhost'
    FLASK_BLOG_DIR = os.path.join(basedir, '..', 'test_blogs')


def configure_logger(app):
    if app.config.get('LOGGER_STREAM', False):
        handler1 = logging.StreamHandler()
        handler1.setLevel(logging.DEBUG)
        app.logger.addHandler(handler1)

    if app.config.get('LOGGER_MAIL', False):
        config = {
            'toaddrs': (
                app.config.get('LOGGER_MAIL_ADMINS', ['mail@example.com'])),
            'fromaddr': app.config.get('LOGGER_MAIL_FROM', 'mail@example.com'),
            'subject': app.config.get(
                'LOGGER_MAIL_SUBJECT', '[{} Error]'.format(__name__.upper())),
            'mailhost': (
                app.config.get('MAIL_SERVER', 'localhost'),
                app.config.get('MAIL_PORT', 25))
        }
        if 'MAIL_PASSWORD' in app.config:
            config['credentials'] = (
                app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        if (app.config.get('MAIL_USE_SSL', False)
                or app.config.get('MAIL_USE_TLS', False)):

            config['secure'] = ()
        try:
            handler2 = logging.handlers.SMTPHandler(**config)
            handler2.setFormatter(mail_formatter)
            handler2.setLevel(logging.WARNING)
            app.logger.addHandler(handler2)
        except Exception as e:
            msg = (
                'Could not enable a connection with the STMPHandler:\n{}'
                .format(e))
            print(msg)
            raise RuntimeError(msg)

    if app.config.get('LOGGER_FILE', False):
        filename = app.config.get(
            'LOGGER_FILENAME', os.path.join(basedir, 'flask_blog.logs'))
        handler3 = logging.FileHandler(filename)
        handler3.setFormatter(file_formatter)
        handler3.setLevel(logging.INFO)
        app.logger.addHandler(handler3)

    app.logger.setLevel(logging.DEBUG)

    if app.config.get('TEST_LOGGER_ON_STARTUP', True):
        app.logger.warn(
            'This is just a test message to check that your loggers log as '
            'expected.')


def configure_app(app):
    if os.getenv('FLASK_BLOG_TESTING', False):
        cobj = TestConfig
    elif os.path.basename(
            os.getenv('FLASK_BLOG_SETTINGS', '')).endswith('empty.py'):
        cobj = DevelopmentConfig
    else:
        cobj = BaseConfig

    app.config.from_object(cobj)
    app.config.from_envvar('FLASK_BLOG_SETTINGS')

# vim:set ft=python sw=4 et spell spelllang=en:
