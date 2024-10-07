# import os

# class Config:
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.getenv('SECRET_KEY')

# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# class ProductionConfig(Config):
#     DEBUG = False