var ready_to_submit = false;

// refreshInbox gets the form ready for submission by
// writing some of the form state to hidden fields, then
// sets the ready_to_submit flag and submits the form.
function refreshInbox() {

    // determine selected contacts
    var contact_ids = $('.contact-pill.active').map(function() {
        return $(this).attr('id').replace('contact','');
    }).get().join(',');
    $('#selected_contacts').val(contact_ids);

    // determine selected tags
    var tag_ids = $('.tag-pill.active').map(function() {
        return $(this).attr('id').replace('tag','');
    }).get().join(',');
    $('#selected_tags').val(tag_ids);

    // determine selected messages
    var message_ids = $('.message-row.active').map(function() {
        return $(this).find('#message_id').val();
    }).get().join(',');
    $('#selected_messages').val(message_ids);

    // determine current list
    var lists = ['contacts','tags'];
    for (var i in lists) {
        var list = lists[i];
        var id = list + '_tab';
        if ($('#'+id).hasClass('active')) {
            $('#curr_list').val(list);
        }
    }

    // set flag
    ready_to_submit = true;

    // submit form
    $('form').submit();
}

// CONTACTS

function sortContacts(sortMethod) {
    if ($('#contact_sort_order').val() != sortMethod) {
        $('#contact_sort_order').val(sortMethod);
        refreshInbox();
    }
}

function toggleHiddenContacts() {
    $('#show_hidden_contacts').val(function(i,v) {
        if (v == 't') return 'f';
        else return 't';
    });
    refreshInbox();
}

// TAGS

function sortTags(sortMethod) {
    if ($('#tag_sort_order').val() != sortMethod) {
        $('#tag_sort_order').val(sortMethod);
        refreshInbox();
    }
}

// MESSAGES

function changeMessageView(view) {
    if ($('#curr_view').val() != view) {
        $('#curr_view').val(view);
        $('#curr_index').val(0);
        $('#message_search').val('');
        $('.message-row').removeClass('active');
        $('.message-row').find(':checkbox').attr('checked', false);
        refreshInbox();
    }
}

function setMessageIndex(index) {
    if ($('#curr_index').val() != index) {
        $('#curr_index').val(index);
        refreshInbox();
    }
}

function sortMessages(sortMethod) {
    if ($('#message_sort_order').val() != sortMethod) {
        $('#message_sort_order').val(sortMethod);
        refreshInbox();
    }
}

function toggleArchivedMessages() {
    $('#show_archived_messages').val(function(i,v) {
        if (v == 't') return 'f';
        else return 't';
    });
    refreshInbox();
}

function setMessageBlockSize(blockSize) {
    if ($('#block_size').val() != blockSize) {
        $('#block_size').val(blockSize);
        refreshInbox();
    }
}

function toggleSelectedMessages() {
    var $label = $('#select_all').find('div');
    if ($label.text()=='Select all') {
        $('.message-row').addClass('active');
        $('.message-row').find(':checkbox').attr('checked', true);
    }
    else {
        $('.message-row').removeClass('active');
        $('.message-row').find(':checkbox').attr('checked', false);
    }
    setMessagesButtonStates();
}

function setMessagesButtonStates() {

    // (de)select all button
    var $label = $('#select_all').find('div');
    if (!$('.message-row').find('input[type=checkbox]:not(:checked)').length) {
        $label.text('Deselect all');
    }
    else {
        $label.text('Select all');
    }

    // archive & delete buttons
    if ($('.message-row').hasClass('active')) {
        $('#archive_messages').removeAttr('disabled');
        $('#delete_messages').removeAttr('disabled');
    }
    else {
        $('#archive_messages').attr('disabled','disabled');
        $('#delete_messages').attr('disabled','disabled');
    }
}

$(function() {

    $('#tag_search').change(function() {
        refreshInbox();
    });

    $('#contact_search').change(function() {
        refreshInbox();
    });

    $('#message_search').change(function() {
        refreshInbox();
    });

    $('form').submit(function() {
        return ready_to_submit;
    });

    // todo: comment all this stuff

    $('.contact-pill').click(function() {
        $(this).toggleClass('active');
        // if any contact is active
        if ($('.contact-pill').hasClass('active')) {
            $('#all_contacts_pill').removeClass('active');
        }
        else {
            $(this).toggleClass('active');
        }
    });

    $('#all_contacts_pill').click(function() {
        $(this).addClass('active');
        $('.contact-pill').removeClass('active');
        $('#selected_contacts').val('');
    });

    $('.tag-pill').click(function() {
        $(this).toggleClass('active');
        // if any tag is active
        if ($('.tag-pill').hasClass('active')) {
            $('#all_tags_pill').removeClass('active');
        }
        else {
            $(this).toggleClass('active');
        }
    });

    $('#all_tags_pill').click(function() {
        $(this).addClass('active');
        $('.tag-pill').removeClass('active');
        $('#selected_tags').val('');
    });

    $('.message-row').mouseenter(function() {
        $(this).addClass('message-hover');
    });

    $('.message-row').mouseleave(function() {
        $(this).removeClass('message-hover');
    });

    $('.message-row').click(function() {
        $(this).toggleClass('active');
        var $chk = $(this).find(':checkbox');
        $chk.attr('checked', !$chk.attr('checked'));
        setMessagesButtonStates();
    });

    $('.message-row').find(':checkbox').click(function(e) {
        e.stopPropagation();
        $(this).closest('tr').toggleClass('active');
        setMessagesButtonStates();
    });

    setMessagesButtonStates();

});
