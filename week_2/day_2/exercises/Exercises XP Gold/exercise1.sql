-- 1)
SELECT rating, COUNT(*) AS film_count
FROM film
GROUP BY rating;

-- 2)
SELECT title, rating
FROM film
WHERE rating IN ('G','PG-13');

-- 2:1)
SELECT title, rating, length, rental_rate
FROM film
WHERE rating IN ('G','PG-13')
  AND length < 120
  AND rental_rate < 3.00
ORDER BY title;

-- 3)
UPDATE customer
SET first_name = 'Youssef', last_name = 'Imlilss', email = 'oudra.brahim@gmail.com'
WHERE customer_id = 1;

-- 4)
UPDATE address
SET address = 'Ben Msik', district='Casablanca'
WHERE address_id = (
    SELECT address_id 
    FROM customer 
    WHERE customer_id = 1
);