CREATE TABLE actors(
	actor_id SERIAL PRIMARY KEY,
	first_name VARCHAR (50) NOT NULL,
	last_name VARCHAR (100) NOT NULL,
	age DATE NOT NULL,
	number_oscars SMALLINT NOT NULL
);

INSERT INTO actors(first_name, last_name, age, number_oscars)
VALUES ('Brad', 'Pitt', '18,12,1963', 2),
	('Johnny', 'Depp', '09,06,1963', 6),
	('Tom', 'Cruise', '03,07,1962', 3),
	('Glenn', 'Close', '19,03,1947', 4),
    ('Leonardo', 'DiCaprio', '05/10/1075', 1),
    ('Kate', 'Winslet', '11/11/1974', 1),
    ('Matt','Damon','08/10/1970', 5),
    ('George','Clooney','06/05/1961', 2);

SELECT * FROM actors;
SELECT COUNT(*) FROM actors;

INSERT INTO actors(first_name, last_name, age, number_oscars)
VALUES ('', '', '19-03-1947', 0);