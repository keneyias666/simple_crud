# CRUD Application

# FOR Virtual Environment Setup

- irm https://claude.ai/install.ps1 | iex
- and also download ollama (irm https://ollama.com/install.ps1 | iex) or download manually and make sure you connect your device as well,
  by selecting a deepseek cloud agent, and will reroute you to connect the device.
- Download GIT as well (git clone <https://github.com/keneyias666/simple_crud>)
- After installing the claude.ai to windows make sure  you go to
  (Edit the System and Environment Variables) check the system variables and look for path and add the path,
  that you installed the claude in.
- ollama launch claude --model minimax-m2.5:cloud


# FOR SQLITE AND QUERIES AND ALL

sqlite3 crud.db
.databases (to verify)
CREATE TABLE table_name ( column1 datatype, column2 datatype);
FOREIGN KEY (trackartist) REFERENCES artist (artistid);
DROP TABLE table_name;
.quit

- DATA TYPES (INT)
INT
INTEGER
TINYINT
SMALLINT
MEDIUMINT
BIGINT
UNSIGNED BIG INT
INT2
INT8

- DATA TYPES (CHAR)
CHARACTER(20)
VARCHAR(255)
VARYING CHARACTER(255)
NCHAR(55)
NATIVE CHARACTER(70)
NVARCHAR(100)
TEXT
CLOB

- DATA TYPES (REAL)
REAL
DOUBLE
DOUBLE PRECISION
FLOAT

- DATA TYPES (NUMERIC)
NUMERIC
DECIMAL(10,5)
BOOLEAN
DATE
DATETIME


# CREATING VENV IN PYTHON

python -m venv venv
cd venv
cd Scripts
activate / deactivate


# INSTALLING DEPENDENCIES NEEDED!!

(pip install -r requirements.txt)
pip install flask
pip install debhelper
pip install sqlalchemy
pip install flash


# FOR CSS SETUP W3 SCHOOLS
https://www.w3schools.com/w3css/4/w3.css
https://www.w3schools.com/w3css/5/w3.css


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
