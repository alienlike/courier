--drop view if exists total_recd_ct;

create view total_recd_ct as
    select a1.id to_account_id, count(*) ct
  from  account a1, account_message am
  where am.recipient_account_id = a1.id
    and am.recipient_type_code = 2 -- to
  group by a1.id;
