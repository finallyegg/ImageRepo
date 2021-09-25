from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgresql://decidio:6N1L1#b1PvmM@localhost:5432/quest'
    JWT_SECRET_KEY = 'super-secret'  # Change this for production
    JWT_EXPIRATION_DELTA = timedelta(seconds=30000)
    HOSTNAME = 'localhost:5666'
    HTTP_PROTOCOL = 'http'
    BLOB_URI = 'blobs/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    LRU_CACHE_SIZE = 50
    PORT = 5666


class DevelopmentConfig(Config):
    DEBUG = True
    OUTPUT_URI = 'outputs/'
