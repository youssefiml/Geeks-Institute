
-- 1)
SELECT * FROM language;

-- 2)
SELECT f.title, f.description, l.name AS language_name
FROM film f
JOIN language l ON f.language_id = l.language_id;

-- 3)
SELECT f.title, f.description, l.name AS language_name
FROM language l
LEFT JOIN film f ON f.language_id = l.language_id;

-- 4)
CREATE TABLE new_film (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

INSERT INTO new_film (name) VALUES
('Inception'),
('The Matrix'),
('Gladiator');

-- 5)
CREATE TABLE customer_review (
    review_id SERIAL PRIMARY KEY,
    film_id INT NOT NULL,
    language_id INT NOT NULL,
    title VARCHAR(100),
    score INT CHECK(score >= 1 AND score <= 10),
    review_text TEXT,
    last_update TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (film_id) REFERENCES new_film(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES language(language_id)
);

-- 6)
INSERT INTO customer_review (film_id, language_id, title, score, review_text)
VALUES
((SELECT id FROM new_film WHERE name = 'Inception'),
 (SELECT language_id FROM language WHERE name = 'English'),
 'Amazing Movie', 9, 'Great story and visuals.'),

((SELECT id FROM new_film WHERE name = 'Gladiator'),
 (SELECT language_id FROM language WHERE name = 'English'),
 'Epic Film', 10, 'A masterpiece of cinema.');

-- 7)
DELETE FROM new_film WHERE name = 'Gladiator';
