import hashlib

from nanohttp import json, context, HTTPFound
from restfulpy.authorization import authorize
from restfulpy.controller import ModelRestController
from restfulpy.orm import DBSession, commit
from sqlalchemy_media import store_manager

class ApplicationController(ModelRestController):
    __model__ = Application

