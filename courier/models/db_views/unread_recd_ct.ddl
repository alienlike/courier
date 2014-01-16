--drop view if exists unread_recd_ct;

create view unread_recd_ct as
    select a1.id to_account_id, count(*) ct
  from  account a1, account_message am
  where am.recipient_account_id = a1.id
    and am.recipient_type_code = 2 -- to
    and am.read_ = false
  group by a1.id;
