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
from .models import get_user_email, get_user_id, get_user_name

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
    # Fetch orgs records
    rows = db(db.organizations).select().as_list()

    for row in rows:
        # Add name of proposer
        proposer_id = row['proposed_by']
        user_record = db(db.auth_user.id == proposer_id).select().first()
        name = user_record['first_name'] + ' ' + user_record['last_name']
        row['proposed_by'] = name

        # Add Deleteable flag
        if proposer_id == get_user_id():
            row['deleteable'] = True
        else:
            row['deleteable'] = False
    
    return dict(
        orgs=rows
    )

@action('add_org', method="POST")
@action.uses(db, url_signer.verify())
def add_org():

    id = db.organizations.insert(
        org_name=request.json.get("name"),
        org_web=request.json.get("web"),
        org_description=request.json.get("description"),
        proposed_by=get_user_id()
    )
    
    return dict(
        id=id,
        name=get_user_name()
    )

@action('delete_org')
@action.uses(db, url_signer.verify())
def delete_org():
    id = request.params.get('id')
    assert id is not None
    db(db.organizations.id == id).delete()
    
    return "ok"

@action('edit_org')
@action.uses(db, url_signer.verify())
def edit_org():
    pass


