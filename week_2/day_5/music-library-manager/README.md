# 🎵 Music Library Manager

A comprehensive full-stack web application built with Flask and PostgreSQL for managing your music collection. This application allows you to catalog albums, artists, and their relationships while providing powerful search, statistics, and analytics features.

## ✨ Features

### Core Features (Mandatory)
- ✅ **CRUD Operations**: Create, read, update, and delete albums and artists
- ✅ **Pagination**: Browse albums with 6 items per page
- ✅ **Search Functionality**: Search across album titles, artists, and genres
- ✅ **Database Relationships**: Many-to-many relationships between albums and artists
- ✅ **Responsive Design**: Mobile-friendly interface using Tailwind CSS
- ✅ **Form Validation**: Comprehensive client and server-side validation
- ✅ **Flash Messages**: User feedback for all actions
- ✅ **Statistics Dashboard**: Charts and analytics using Chart.js

### Database Schema
- **Albums** (Primary Entity): title, release_year, genre, created_at
- **Artists** (Secondary Entity): name, country, formed_year, created_at  
- **Album_Artists** (Many-to-Many): Linking albums to artists with cascade delete

### User Interface
- Modern gradient design with glassmorphism effects
- Interactive elements with hover animations
- Mobile-responsive navigation with dropdown menu
- Loading states and smooth transitions
- Chart visualizations for data insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd music-library-manager
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL Database**
   ```bash
   # Create database
   createdb music_library
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE music_library;
   \q
   ```

5. **Configure Database Connection**
   
   Create a `.env` file in the root directory:
   ```env
   DB_HOST=localhost
   DB_NAME=music_library
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_PORT=5432
   ```

6. **Initialize Database with Schema and Sample Data**
   ```bash
   python database/index.py
   ```

7. **Run the Application**
   ```bash
   python index.py
   ```

8. **Open in Browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
music-library-manager/
├── index.py                 # Main Flask application
├── models/
│   └── music_model.py      # Database models and operations
├── database/
│   ├── index.py            # Database connection and initialization
│   └── seed/
│       └── index.sql       # Database schema and sample data
├── templates/
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Albums list page
│   ├── create.html         # Create album form
│   ├── edit.html           # Edit album form
│   ├── details.html        # Album details page
│   ├── stats.html          # Statistics dashboard
│   ├── artists.html        # Artists list page
│   └── create_artist.html  # Create artist form
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🎯 Usage Guide

### Adding Albums
1. Click "Add Album" button or use the floating action button
2. Fill in album details (title, year, genre)
3. Select one or more artists
4. Submit to create the album

### Managing Artists
1. Navigate to "Artists" page
2. Click "Add New Artist" to create artists
3. Provide name, country, and optional formation year
4. View all artists with their country and era information

### Searching and Browsing
- Use the search bar to find albums by title, artist, or genre
- Browse paginated results (6 albums per page)
- Click on album cards to view detailed information
- Edit or delete albums from the details page

### Statistics and Analytics
- Visit the "Statistics" page for insights
- View charts showing albums by genre and release year
- See key metrics like total albums, artists, and genres
- Quick access to recent additions and collection highlights

## 🗃️ Database Schema

### Tables

**artists**
- id (SERIAL PRIMARY KEY)
- name (VARCHAR(255) NOT NULL UNIQUE)
- country (VARCHAR(100) NOT NULL)
- formed_year (INTEGER, optional)
- created_at (TIMESTAMP)

**albums**
- id (SERIAL PRIMARY KEY)  
- title (VARCHAR(255) NOT NULL)
- release_year (INTEGER NOT NULL)
- genre (VARCHAR(100) NOT NULL)
- created_at (TIMESTAMP)

**album_artists**
- id (SERIAL PRIMARY KEY)
- album_id (INTEGER → albums.id CASCADE DELETE)
- artist_id (INTEGER → artists.id CASCADE DELETE)
- UNIQUE(album_id, artist_id)

### Sample Data
The application includes 20 sample albums and 15 sample artists representing various genres and eras, from classic rock legends like The Beatles and Led Zeppelin to modern alternative acts like Radiohead.

## 🎨 Design Features

- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Modern UI**: Gradient backgrounds with glassmorphism effects
- **Interactive Elements**: Hover animations, loading states, and transitions  
- **Accessibility**: Proper contrast ratios and semantic markup
- **Charts**: Beautiful data visualizations using Chart.js
- **Flash Messages**: Auto-dismissing notifications for user feedback

## 🔧 Technical Details

### Backend (Flask)
- RESTful route structure
- PostgreSQL integration with psycopg2
- Form validation and error handling
- JSON API endpoints for charts
- Secure database operations with proper escaping

### Frontend (HTML/CSS/JavaScript)
- Tailwind CSS for styling
- Chart.js for data visualization
- Font Awesome icons
- Vanilla JavaScript for interactivity
- Mobile-first responsive design

### Database
- Proper foreign key constraints
- CASCADE delete for data integrity  
- Indexes for performance optimization
- Data validation at database level

## 🐛 Troubleshooting

**Database Connection Issues:**
- Verify PostgreSQL is running
- Check database credentials in `.env` file
- Ensure database `music_library` exists

**Missing Dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Permission Errors:**
- On macOS/Linux, ensure proper file permissions
- Run with `sudo` if necessary for database operations

**Port Already in Use:**
```bash
# Change port in index.py
app.run(debug=True, port=5001)
```

## 📝 Development Notes

### Code Quality
- Clean, readable code with comprehensive comments
- Consistent naming conventions throughout
- Proper error handling and validation
- Security best practices implemented

### Performance Considerations
- Database queries optimized with proper indexing
- Pagination implemented to handle large datasets
- Efficient many-to-many relationship handling
- Minimal database calls per page load

### Future Enhancements
- User authentication system
- Image upload for albums and artists
- Rating and review system
- Advanced search filters
- Export functionality (CSV, PDF)
- API for mobile app integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is created for educational purposes as part of a web development assignment.

---

**Built with ❤️ using Flask, PostgreSQL, and modern web technologies**