--drop view if exists v_message_recd;

create view v_message_recd as
    select
      m.id message_id,
      am1.id account_message_id,
      a2.id from_account_id,
      a2.display_name from_display_name,
      a1.id to_account_id,
      a1.display_name to_display_name,
      al.id account_link_id,
      al.hidden,
      am1.archived,
      am1.read_
  from
    message m,
      account_message am1, -- recipient
      account_message am2, -- sender
      account a1, -- recipient
      account a2, -- sender
      account_link al,
      link l
  where am1.recipient_type_code = 2 -- to
    and a1.id = am1.recipient_account_id
    and m.id = am1.message_id
    and am2.message_id = m.id
    and am2.recipient_type_code = 1 -- from
    and a2.id = am2.recipient_account_id
    and al.from_account_id = a2.id
    and al.to_account_id = a1.id
    and l.id = al.link_id
    and l.link_state_code in (2,4) -- accepted, broken
  order by message_id, from_account_id;
