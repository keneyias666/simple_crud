# CRUD Application - Product Management System

# FOR SQLITE AND QUERIES AND ALL

sqlite3 crud.db
.databases (to verify)
CREATE TABLE table_name ( column1 datatype, column2 datatype);
FOREIGN KEY (trackartist) REFERENCES artist (artistid);
DROP TABLE table_name;
.quit

CREATING VENV IN PYTHON

python -m venv venv
cd venv
cd Scripts
activate / deactivate

INSTALLING DEPENDENCIES NEEDED

pip install -r requirements.txt


A simple Flask-based CRUD (Create, Read, Update, Delete) application for managing products with a modern, responsive UI.

## Features

- ✅ Add, Edit, and Delete products
- ✅ Editable item codes
- ✅ Real-time search functionality
- ✅ Sort items by item code (ascending/descending)
- ✅ Color-coded notifications (green for success, red for errors)
- ✅ Modern, responsive UI design
- ✅ SQLite database for data storage

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/keneyias666/simple_crud.git
   cd simple_crud
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv vnv
   vnv\Scripts\activate
   
   # On Linux/Mac
   python3 -m venv vnv
   source vnv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:5000`

## Project Structure

```
crud/
├── app.py              # Main Flask application
├── dbhelper.py         # Database helper functions
├── crud.db             # SQLite database file
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   └── index.html      # Main page template
└── static/            # Static files
    ├── css/           # Stylesheets
    └── images/        # Images and logos
```

## Usage

1. **Add a Product**: Click the "➕ Add New Product" button
2. **Edit a Product**: Click the ✏️ edit button next to any product
3. **Delete a Product**: Click the 🗑️ delete button next to any product
4. **Search Products**: Use the search box to filter products in real-time
5. **Sort by Item Code**: Click the sort button (⇅) in the ITEMCODE column header

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite3
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: W3.CSS framework

## License

Copyright © 2025, University of Cebu-CCS

## Author

Developed for educational purposes.
