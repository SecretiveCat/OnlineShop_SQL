set enable_indexscan = off; 
set enable_bitmapscan = off;

set enable_seqscan = off;



explain analyze
select c.name, c.surname, COUNT(*) as total_orders
from clients c
join orders o on o.client_id = c.id
group by c.id, c.name, c.surname
order by total_orders desc, c.name asc, c.surname asc
limit 5;


explain analyze
with clients_stat as (
	select o.client_id, COUNT(*) as total_orders
	from orders o
	join products p on p.product_id = o.product_id
	group by o.client_id)
select c.name, c.surname, cs.total_orders
from clients_stat cs
join clients c on c.id = cs.client_id
order by cs.total_orders desc, c.name asc, c.surname asc
limit 5;




create index if not exists idx_orders_client_id on orders(client_id);
create index if not exists idx_orders_product_id on orders(product_id);

drop index if exists idx_orders_client_id;
drop index if exists idx_orders_product_id;


reset enable_indexscan;
reset enable_bitmapscan;

reset enable_seqscan;
