-- drop view v_account;

CREATE OR REPLACE VIEW v_account AS
    SELECT account.id, account.account_type_code, account.uid, account.username, account.display_name
  FROM account;