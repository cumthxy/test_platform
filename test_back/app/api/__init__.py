# -*- coding: utf-8 -*-
from flask import Blueprint
api = Blueprint('api', __name__)
from . import login
from . import test_api
from . import test_task


