SELECT first_name, last_name, birth_date
FROM students 
ORDER 
BY last_name ASC
LIMIT 4;

SELECT *
FROM students
ORDER
BY birth_date DESC
LIMIT 1;

SELECT *
FROM students
LIMIT 3
OFFSET 2;