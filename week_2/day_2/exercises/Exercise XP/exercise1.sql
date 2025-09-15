SELECT *
FROM items
ORDER
BY price
ASC;

SELECT *
FROM items
WHERE price >= 80
ORDER
BY price
DESC;

SELECT first_name, last_name
FROM customers
ORDER
BY first_name
ASC
TOP 3;

SELECT last_name FROM customers ORDER BY last_name DESC;