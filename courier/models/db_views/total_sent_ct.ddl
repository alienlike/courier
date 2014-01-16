--drop view if exists total_sent_ct;

create view total_sent_ct as
    select a1.id from_account_id, count(*) ct
  from  account a1, account_message am
  where am.recipient_account_id = a1.id
    and am.recipient_type_code = 1 -- from
  group by a1.id;
