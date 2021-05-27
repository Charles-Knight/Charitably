"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)


"""
Page Endpoints
"""

"""
Index is a simple static page that asks the user to log in. If the user is already logged in then
they should be forward to the main application page
"""
@action('index')
@action.uses(db, auth, 'index.html')
def index():
    email = get_user_email()
    if email != None:
        redirect(URL('organizations'))

    return dict(
        email = get_user_email()
    )

@action('organizations')
@action.uses(db, auth, url_signer, 'organizations_view.html')
def org_view():
    if get_user_email() == None:
        redirect(URL('index'))
    
    return dict(
        # COMPLETE: return here any signed URLs you need.
        load_orgs_url   = URL('load_orgs', signer=url_signer),
        add_org_url     = URL('add_org', signer=url_signer),
        delete_org_url  = URL('delete_org', signer=url_signer),
        edit_org_url    = URL('edit_org', signer=url_signer),
        email           = get_user_email()
    )

"""
API Endpoints
"""
@action('load_orgs')
@action.uses(db, url_signer.verify())
def load_orgs():
    pass

@action('add_org')
@action.uses(db, url_signer.verify())
def add_org():
    pass

@action('delete_org')
@action.uses(db, url_signer.verify())
def delete_org():
    pass

@action('edit_org')
@action.uses(db, url_signer.verify())
def edit_org():
    pass


