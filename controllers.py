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
        redirect(URL('groups_view'))

    return dict(
        email = get_user_email()
    )

@action('organizations/<group_id>')
@action.uses(db, auth, url_signer.verify(), 'organizations_view.html')
def org_view(group_id=None):
    if get_user_email() == None:
        redirect(URL('index'))

    return dict(
        # COMPLETE: return here any signed URLs you need.
        load_orgs_url          = URL('load_orgs', signer=url_signer),
        add_org_url            = URL('add_org', signer=url_signer),
        delete_org_url         = URL('delete_org', signer=url_signer),
        edit_org_url           = URL('edit_org', signer=url_signer),
        
        load_allocations_url   = URL('load_allocations', signer=url_signer),
        submit_allocations_url = URL('submit_allocations', signer=url_signer),
        add_allocation_url     = URL('add_allocation', signer=url_signer),
        remove_allocation_url  = URL('remove_allocation', signer=url_signer),
        email                  = get_user_email(),
        group_id               = group_id
        # This is probably not a secure way to pass the group ID because it the
        # user could modify it in the developer tools but I don't have time to
        # think about that right now...
        #
        # Future me... Is there a way to deal with this? Maybe a hashed id, that
        # can be decoded in the controller?
    )

@action('groups_view')
@action.uses(db, auth, 'groups_view.html')
def org_view():
    if get_user_email() == None:
        redirect(URL('index'))
    
    memberships = db(db.group_membership.users_id == get_user_id()).select().as_list()
    groups = list()
    for membership in memberships:
        group = db(db.groups.id == membership['groups_id']).select().first().as_dict()
        groups.append(group)
    
    return dict(
        # COMPLETE: return here any signed URLs you need.
        email  = get_user_email(),
        groups = groups,
        url_signer = url_signer,
    )

@action('groups_management')
@action.uses(db, auth, 'groups_management.html')
def group_view():
    if get_user_email() == None:
        redirect(URL('index'))
    
    return dict(
        email=get_user_email(),
        name=get_user_name(),

        create_group_url        = URL('create_group', signer=url_signer),
        edit_group_url          = URL('edit_group', signer=url_signer),
        load_groups_url         = URL('load_owned_groups', signer=url_signer),
        add_group_member_url    = URL('add_group_member', signer=url_signer),
        delete_group_member_url = URL('delete_group_member', signer=url_signer),
        get_group_members_url   = URL('get_group_members', signer=url_signer)
        
    )

"""
API Endpoints
"""

"""
Organizations: These endpoints deal with managing organizations
"""
@action('load_orgs')
@action.uses(db, url_signer.verify())
def load_orgs():
    
    group_id = request.params.get('group_id')

    # Fetch orgs records
    rows = db(db.organizations.org_group_id == group_id).select().as_list()

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
        org_group_id=request.json.get("group_id"),
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

"""
Allocations: These endpoints deal with managing user allocations
"""
@action('submit_allocations', method="POST")
@action.uses(db, url_signer.verify())
def submit_allocations():
    allocations = request.json
    for alloc in allocations:
        db(db.allocations.id == alloc['id']).update(amount=alloc['amount'])
        # record = db.allocations['id'][allocation['id']]
        # record.update_record(
        #     amount=allocations['amount']
        # )

        # row.update_record()
    
    return dict(allocations=allocations)

'''
Adds new allocation to the allocations table. Sets initial amount to zero
amount will be updated when the user determines how much they want to allocate
to this organization. Returns the allocations id in the database
'''
@action('add_allocation', method="POST")
@action.uses(db, url_signer.verify())
def add_allocation():
    org_id = request.json['org_id']
    group_id = request.json['group_id']

    id = db.allocations.insert(
        org_id=org_id,
        user_id=get_user_id,
        group_id=group_id,
        submitted=False,
        amount=0
    )

    return dict(id=id)

@action('update_allocation', method="POST")
@action.uses(db, url_signer.verify())
def update_allocations():
    
    pass


@action('remove_allocation', method="POST")
@action.uses(db, url_signer.verify())
def remove_allocation():
    id = request.json['id']
    assert id is not None
    db(db.allocations.id == id).delete()
    
    return "ok"

@action('load_allocations')
@action.uses(db, url_signer.verify())
def load_allocations():
    group_id = request.params['group_id']
    print(group_id)
    allocations = db((db.allocations.user_id == get_user_id()) & (db.allocations.group_id == group_id)).select().as_list()
    for allocation in allocations:
        org_id = allocation['org_id']
        org_name = db.organizations[org_id]['org_name']
        allocation['org_name'] = org_name
    return dict(
        allocations = allocations
    )

"""
Groups: These endpoints deal with managing user groups
"""
@action('create_group', method="POST")
@action.uses(db, url_signer.verify())
def add_group():
    #TODO: process input values
    name = request.json['group_name']
    desc = request.json['group_desc']
    funds = request.json['funding']


    id = db.groups.insert(
        group_name = name,
        funding = funds,
        group_desc = desc,
        process_stage = 1,
        owner = get_user_id()
    )

    db.group_membership.insert(
        groups_id = id,
        users_id = get_user_id(),
        role = "Admin"
    )

    return dict(
        id=id
    )

@action('load_groups')
@action.uses(db, url_signer.verify())
def load_groups():
    memberships = db(db.group_membership.users_id == get_user_id()).select().as_list()
    groups = list()
    for membership in memberships:
        group = db(db.groups.id == membership['groups_id']).select().first().as_dict()
        groups.append(group)
    
    return dict(
        groups=groups
    )



@action('load_owned_groups')
@action.uses(db, url_signer.verify())
def load_owned_groups():
    groups = db(db.groups.owner == get_user_id()).select().as_list()
    return dict(
        groups = groups
    )

@action('edit_group', method="POST")
@action.uses(db, url_signer.verify())
def update_group():
    id = request.json['id']
    field = request.json['field']
    value = request.json['value']
    
    assert id is not None
    db(db.groups.id == id).update(**{field: value})
    return 'ok'

@action('add_group_member', method="POST")
@action.uses(db, url_signer.verify())
def add_group_member():
    # TODO: Check email is valid and return error if not
    #       Then make sure user is made aware somehow
    group_id = request.json['group_id']
    member_email = request.json['email']
    member_role = request.json['role']
    member_user_id = db(db.auth_user.email == member_email).select().first()['id']
    member_user_name = db(db.auth_user.id == member_user_id).select().first()['first_name']

    id = db.group_membership.insert(
        groups_id = group_id,
        users_id = member_user_id,
        role = member_role
    )

    return dict(
        id = id,
        group_id = group_id,
        user_id = member_user_id,
        user_email = member_email,
        user_name = member_user_name
    )

@action('delete_group_member')
@action.uses(db, url_signer.verify())
def delete_group_member():
    id = request.params.get('id')
    assert id is not None
    
    db(db.group_membership.id == id).delete()
    
    return "ok"

@action('get_group_members', method="POST")
@action.uses(db, url_signer.verify())
def get_group_members():
    group_id = request.json['group_id']
    
    group_members = db(db.group_membership.groups_id == group_id).select().as_list()
    for member in group_members:
        member_user_id = member['users_id']
        user_email = db(db.auth_user.id == member_user_id).select().first()['email'] 
        first = db(db.auth_user.id == member_user_id).select().first()['first_name'] 
        last = db(db.auth_user.id == member_user_id).select().first()['last_name']
        user_name = first + " " + last
        
        member['user_email'] = user_email
        member['user_name'] = user_name

    return dict(
        group_members = group_members
    )
