-- Q1)
SELECT COUNT(*) 
FROM FirstTab AS ft 
WHERE ft.id 
NOT IN ( SELECT id FROM SecondTab WHERE id IS NULL );
-- The OUTPUT is 0

-- Q2)
SELECT COUNT(*) 
FROM FirstTab AS ft 
WHERE ft.id 
NOT IN ( SELECT id FROM SecondTab WHERE id = 5 );
-- The OUTPUT is 2

-- Q3)
SELECT COUNT(*) 
FROM FirstTab AS ft 
WHERE ft.id
NOT IN ( SELECT id FROM SecondTab );
-- The OUTPUT is 0

-- Q4)
SELECT COUNT(*) 
FROM FirstTab AS ft 
WHERE ft.id 
NOT IN ( SELECT id FROM SecondTab WHERE id IS NOT NULL );
-- The OUTPUT is 2
