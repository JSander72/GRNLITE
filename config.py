import os

database_url = 'sqlite:///GRNLITE.db'

class DevelopmentConfig:    
    SQLALCHEMY_DATABASE_URI = database_url
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class TestingConfig:
    pass

class ProductionConfig:
    pass