import sys
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import math
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import your modules
try:
    from models.music_model import MusicModel
    from database.index import get_db_connection
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have created the models/ and database/ directories with __init__.py files")
    sys.exit(1)

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Use environment variable for secret key, with fallback for development
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Initialize the model
music_model = MusicModel()

@app.route('/')
def index():
    """Main page showing albums with pagination and search"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    per_page = 6
    
    if search:
        albums, total = music_model.search_albums(search, page, per_page)
    else:
        albums, total = music_model.get_albums_paginated(page, per_page)
    
    total_pages = math.ceil(total / per_page)
    
    return render_template('index.html', 
                         albums=albums, 
                         page=page, 
                         total_pages=total_pages,
                         search=search)

@app.route('/create', methods=['GET', 'POST'])
def create_album():
    """Create a new album"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        release_year = request.form.get('release_year', type=int)
        genre = request.form.get('genre', '').strip()
        artist_ids = request.form.getlist('artist_ids')
        
        # Validation
        errors = []
        if not title:
            errors.append('Album title is required')
        if not release_year or release_year < 1900 or release_year > 2024:
            errors.append('Valid release year is required (1900-2024)')
        if not genre:
            errors.append('Genre is required')
        if not artist_ids:
            errors.append('At least one artist must be selected')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            artists = music_model.get_all_artists()
            return render_template('create.html', artists=artists, 
                                 title=title, release_year=release_year, 
                                 genre=genre, selected_artists=artist_ids)
        
        try:
            album_id = music_model.create_album(title, release_year, genre, artist_ids)
            flash(f'Album "{title}" created successfully!', 'success')
            return redirect(url_for('album_details', album_id=album_id))
        except Exception as e:
            flash(f'Error creating album: {str(e)}', 'error')
    
    artists = music_model.get_all_artists()
    return render_template('create.html', artists=artists)

@app.route('/album/<int:album_id>')
def album_details(album_id):
    """Show album details"""
    album = music_model.get_album_by_id(album_id)
    if not album:
        flash('Album not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('details.html', album=album)

@app.route('/edit/<int:album_id>', methods=['GET', 'POST'])
def edit_album(album_id):
    """Edit an existing album"""
    album = music_model.get_album_by_id(album_id)
    if not album:
        flash('Album not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        release_year = request.form.get('release_year', type=int)
        genre = request.form.get('genre', '').strip()
        artist_ids = request.form.getlist('artist_ids')
        
        # Validation
        errors = []
        if not title:
            errors.append('Album title is required')
        if not release_year or release_year < 1900 or release_year > 2024:
            errors.append('Valid release year is required (1900-2024)')
        if not genre:
            errors.append('Genre is required')
        if not artist_ids:
            errors.append('At least one artist must be selected')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            artists = music_model.get_all_artists()
            return render_template('edit.html', album=album, artists=artists,
                                 title=title, release_year=release_year, 
                                 genre=genre, selected_artists=artist_ids)
        
        try:
            music_model.update_album(album_id, title, release_year, genre, artist_ids)
            flash(f'Album "{title}" updated successfully!', 'success')
            return redirect(url_for('album_details', album_id=album_id))
        except Exception as e:
            flash(f'Error updating album: {str(e)}', 'error')
    
    artists = music_model.get_all_artists()
    return render_template('edit.html', album=album, artists=artists)

@app.route('/delete/<int:album_id>', methods=['POST'])
def delete_album(album_id):
    """Delete an album"""
    album = music_model.get_album_by_id(album_id)
    if not album:
        flash('Album not found', 'error')
        return redirect(url_for('index'))
    
    try:
        music_model.delete_album(album_id)
        flash(f'Album "{album["title"]}" deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting album: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    """Statistics and analytics page"""
    stats_data = music_model.get_statistics()
    return render_template('stats.html', stats=stats_data)

@app.route('/api/stats/genres')
def api_genre_stats():
    """API endpoint for genre statistics (for charts)"""
    genre_stats = music_model.get_genre_statistics()
    return jsonify(genre_stats)

@app.route('/api/stats/years')
def api_year_stats():
    """API endpoint for release year statistics (for charts)"""
    year_stats = music_model.get_year_statistics()
    return jsonify(year_stats)

@app.route('/artists')
def artists():
    """View all artists"""
    all_artists = music_model.get_all_artists()
    return render_template('artists.html', artists=all_artists)

@app.route('/create_artist', methods=['GET', 'POST'])
def create_artist():
    """Create a new artist"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        country = request.form.get('country', '').strip()
        formed_year = request.form.get('formed_year', type=int)
        
        # Validation
        errors = []
        if not name:
            errors.append('Artist name is required')
        if not country:
            errors.append('Country is required')
        if formed_year and (formed_year < 1900 or formed_year > 2024):
            errors.append('Valid formed year is required (1900-2024)')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('create_artist.html', 
                                 name=name, country=country, formed_year=formed_year)
        
        try:
            music_model.create_artist(name, country, formed_year)
            flash(f'Artist "{name}" created successfully!', 'success')
            return redirect(url_for('artists'))
        except Exception as e:
            flash(f'Error creating artist: {str(e)}', 'error')
    
    return render_template('create_artist.html')

if __name__ == '__main__':
    app.run(debug=True)