-- Clean SQL file without special characters
-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS album_artists CASCADE;
DROP TABLE IF EXISTS albums CASCADE;
DROP TABLE IF EXISTS artists CASCADE;

-- Create Artists table (Secondary Entity)
CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100) NOT NULL,
    formed_year INTEGER CHECK (formed_year >= 1900 AND formed_year <= 2024),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Albums table (Primary Entity)
CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INTEGER NOT NULL CHECK (release_year >= 1900 AND release_year <= 2024),
    genre VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Many-to-Many relationship table
CREATE TABLE album_artists (
    id SERIAL PRIMARY KEY,
    album_id INTEGER REFERENCES albums(id) ON DELETE CASCADE,
    artist_id INTEGER REFERENCES artists(id) ON DELETE CASCADE,
    UNIQUE(album_id, artist_id)
);

-- Create indexes for better performance
CREATE INDEX idx_albums_title ON albums(title);
CREATE INDEX idx_albums_genre ON albums(genre);
CREATE INDEX idx_albums_year ON albums(release_year);
CREATE INDEX idx_artists_name ON artists(name);
CREATE INDEX idx_album_artists_album ON album_artists(album_id);
CREATE INDEX idx_album_artists_artist ON album_artists(artist_id);

-- Insert sample artists (Secondary Entity - 15 artists)
INSERT INTO artists (name, country, formed_year) VALUES
('The Beatles', 'United Kingdom', 1960),
('Pink Floyd', 'United Kingdom', 1965),
('Led Zeppelin', 'United Kingdom', 1968),
('Queen', 'United Kingdom', 1970),
('The Rolling Stones', 'United Kingdom', 1962),
('Bob Dylan', 'United States', 1961),
('David Bowie', 'United Kingdom', 1962),
('Radiohead', 'United Kingdom', 1985),
('Nirvana', 'United States', 1987),
('The Doors', 'United States', 1965),
('Jimi Hendrix', 'United States', 1966),
('AC/DC', 'Australia', 1973),
('Black Sabbath', 'United Kingdom', 1968),
('Deep Purple', 'United Kingdom', 1968),
('The Who', 'United Kingdom', 1964);

-- Insert sample albums (Primary Entity - 20 albums)
INSERT INTO albums (title, release_year, genre) VALUES
('Abbey Road', 1969, 'Rock'),
('The Dark Side of the Moon', 1973, 'Progressive Rock'),
('Led Zeppelin IV', 1971, 'Hard Rock'),
('Bohemian Rhapsody', 1975, 'Rock'),
('Sticky Fingers', 1971, 'Rock'),
('Highway 61 Revisited', 1965, 'Folk Rock'),
('The Rise and Fall of Ziggy Stardust', 1972, 'Glam Rock'),
('OK Computer', 1997, 'Alternative Rock'),
('Nevermind', 1991, 'Grunge'),
('The Doors', 1967, 'Psychedelic Rock'),
('Are You Experienced', 1967, 'Psychedelic Rock'),
('Back in Black', 1980, 'Hard Rock'),
('Paranoid', 1970, 'Heavy Metal'),
('Machine Head', 1972, 'Hard Rock'),
('Whos Next', 1971, 'Rock'),
('Sgt Peppers Lonely Hearts Club Band', 1967, 'Psychedelic Rock'),
('Wish You Were Here', 1975, 'Progressive Rock'),
('Physical Graffiti', 1975, 'Hard Rock'),
('A Night at the Opera', 1975, 'Rock'),
('Let It Bleed', 1969, 'Rock');

-- Create album-artist relationships (Many-to-Many)
INSERT INTO album_artists (album_id, artist_id) VALUES
-- Beatles albums
(1, 1), -- Abbey Road - The Beatles
(16, 1), -- Sgt. Pepper's - The Beatles

-- Pink Floyd albums
(2, 2), -- Dark Side of the Moon - Pink Floyd
(17, 2), -- Wish You Were Here - Pink Floyd

-- Led Zeppelin albums
(3, 3), -- Led Zeppelin IV - Led Zeppelin
(18, 3), -- Physical Graffiti - Led Zeppelin

-- Queen albums
(4, 4), -- Bohemian Rhapsody - Queen
(19, 4), -- A Night at the Opera - Queen

-- Rolling Stones albums
(5, 5), -- Sticky Fingers - Rolling Stones
(20, 5), -- Let It Bleed - Rolling Stones

-- Other artists
(6, 6), -- Highway 61 Revisited - Bob Dylan
(7, 7), -- Ziggy Stardust - David Bowie
(8, 8), -- OK Computer - Radiohead
(9, 9), -- Nevermind - Nirvana
(10, 10), -- The Doors - The Doors
(11, 11), -- Are You Experienced - Jimi Hendrix
(12, 12), -- Back in Black - AC/DC
(13, 13), -- Paranoid - Black Sabbath
(14, 14), -- Machine Head - Deep Purple
(15, 15); -- Who's Next - The Who

-- Verify the data
SELECT 'Artists created:' as info, COUNT(*) as count FROM artists
UNION ALL
SELECT 'Albums created:', COUNT(*) FROM albums
UNION ALL
SELECT 'Relationships created:', COUNT(*) FROM album_artists;