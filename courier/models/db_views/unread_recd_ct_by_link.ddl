--drop view if exists unread_recd_ct_by_link;

create view unread_recd_ct_by_link as
    select account_id to_account_id, link_account_id from_account_id, display_name from_display_name, coalesce(ct, 0) ct, hidden
  from (
      select linked_accts.account_id, linked_accts.link_account_id, linked_accts.display_name, messages.ct, linked_accts.hidden
    from (
      -- get all accounts linked to user
        select a1.id account_id, a2.id link_account_id, a2.display_name, al.hidden
      from link l, account_link al, account a1, account a2
      where al.from_account_id = a1.id
        and al.to_account_id = a2.id
        and al.link_id = l.id
        and l.link_state_code = 2 -- accepted
      ) linked_accts
      left outer join (
      -- get unread message count grouped by sender
        select a1.id to_account_id, a2.id from_account_id, count(*) ct
      from message, account a1, account a2, account_message am1, account_message am2
      where message.id = am1.message_id
        and message.id = am2.message_id
        and am1.recipient_account_id = a1.id
        and am2.recipient_account_id = a2.id
        and am1.recipient_type_code = 2 -- to
        and am2.recipient_type_code = 1 -- from
        and am1.read_ = false
      group by a2.id, a1.id
      ) messages
      on messages.to_account_id = linked_accts.account_id
        and messages.from_account_id = linked_accts.link_account_id
    ) r
  order by from_display_name;
