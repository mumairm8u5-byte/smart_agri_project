import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "agri.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
