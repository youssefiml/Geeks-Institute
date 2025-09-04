-- 1) Fetch the last 2 customers in alphabetical order (A-Z) – 
-- exclude ‘id’ from the results.
SELECT first_name, last_name
FROM customers
ORDER
BY first_name ASC
OFFSET (SELECT COUNT(*) - 2 FROM customers)
LIMIT 2;

-- 2)Use SQL to delete all purchases made by Scott.
DELETE FROM purchases
WHERE customer_id = (
  SELECT id FROM customers WHERE first_name = 'Scott'
);

-- 3)Does Scott still exist in the customers table, 
-- even though he has been deleted? Try and find him.
SELECT * 
FROM customers 
WHERE first_name = 'Scott';


-- 4) Use SQL to find all purchases. Join purchases with the customers table, 
-- so that Scott’s order will appear, although instead of the customer’s first and last name.
SELECT p.id AS purchase_id,
       p.item,
       c.first_name,
       c.last_name
FROM purchases p
LEFT JOIN customers c ON p.customer_id = c.id;


-- 5) Use SQL to find all purchases. Join purchases with the customers table,
-- so that Scott’s order will NOT appear.
SELECT p.id AS purchase_id,
       p.item,
       c.first_name,
       c.last_name
FROM purchases p
INNER JOIN customers c ON p.customer_id = c.id;