from pyramid.view import view_config
from sqlalchemy.orm import aliased
from courier.block import Block
from courier.models.account_message import AccountMessage
from courier.models import DBSession
from courier.models.enums import RecipientType
from courier.models.account import Account
from courier.models.db_views import *
from courier.models.message import Message
from courier.models.tag import Tag
from courier.models.account_link import AccountLink

MIN_BLOCK_SIZE = 20
MAX_BLOCK_SIZE = 500

def get_counts(acct, curr_view):

    unread_ct = 0
    total_ct = 0

    if curr_view == 'received':

        # get unread received message count for current filter
        q = unread_recd_ct.select().where(unread_recd_ct.c.to_account_id==acct.id)
        for r in DBSession.execute(q):
            unread_ct = r[unread_recd_ct.c.ct]
            break

        # get total received message count for current filter
        q = total_recd_ct.select().where(total_recd_ct.c.to_account_id==acct.id)
        for r in DBSession.execute(q):
            total_ct = r[total_recd_ct.c.ct]
            break

    elif curr_view == 'sent':

        # get total sent message count for current filter
        q = total_sent_ct.select().where(total_sent_ct.c.from_account_id==acct.id)
        for r in DBSession.execute(q):
            total_ct = r[total_sent_ct.c.ct]
            break

    return unread_ct, total_ct

def get_account_messages(acct, curr_view, curr_index, to_index, sort_order,
                 show_archived_messages=False, show_hidden_contacts=False,
                 contact_ids=None, tag_ids=None, message_search=''):

    # get account messages for current account
    acct_messages = DBSession.query(AccountMessage).filter(AccountMessage.recipient_account==acct)

    # filter by recipient type, depending on current view
    if curr_view == 'sent':
        acct_messages = acct_messages.filter(AccountMessage.recipient_type_code==RecipientType.From)
    else:
        acct_messages = acct_messages.filter(AccountMessage.recipient_type_code!=RecipientType.From)

    # filter by archived status
    if not show_archived_messages:
        acct_messages = acct_messages.filter(AccountMessage.archived==False)

    if contact_ids or not show_hidden_contacts:

        # join contacts to account messages
        contact_message = aliased(AccountMessage)
        contact_acct = aliased(Account)
        contact_acct_link = aliased(AccountLink)
        acct_messages = acct_messages.join(AccountMessage.message)\
            .join(contact_message, Message.account_messages)\
            .join(contact_acct, contact_message.recipient_account)\
            .filter(contact_acct.id!=acct.id)

        # filter by contact ids
        if contact_ids:
            acct_messages = acct_messages.filter(contact_acct.id.in_(contact_ids))

        # filter by contact hidden status
        if not show_hidden_contacts:
            peer_acct_link = aliased(AccountLink)
            acct_messages = acct_messages.join(contact_acct_link, contact_acct.account_links)\
                .filter(contact_acct_link.to_account_id==acct.id)\
                .join(peer_acct_link, contact_acct_link.peer)\
                .filter(peer_acct_link.hidden==False)

    if tag_ids or message_search:

        # join messages to account messages
        acct_messages = acct_messages.join(AccountMessage.message)

        # filter by tag ids
        if tag_ids:
            acct_messages = acct_messages.join(Message.tags)\
                .filter(Tag.id.in_(tag_ids))

        # filter by message search
        if message_search:
            # todo: use encrypted full-text index in lieu of 'like'
            acct_messages = acct_messages.filter(Message.subject.like('%%%s%%' % message_search))

    # todo: implement sort order
    if sort_order:
        pass

    # apply offset and limit
    # todo: implement windowed range query in lieu of slice()
    # (see http://stackoverflow.com/a/7390660/204900)
    acct_messages = acct_messages.slice(curr_index, to_index)

    return acct_messages

@view_config(route_name='inbox', renderer='../templates/inbox.pt')
def inbox(request):

    # todo: get auth user from session
    AUTH_USER = 'nw'

    # get authenticated user's account
    acct = DBSession.query(Account).filter(Account.username==AUTH_USER).one()

    # get parameters from request
    contact_search = request.GET.get('contact_search', '').strip()
    tag_search = request.GET.get('tag_search', '').strip()
    message_search = request.GET.get('message_search', '').strip()
    contact_sort_order = request.GET.get('contact_sort_order', 'az')
    tag_sort_order = request.GET.get('tag_sort_order', 'az')
    message_sort_order = request.GET.get('message_sort_order', 'newest')
    selected_contacts = request.GET.get('selected_contacts', '')
    selected_tags = request.GET.get('selected_tags', '')
    selected_messages = request.GET.get('selected_messages', '')
    show_hidden_contacts = request.GET.get('show_hidden_contacts', None)
    show_archived_messages = request.GET.get('show_archived_messages', None)
    curr_list = request.GET.get('curr_list', 'contacts')
    curr_view = request.GET.get('curr_view', 'received')
    curr_index = request.GET.get('curr_index', '0')
    block_size = request.GET.get('block_size', None)

    # get counts
    unread_received, total_received = get_counts(acct, 'received')
    unread_sent, total_sent = get_counts(acct, 'sent')
    total_ct = total_sent if curr_view == 'sent' else total_received

    # get selected items
    if selected_contacts:
        selected_contacts = [int(val) for val in selected_contacts.split(',')]
    else:
        selected_contacts = []
    if selected_tags:
        selected_tags = [int(val) for val in selected_tags.split(',')]
    else:
        selected_tags = []
    if selected_messages:
        selected_messages = [int(val) for val in selected_messages.split(',')]
    else:
        selected_messages = []

    # convert t/f values to boolean
    show_hidden_contacts = show_hidden_contacts == 't'
    show_archived_messages = show_archived_messages == 't'

    # parse curr_index
    try:
        curr_index = max(int(curr_index), 0)
    except (TypeError, ValueError):
        curr_index = 0

    # parse block_size
    try:
        block_size = max(int(block_size), 0)
    except (TypeError, ValueError):
        block_size = MIN_BLOCK_SIZE

    # constrain block_size to between MIN_BLOCK_SIZE and MAX_BLOCK_SIZE
    block_size = max(min(MAX_BLOCK_SIZE, block_size), MIN_BLOCK_SIZE)

    # constrain curr_index if equal to or greater than the message count
    if curr_index >= total_ct:
        curr_index = max(total_ct - block_size, 0)

    # determine to_index
    to_index = min(curr_index + block_size, total_ct)

    # get page blocks
    blocks = Block.get_blocks(block_size, total_ct, curr_index)

    # get messages
    acct_messages = get_account_messages(acct, curr_view, curr_index, to_index,
                                         message_sort_order, show_archived_messages,
        show_hidden_contacts=show_hidden_contacts,
        contact_ids=selected_contacts, tag_ids=selected_tags, message_search=message_search)

    # get contacts and unread message count for each, according to sort
    q = unread_recd_ct_by_link.select().where(
        unread_recd_ct_by_link.c.to_account_id==acct.id
    )
    if not show_hidden_contacts:
        q = q.where(unread_recd_ct_by_link.c.hidden==False)
    contacts = DBSession.execute(q)

    # get tags and unread message count for each, according to sort
    q = unread_recd_ct_by_tag.select().where(
        unread_recd_ct_by_tag.c.to_account_id==acct.id
    )
    tags = DBSession.execute(q)

    return {
        # data
        'contacts': contacts,
        'tags': tags,
        'unread_received_ct': unread_received,
        'total_received_ct': total_received,
        'total_sent_ct': total_sent,
        'acct_messages': acct_messages,
        'blocks': blocks,
        # params
        'contact_search': contact_search,
        'tag_search': tag_search,
        'message_search': message_search,
        'contact_sort_order': contact_sort_order,
        'tag_sort_order': tag_sort_order,
        'message_sort_order': message_sort_order,
        'selected_contacts': selected_contacts,
        'selected_tags': selected_tags,
        'selected_messages': selected_messages,
        'show_hidden_contacts': show_hidden_contacts,
        'show_archived_messages': show_archived_messages,
        'curr_list': curr_list,
        'curr_view': curr_view,
        'curr_index': curr_index,
        'block_size': block_size
    }