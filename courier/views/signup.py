import transaction
from pyramid.view import view_config, render_view_to_response
from pyramid.httpexceptions import HTTPFound
from courier.keygen import KeyGen
from courier.validation import Validation
from courier.models import DBSession
from courier.models.account import Account
from courier.models.enums import AccountType
from courier.models.person import Person

@view_config(route_name='signup')
def signup(request):

    # TODO: figure out the right way to determine where the user is coming from
    # determine where user came from
    from_index = ('username' not in request.POST)
    from_agrement = request.POST.get('chkAgree','') == 'yes'

    if from_agrement:
        # redirect to the login form
        username = request.POST['username']
        login = request.route_url('login')
        login = '%s?username=%s' % (login, username)
        return HTTPFound(location=login)

    # get posted values and validate
    context = get_fields(request)
    if not from_index:
        context = validate_fields(context)
    valid = context['valid']

    # render the appropriate view
    if from_index or not valid:
        return render_view_to_response(context, request, name='signup-form')
    else:

        # create account
        first_name = context['first_name'].value
        last_name = context['last_name'].value
        username = context['username'].value
        display_name = '%s %s' % (first_name, last_name)
        password = context['password'].value
        recovery_key = KeyGen.generate_recovery_key()
        acct = Account(AccountType.Person, username, password, recovery_key)
        email_address = None
        mobile_phone = None

        # create person
        person = Person(first_name, last_name, email_address, mobile_phone, acct)

        # persist
        DBSession.add(person)
        transaction.commit()

        # TODO: create a pending flag to identify unconfirmed accounts

        context = {'recovery_key': recovery_key,
                   'username': username,
                   'display_name': display_name}

        return render_view_to_response(context, request, name='signup-complete')

@view_config(name='signup-form', renderer='../templates/signup-form.pt')
def signup_form(context, request):
    return context

@view_config(name='signup-complete', renderer='../templates/signup-complete.pt')
def signup_complete(context, request):
    return context

def get_fields(request):

    # get values
    get = lambda x: Validation(request.POST.get(x,'').strip())
    first_name = get('first_name')
    last_name = get('last_name')
    username = get('username')
    password = get('password')
    pconfirm = get('pconfirm')

    return {'first_name':first_name,
            'last_name':last_name,
            'username':username,
            'password':password,
            'pconfirm':pconfirm,
            'valid':True}

def validate_fields(context):

    valid = True
    first_name = context['first_name']
    last_name = context['last_name']
    username = context['username']
    password = context['password']
    pconfirm = context['pconfirm']

    # validate first name
    if not len(first_name.value):
        valid = False
        first_name.valid = False
        first_name.comment = 'Required'

    # validate last name
    if not len(last_name.value):
        valid = False
        last_name.valid = False
        last_name.comment = 'Required'

    # validate username (length >= 2; value unique)
    if not len(username.value):
        valid = False
        username.valid = False
        username.comment = 'Required'
    else:
        existing = DBSession.query(Account).filter(Account.username == username.value).count()
        # if username not unique
        if existing > 0:
            valid = False
            username.valid = False
            username.comment = 'Username exists'

    # validate password (length >= 8)
    if not len(password.value):
        valid = False
        password.valid = False
        password.comment = 'Required'
    elif not len(password.value) >= 8:
        valid = False
        password.valid = False
        password.comment = '8 characters required'

    # validate confirm (equal to password)
    if pconfirm.value != password.value:
        valid = False
        pconfirm.valid = False
        pconfirm.comment = 'Must match password'

    # TODO: apply validation comments to signup-form.pt

    return {'first_name':first_name,
            'last_name':last_name,
            'username':username,
            'password':password,
            'pconfirm':pconfirm,
            'valid':valid}