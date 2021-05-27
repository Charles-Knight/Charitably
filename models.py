"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user_name():
    first_name = auth.current_user.get('first_name') if auth.current_user else None
    last_name = auth.current_user.get('last_name') if auth.current_user else None
    return first_name + " " + last_name

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
db.define_table(
    'groups',
    Field('group_name', requires=IS_NOT_EMPTY())
)

db.define_table(
    'organizations',
    Field('org_name', requires=IS_NOT_EMPTY()),
    Field('org_web'),
    Field('org_description'),
    Field('proposed_by', 'references auth_user')
)

db.commit()
