select distinct t.stock_id
from (
select t.*,
  max(t.trans_price) over(partition by t.stock_id) max_price_in_last_15_mins,
  min(t.trans_price) over(partition by t.stock_id) min_price_in_last_15_mins,
  s.high_limit
from dw.stock_transaction t
inner join dw.stock s on t.stock_id = s.stock_id
where t.biz_date = date(now()) 
and s.biz_date = date(now()) 
and t.time >= '14:45:00'
) t where t.max_price_in_last_15_mins = t.high_limit
and t.min_price_in_last_15_mins <> t.high_limit
