from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from courier.models.account import Account
from courier.models import DBSession

@view_config(route_name='login', renderer='../templates/login.pt')
def login(request):

    # if form was submitted
    if 'username' in request.POST:

        # authenticate the user
        username = request.POST['username']
        password = request.POST['password']
        acct = DBSession.query(Account).filter(Account.username==username).one()
        if acct is None:
            valid = False
        else:
            valid = acct.validate_password(password)

        if valid:
            # remember user and send to the inbox
            headers = remember(request, username)
            inbox = request.route_url('inbox')
            return HTTPFound(location=inbox, headers=headers)
        else:
            # denied; back to login form to try again
            return {'valid': valid,
                    'username': username,
                    'password': password}

    elif 'username' in request.GET:
        # show login form with username pre-entered
        username = request.GET['username']
        return {'valid': True,
                'username': username,
                'password': None}

    else:
        # show blank login form
        return {'valid': True,
                'username': None,
                'password': None}