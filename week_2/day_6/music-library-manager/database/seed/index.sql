-- Drop tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS organizers CASCADE;
DROP TABLE IF EXISTS attendees CASCADE;

-- Create organizers table (primary entity)
CREATE TABLE organizers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create attendees table (secondary entity)
CREATE TABLE attendees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create events table (main entity)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    organizer_id INTEGER NOT NULL REFERENCES organizers(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tickets table (many-to-many relationship: events <-> attendees)
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    attendee_id INTEGER NOT NULL REFERENCES attendees(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, attendee_id)
);

-- Create indexes for better performance
CREATE INDEX idx_events_date ON events(date);
CREATE INDEX idx_events_organizer ON events(organizer_id);
CREATE INDEX idx_tickets_event ON tickets(event_id);
CREATE INDEX idx_tickets_attendee ON tickets(attendee_id);
CREATE INDEX idx_events_name ON events(name);

-- Insert sample organizers (10 organizers)
INSERT INTO organizers (name, email, phone) VALUES
('TechEvents Inc', 'contact@techevents.com', '+1-555-0101'),
('Creative Minds Co', 'info@creativeminds.com', '+1-555-0102'),
('Business Network Group', 'hello@businessnetwork.com', '+1-555-0103'),
('Arts & Culture Foundation', 'events@artsculture.org', '+1-555-0104'),
('Health & Wellness Society', 'organizer@healthwellness.org', '+1-555-0105'),
('Music Festival Organizers', 'contact@musicfest.com', '+1-555-0106'),
('Sports Events Co', 'admin@sportsevents.com', '+1-555-0107'),
('Education Summit Group', 'team@edusummit.org', '+1-555-0108'),
('Food & Wine Society', 'events@foodwine.com', '+1-555-0109'),
('Community Events Network', 'info@communityevents.org', '+1-555-0110');

-- Insert sample attendees (15 attendees)
INSERT INTO attendees (name, email, phone) VALUES
('Alice Johnson', 'alice.johnson@email.com', '+1-555-1001'),
('Bob Smith', 'bob.smith@email.com', '+1-555-1002'),
('Carol Davis', 'carol.davis@email.com', '+1-555-1003'),
('David Wilson', 'david.wilson@email.com', '+1-555-1004'),
('Emily Brown', 'emily.brown@email.com', '+1-555-1005'),
('Frank Miller', 'frank.miller@email.com', '+1-555-1006'),
('Grace Lee', 'grace.lee@email.com', '+1-555-1007'),
('Henry Taylor', 'henry.taylor@email.com', '+1-555-1008'),
('Isabel Martinez', 'isabel.martinez@email.com', '+1-555-1009'),
('Jack Anderson', 'jack.anderson@email.com', '+1-555-1010'),
('Kate Thompson', 'kate.thompson@email.com', '+1-555-1011'),
('Liam Garcia', 'liam.garcia@email.com', '+1-555-1012'),
('Maya Patel', 'maya.patel@email.com', '+1-555-1013'),
('Nathan Clark', 'nathan.clark@email.com', '+1-555-1014'),
('Olivia Rodriguez', 'olivia.rodriguez@email.com', '+1-555-1015');

-- Insert sample events (12 events)
INSERT INTO events (name, date, location, description, organizer_id) VALUES
('Tech Innovation Summit 2025', '2025-10-15', 'San Francisco Convention Center', 'Annual technology conference featuring the latest innovations in AI, blockchain, and quantum computing.', 1),
('Creative Arts Workshop', '2025-11-20', 'Downtown Art Gallery', 'Interactive workshop for aspiring artists to learn new techniques and network with professionals.', 2),
('Business Leadership Forum', '2025-12-05', 'Marriott Business Hotel', 'Executive forum discussing leadership strategies in the digital age.', 3),
('Classical Music Gala', '2025-10-30', 'City Symphony Hall', 'Evening of classical music performances by renowned international artists.', 4),
('Wellness & Mindfulness Retreat', '2025-11-15', 'Mountain View Spa Resort', 'Three-day retreat focused on mental health, meditation, and holistic wellness practices.', 5),
('Rock Music Festival', '2025-12-20', 'Riverside Park Amphitheater', 'Two-day outdoor music festival featuring local and international rock bands.', 6),
('Marathon Championship', '2025-10-25', 'City Center to Waterfront', 'Annual city marathon with categories for professional and amateur runners.', 7),
('Education Technology Conference', '2025-11-10', 'University Convention Center', 'Conference exploring the future of education technology and digital learning.', 8),
('Culinary Excellence Awards', '2025-12-15', 'Grand Hotel Ballroom', 'Annual awards ceremony celebrating the finest restaurants and chefs in the region.', 9),
('Community Service Fair', '2025-10-20', 'Central Community Center', 'Fair showcasing local volunteer opportunities and community service projects.', 10),
('Startup Pitch Competition', '2025-11-25', 'Innovation Hub Downtown', 'Competition for early-stage startups to pitch their ideas to investors.', 1),
('Holiday Charity Concert', '2025-12-22', 'Cathedral Concert Hall', 'Annual holiday concert raising funds for local charities and food banks.', 6);

-- Insert sample ticket registrations (attendees registered for events)
INSERT INTO tickets (event_id, attendee_id) VALUES
-- Tech Innovation Summit (event 1)
(1, 1), (1, 2), (1, 3), (1, 7), (1, 12),
-- Creative Arts Workshop (event 2)
(2, 4), (2, 5), (2, 6), (2, 13),
-- Business Leadership Forum (event 3)
(3, 1), (3, 8), (3, 9), (3, 14), (3, 15),
-- Classical Music Gala (event 4)
(4, 2), (4, 10), (4, 11), (4, 6),
-- Wellness Retreat (event 5)
(5, 3), (5, 4), (5, 13), (5, 5), (5, 7),
-- Rock Music Festival (event 6)
(6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 15),
-- Marathon Championship (event 7)
(7, 1), (7, 14), (7, 2),
-- Education Tech Conference (event 8)
(8, 3), (8, 12), (8, 13), (8, 6),
-- Culinary Awards (event 9)
(9, 4), (9, 5), (9, 7), (9, 9), (9, 15),
-- Community Service Fair (event 10)
(10, 8), (10, 10), (10, 14),
-- Startup Pitch Competition (event 11)
(11, 1), (11, 11), (11, 12), (11, 6),
-- Holiday Charity Concert (event 12)
(12, 2), (12, 3), (12, 4), (12, 5), (12, 13), (12, 15), (12, 7);

-- Verify the data
SELECT 'Database setup completed successfully!' as status;
SELECT 'Total organizers: ' || COUNT(*) as organizers_count FROM organizers;
SELECT 'Total attendees: ' || COUNT(*) as attendees_count FROM attendees;
SELECT 'Total events: ' || COUNT(*) as events_count FROM events;
SELECT 'Total registrations: ' || COUNT(*) as tickets_count FROM tickets;