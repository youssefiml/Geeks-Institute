import sys
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import math
from datetime import datetime, date
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models.event_model import EventModel
    from database.index import get_db_connection
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have created the models/ and database/ directories with __init__.py files")
    sys.exit(1)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

event_model = EventModel()

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    per_page = 6

    if search:
        events, total = event_model.search_events(search, page, per_page)
    else:
        events, total = event_model.get_events_paginated(page, per_page)

    total_pages = math.ceil(total / per_page)

    return render_template('index.html', 
                         events=events, 
                         page=page, 
                         total_pages=total_pages,
                         search=search)

@app.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        date_str = request.form.get('date', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        organizer_id = request.form.get('organizer_id', type=int)

        errors = []
        if not name:
            errors.append('Event name is required')
        if not date_str:
            errors.append('Event date is required')
        else:
            try:
                event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if event_date < date.today():
                    errors.append('Event date cannot be in the past')
            except ValueError:
                errors.append('Invalid date format')
        if not location:
            errors.append('Location is required')
        if not organizer_id:
            errors.append('Organizer must be selected')

        if errors:
            for error in errors:
                flash(error, 'error')
            organizers = event_model.get_all_organizers()
            return render_template('create.html', organizers=organizers, 
                                 name=name, date=date_str, location=location, 
                                 description=description, organizer_id=organizer_id)

        try:
            event_id = event_model.create_event(name, date_str, location, description, organizer_id)
            flash(f'Event "{name}" created successfully!', 'success')
            return redirect(url_for('event_details', event_id=event_id))
        except Exception as e:
            flash(f'Error creating event: {str(e)}', 'error')

    organizers = event_model.get_all_organizers()
    return render_template('create.html', organizers=organizers)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = event_model.get_event_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('index'))

    attendees = event_model.get_event_attendees(event_id)
    return render_template('details.html', event=event, attendees=attendees)

@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = event_model.get_event_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        date_str = request.form.get('date', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        organizer_id = request.form.get('organizer_id', type=int)

        errors = []
        if not name:
            errors.append('Event name is required')
        if not date_str:
            errors.append('Event date is required')
        else:
            try:
                event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if event_date < date.today():
                    errors.append('Event date cannot be in the past')
            except ValueError:
                errors.append('Invalid date format')
        if not location:
            errors.append('Location is required')
        if not organizer_id:
            errors.append('Organizer must be selected')

        if errors:
            for error in errors:
                flash(error, 'error')
            organizers = event_model.get_all_organizers()
            return render_template('edit.html', event=event, organizers=organizers,
                                 name=name, date=date_str, location=location, 
                                 description=description, organizer_id=organizer_id)

        try:
            event_model.update_event(event_id, name, date_str, location, description, organizer_id)
            flash(f'Event "{name}" updated successfully!', 'success')
            return redirect(url_for('event_details', event_id=event_id))
        except Exception as e:
            flash(f'Error updating event: {str(e)}', 'error')

    organizers = event_model.get_all_organizers()
    return render_template('edit.html', event=event, organizers=organizers)

@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = event_model.get_event_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('index'))

    try:
        event_model.delete_event(event_id)
        flash(f'Event "{event["name"]}" deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting event: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/organizers')
def organizers():
    all_organizers = event_model.get_all_organizers()
    return render_template('organizers.html', organizers=all_organizers)

@app.route('/create_organizer', methods=['GET', 'POST'])
def create_organizer():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        errors = []
        if not name:
            errors.append('Organizer name is required')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not phone:
            errors.append('Phone number is required')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('create_organizer.html', 
                                 name=name, email=email, phone=phone)

        try:
            event_model.create_organizer(name, email, phone)
            flash(f'Organizer "{name}" created successfully!', 'success')
            return redirect(url_for('organizers'))
        except Exception as e:
            flash(f'Error creating organizer: {str(e)}', 'error')

    return render_template('create_organizer.html')

@app.route('/attendees')
def attendees():
    all_attendees = event_model.get_all_attendees()
    return render_template('attendees.html', attendees=all_attendees)

@app.route('/create_attendee', methods=['GET', 'POST'])
def create_attendee():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        errors = []
        if not name:
            errors.append('Attendee name is required')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not phone:
            errors.append('Phone number is required')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('create_attendee.html', 
                                 name=name, email=email, phone=phone)

        try:
            event_model.create_attendee(name, email, phone)
            flash(f'Attendee "{name}" created successfully!', 'success')
            return redirect(url_for('attendees'))
        except Exception as e:
            flash(f'Error creating attendee: {str(e)}', 'error')

    return render_template('create_attendee.html')

@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register_for_event(event_id):
    event = event_model.get_event_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        attendee_id = request.form.get('attendee_id', type=int)
        
        if not attendee_id:
            flash('Please select an attendee', 'error')
            attendees = event_model.get_all_attendees()
            return render_template('register.html', event=event, attendees=attendees)

        try:
            event_model.register_attendee(event_id, attendee_id)
            attendee = event_model.get_attendee_by_id(attendee_id)
            flash(f'{attendee["name"]} registered for "{event["name"]}" successfully!', 'success')
            return redirect(url_for('event_details', event_id=event_id))
        except Exception as e:
            flash(f'Error registering attendee: {str(e)}', 'error')

    attendees = event_model.get_all_attendees()
    registered_attendees = event_model.get_event_attendees(event_id)
    registered_ids = [att['id'] for att in registered_attendees]
    
    return render_template('register.html', event=event, attendees=attendees, registered_ids=registered_ids)

@app.route('/dashboard')
def dashboard():
    stats_data = event_model.get_statistics()
    return render_template('dashboard.html', stats=stats_data)

@app.route('/api/stats/organizers')
def api_organizer_stats():
    organizer_stats = event_model.get_organizer_statistics()
    return jsonify(organizer_stats)

@app.route('/api/stats/monthly')
def api_monthly_stats():
    monthly_stats = event_model.get_monthly_statistics()
    return jsonify(monthly_stats)

@app.route('/api/stats/popular')
def api_popular_events():
    popular_stats = event_model.get_popular_events()
    return jsonify(popular_stats)

if __name__ == '__main__':
    app.run(debug=True)