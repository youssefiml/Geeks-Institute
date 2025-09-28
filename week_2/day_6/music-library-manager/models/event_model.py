import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.index import get_db_connection
from datetime import datetime, date

class EventModel:
    def __init__(self):
        pass

    def get_events_paginated(self, page, per_page):
        """Get paginated events with organizer information"""
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get total count
        cur.execute("SELECT COUNT(*) FROM events")
        total = cur.fetchone()[0]
        
        # Get paginated events with organizer info
        cur.execute("""
            SELECT e.id, e.name, e.date, e.location, e.description, e.created_at,
                   o.name as organizer_name, o.id as organizer_id
            FROM events e
            JOIN organizers o ON e.organizer_id = o.id
            ORDER BY e.date DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        
        events = []
        for row in cur.fetchall():
            events.append({
                'id': row[0],
                'name': row[1],
                'date': row[2],
                'location': row[3],
                'description': row[4],
                'created_at': row[5],
                'organizer_name': row[6],
                'organizer_id': row[7]
            })
        
        cur.close()
        conn.close()
        
        return events, total

    def search_events(self, search_term, page, per_page):
        """Search events by name, location, or organizer"""
        offset = (page - 1) * per_page
        search_pattern = f"%{search_term}%"
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get total count for search
        cur.execute("""
            SELECT COUNT(*)
            FROM events e
            JOIN organizers o ON e.organizer_id = o.id
            WHERE e.name ILIKE %s OR e.location ILIKE %s OR o.name ILIKE %s
        """, (search_pattern, search_pattern, search_pattern))
        total = cur.fetchone()[0]
        
        # Get paginated search results
        cur.execute("""
            SELECT e.id, e.name, e.date, e.location, e.description, e.created_at,
                   o.name as organizer_name, o.id as organizer_id
            FROM events e
            JOIN organizers o ON e.organizer_id = o.id
            WHERE e.name ILIKE %s OR e.location ILIKE %s OR o.name ILIKE %s
            ORDER BY e.date DESC
            LIMIT %s OFFSET %s
        """, (search_pattern, search_pattern, search_pattern, per_page, offset))
        
        events = []
        for row in cur.fetchall():
            events.append({
                'id': row[0],
                'name': row[1],
                'date': row[2],
                'location': row[3],
                'description': row[4],
                'created_at': row[5],
                'organizer_name': row[6],
                'organizer_id': row[7]
            })
        
        cur.close()
        conn.close()
        
        return events, total

    def get_event_by_id(self, event_id):
        """Get a single event by ID with organizer info"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT e.id, e.name, e.date, e.location, e.description, e.created_at,
                   o.name as organizer_name, o.id as organizer_id, o.email, o.phone
            FROM events e
            JOIN organizers o ON e.organizer_id = o.id
            WHERE e.id = %s
        """, (event_id,))
        
        row = cur.fetchone()
        if row:
            event = {
                'id': row[0],
                'name': row[1],
                'date': row[2],
                'location': row[3],
                'description': row[4],
                'created_at': row[5],
                'organizer_name': row[6],
                'organizer_id': row[7],
                'organizer_email': row[8],
                'organizer_phone': row[9]
            }
        else:
            event = None
        
        cur.close()
        conn.close()
        
        return event

    def create_event(self, name, date, location, description, organizer_id):
        """Create a new event"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO events (name, date, location, description, organizer_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (name, date, location, description, organizer_id))
        
        event_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        
        return event_id

    def update_event(self, event_id, name, date, location, description, organizer_id):
        """Update an existing event"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE events 
            SET name = %s, date = %s, location = %s, description = %s, organizer_id = %s
            WHERE id = %s
        """, (name, date, location, description, organizer_id, event_id))
        
        conn.commit()
        cur.close()
        conn.close()

    def delete_event(self, event_id):
        """Delete an event (tickets will be deleted by CASCADE)"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
        
        conn.commit()
        cur.close()
        conn.close()

    def get_all_organizers(self):
        """Get all organizers"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT o.id, o.name, o.email, o.phone, o.created_at,
                   COUNT(e.id) as event_count
            FROM organizers o
            LEFT JOIN events e ON o.id = e.organizer_id
            GROUP BY o.id, o.name, o.email, o.phone, o.created_at
            ORDER BY o.name
        """)
        
        organizers = []
        for row in cur.fetchall():
            organizers.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'created_at': row[4],
                'event_count': row[5]
            })
        
        cur.close()
        conn.close()
        
        return organizers

    def create_organizer(self, name, email, phone):
        """Create a new organizer"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO organizers (name, email, phone)
            VALUES (%s, %s, %s)
        """, (name, email, phone))
        
        conn.commit()
        cur.close()
        conn.close()

    def get_all_attendees(self):
        """Get all attendees with their event count"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT a.id, a.name, a.email, a.phone, a.created_at,
                   COUNT(t.id) as event_count
            FROM attendees a
            LEFT JOIN tickets t ON a.id = t.attendee_id
            GROUP BY a.id, a.name, a.email, a.phone, a.created_at
            ORDER BY a.name
        """)
        
        attendees = []
        for row in cur.fetchall():
            attendees.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'created_at': row[4],
                'event_count': row[5]
            })
        
        cur.close()
        conn.close()
        
        return attendees

    def create_attendee(self, name, email, phone):
        """Create a new attendee"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO attendees (name, email, phone)
            VALUES (%s, %s, %s)
        """, (name, email, phone))
        
        conn.commit()
        cur.close()
        conn.close()

    def get_attendee_by_id(self, attendee_id):
        """Get a single attendee by ID"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM attendees WHERE id = %s", (attendee_id,))
        row = cur.fetchone()
        
        if row:
            attendee = {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'created_at': row[4]
            }
        else:
            attendee = None
        
        cur.close()
        conn.close()
        
        return attendee

    def get_event_attendees(self, event_id):
        """Get all attendees for a specific event"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT a.id, a.name, a.email, a.phone, t.created_at as registered_at
            FROM attendees a
            JOIN tickets t ON a.id = t.attendee_id
            WHERE t.event_id = %s
            ORDER BY t.created_at DESC
        """, (event_id,))
        
        attendees = []
        for row in cur.fetchall():
            attendees.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'registered_at': row[4]
            })
        
        cur.close()
        conn.close()
        
        return attendees

    def register_attendee(self, event_id, attendee_id):
        """Register an attendee for an event (create ticket)"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if already registered
        cur.execute("""
            SELECT id FROM tickets 
            WHERE event_id = %s AND attendee_id = %s
        """, (event_id, attendee_id))
        
        if cur.fetchone():
            cur.close()
            conn.close()
            raise Exception("Attendee is already registered for this event")
        
        # Create ticket
        cur.execute("""
            INSERT INTO tickets (event_id, attendee_id)
            VALUES (%s, %s)
        """, (event_id, attendee_id))
        
        conn.commit()
        cur.close()
        conn.close()

    def get_statistics(self):
        """Get dashboard statistics"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Total counts
        cur.execute("SELECT COUNT(*) FROM events")
        total_events = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM organizers")
        total_organizers = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM attendees")
        total_attendees = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM tickets")
        total_registrations = cur.fetchone()[0]
        
        # Upcoming events
        cur.execute("SELECT COUNT(*) FROM events WHERE date >= %s", (date.today(),))
        upcoming_events = cur.fetchone()[0]
        
        # Most popular event
        cur.execute("""
            SELECT e.name, COUNT(t.id) as attendee_count
            FROM events e
            LEFT JOIN tickets t ON e.id = t.event_id
            GROUP BY e.id, e.name
            ORDER BY attendee_count DESC
            LIMIT 1
        """)
        popular_result = cur.fetchone()
        most_popular_event = popular_result[0] if popular_result else "No events yet"
        
        # Most active organizer
        cur.execute("""
            SELECT o.name, COUNT(e.id) as event_count
            FROM organizers o
            LEFT JOIN events e ON o.id = e.organizer_id
            GROUP BY o.id, o.name
            ORDER BY event_count DESC
            LIMIT 1
        """)
        active_result = cur.fetchone()
        most_active_organizer = active_result[0] if active_result else "No organizers yet"
        
        cur.close()
        conn.close()
        
        return {
            'total_events': total_events,
            'total_organizers': total_organizers,
            'total_attendees': total_attendees,
            'total_registrations': total_registrations,
            'upcoming_events': upcoming_events,
            'most_popular_event': most_popular_event,
            'most_active_organizer': most_active_organizer
        }

    def get_organizer_statistics(self):
        """Get statistics for events per organizer"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT o.name, COUNT(e.id) as event_count
            FROM organizers o
            LEFT JOIN events e ON o.id = e.organizer_id
            GROUP BY o.id, o.name
            ORDER BY event_count DESC
            LIMIT 10
        """)
        
        stats = []
        for row in cur.fetchall():
            stats.append({
                'organizer': row[0],
                'events': row[1]
            })
        
        cur.close()
        conn.close()
        
        return stats

    def get_monthly_statistics(self):
        """Get monthly event statistics"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                TO_CHAR(date, 'YYYY-MM') as month,
                COUNT(*) as event_count
            FROM events
            WHERE date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY TO_CHAR(date, 'YYYY-MM')
            ORDER BY month
        """)
        
        stats = []
        for row in cur.fetchall():
            stats.append({
                'month': row[0],
                'events': row[1]
            })
        
        cur.close()
        conn.close()
        
        return stats

    def get_popular_events(self):
        """Get most popular events by attendee count"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT e.name, COUNT(t.id) as attendee_count
            FROM events e
            LEFT JOIN tickets t ON e.id = t.event_id
            GROUP BY e.id, e.name
            ORDER BY attendee_count DESC
            LIMIT 10
        """)
        
        stats = []
        for row in cur.fetchall():
            stats.append({
                'event': row[0],
                'attendees': row[1]
            })
        
        cur.close()
        conn.close()
        
        return stats