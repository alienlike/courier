--drop view if exists unread_recd_ct_by_tag;

create view unread_recd_ct_by_tag as
    select account_id to_account_id, tag_id, text_ tag_text, coalesce(ct, 0) ct
  from (
      select tags.account_id, tags.tag_id, tags.text_, messages.ct
    from (
      -- get all tags for user
        select a.id account_id, t.id tag_id, t.text_
      from account a, tag t
      where a.id = t.account_id
      ) tags
      left outer join (
      -- get unread message count grouped by tag
        select a.id account_id, mt.tag_id, count(*) ct
      from account a, account_message am, message, message_tag mt
      where a.id = am.recipient_account_id
        and am.message_id = message.id
        and am.recipient_type_code = 2 -- to
        and message.id = mt.message_id
        and am.read_ = false
      group by a.id, mt.tag_id
      ) messages
      on messages.tag_id = tags.tag_id
        and messages.account_id = tags.account_id
    ) r
  order by text_;
