# Skills Test CRUD System (Flask + SQLite)

A simple menu website with add, search/update, search/delete, view, and 5 inquiries. Every result shows `COUNT(*)`.
It is set up for the **Clinic Consultations Logging System**.

**You only edit 2 files:**

| File | What it is |
| --- | --- |
| `clinic.sql` | **The database.** Table names and column names. |
| `config.py` | **The website words.** Menu names and labels. |

The column names must be the **same** in both files.

---

## 1. Download the project (clone)

Open **PowerShell** and type:

```powershell
cd $HOME\Desktop
git clone https://github.com/keneyias666/simple_crud.git
cd simple_crud
```

If the test says the folder name must be your family name:

```powershell
cd $HOME\Desktop
Rename-Item simple_crud YourFamilyName
cd YourFamilyName
```

No Git? Open the GitHub page → **Code** → **Download ZIP** → extract it → open PowerShell inside the folder.

---

## 2. Install (one time)

```powershell
python -m venv vnv
.\vnv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- If `python` is not found, use `py` instead.
- If `Activate.ps1` is blocked, run this once, then try again:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## 3. Create the tables

```powershell
.\sqlite3.exe clinic.db ".read clinic.sql"
```

Optional, to add practice data:

```powershell
.\sqlite3.exe clinic.db ".read sample_data.sql"
```

Check the result:

```powershell
.\sqlite3.exe clinic.db ".tables"
```

---

## 4. Run the website

```powershell
python app.py
```

Open **http://127.0.0.1:5000**. Stop it with **Ctrl+C**.

---

## 5. How to make tables (for any system)

A table looks like this:

```sql
CREATE TABLE tablename (
  idColumn   INTEGER PRIMARY KEY,
  column2    TEXT,
  column3    TEXT
);
```

A column that points to another table:

```sql
  otherID INTEGER REFERENCES othertable(otherID),
```

Types to use:

| Sheet says | Write |
| --- | --- |
| int | `INTEGER` |
| text | `TEXT` |
| date | `DATE` |
| datetime | `DATETIME` |
| PK | `INTEGER PRIMARY KEY` |
| FK | `INTEGER REFERENCES table(column)` |

`clinic.sql` has 3 tables:

- **TABLE 1**: first master table (Doctor)
- **TABLE 2**: second master table (Patient, which has a birth date)
- **TABLE 3**: transaction table (Consultation, which points to table 1 and table 2 and has a date)

---

## 6. Change to a different system (step by step)

Example: the sheet says **Library**, with tables **Book**, **Borrower**, and **Loan**.

### Step 1: Edit `clinic.sql`

Rename the tables and columns:

```sql
DROP TABLE IF EXISTS loan;
DROP TABLE IF EXISTS borrower;
DROP TABLE IF EXISTS book;

-- TABLE 1
CREATE TABLE book (
  bookID     INTEGER PRIMARY KEY,
  bookTitle  TEXT,
  bookAuthor TEXT,
  bookGenre  TEXT
);

-- TABLE 2
CREATE TABLE borrower (
  brwID    INTEGER PRIMARY KEY,
  brwFName TEXT,
  brwLName TEXT,
  brwBDate DATE,
  brwTelNo TEXT
);

-- TABLE 3
CREATE TABLE loan (
  loanID   INTEGER PRIMARY KEY,
  brwID    INTEGER REFERENCES borrower(brwID),
  bookID   INTEGER REFERENCES book(bookID),
  loanDate DATETIME,
  remarks  TEXT
);
```

### Step 2: Edit `config.py`

Change the words in the `# CHANGE` lines. Each table has a block like this:

```python
{
    "key": "book",                 # short name, lowercase
    "table": "book",               # same as in clinic.sql
    "pk": "bookID",                # the PRIMARY KEY column
    "singular": "Book",
    "plural": "Books",
    "menu": "Books Management",    # text on the menu
    "fields": [
        {"name": "bookID",     "label": "Book ID",     "input": "number"},
        {"name": "bookTitle",  "label": "Book Title",  "input": "text"},
        {"name": "bookAuthor", "label": "Book Author", "input": "text"},
        {"name": "bookGenre",  "label": "Book Genre",  "input": "text", "inquiry": "text"},
    ],
},
```

What to write in each field:

| Key | Meaning |
| --- | --- |
| `name` | Column name. **Must match `clinic.sql`.** |
| `label` | Words shown on the page |
| `input` | `number`, `text`, `date`, `datetime-local`, or `textarea` (long text) |
| `"inquiry": "text"` | Put on **one** column of TABLE 1. Inquiry 1 searches it. |
| `"inquiry": "age"` | Put on the **birth date** of TABLE 2. Inquiry 2 uses it. |
| `"inquiry": "date"` | Put on the **date** of TABLE 3. Inquiry 5 uses it. |
| `"fk": "book"` | Put on TABLE 3 columns that point to another table. Use that table's `key`. |

TABLE 3 example:

```python
"fields": [
    {"name": "loanID",   "label": "Loan Number",    "input": "number"},
    {"name": "brwID",    "label": "Borrower ID",    "input": "number", "fk": "borrower"},
    {"name": "bookID",   "label": "Book ID",        "input": "number", "fk": "book"},
    {"name": "loanDate", "label": "Loan Date/Time", "input": "datetime-local", "inquiry": "date"},
    {"name": "remarks",  "label": "Remarks",        "input": "textarea"},
],
```

Also change `SYSTEM` (system name) and `INQUIRY` (the 5 inquiry sentences) at the top and bottom of `config.py`.

### Step 3: Rebuild and run

```powershell
.\sqlite3.exe clinic.db ".read clinic.sql"
python app.py
```

If something does not match, the website shows a red message saying exactly which table or column is missing.

---

## 7. Database queries

Open sqlite:

```powershell
.\sqlite3.exe clinic.db
```

All of these are in `queries.sql`. Change the names and values to match your tables.

```sql
-- Add
INSERT INTO doctor VALUES (1006, 'Rosa', 'Cruz', 'Cebu City', 'Neurology');

-- Search
SELECT * FROM doctor WHERE docID = 1006;

-- Update
UPDATE doctor SET docAddress = 'Lahug' WHERE docID = 1006;

-- Delete
DELETE FROM doctor WHERE docID = 1006;

-- View with COUNT
SELECT COUNT(*) AS total FROM doctor;
SELECT * FROM doctor;

-- Inquiry 1: by text
SELECT COUNT(*) AS total FROM doctor WHERE docSpecial = 'Cardiology';

-- Inquiry 2: age range
SELECT COUNT(*) AS total FROM patient
WHERE (strftime('%Y','now') - strftime('%Y', patBDate)) BETWEEN 20 AND 40;

-- Inquiry 3: by patient ID
SELECT COUNT(*) AS total FROM consultation WHERE patID = 2001;

-- Inquiry 4: by doctor ID
SELECT COUNT(*) AS total FROM consultation WHERE docID = 1001;

-- Inquiry 5: date range
SELECT COUNT(*) AS total FROM consultation
WHERE date(consultDate) BETWEEN '2026-01-01' AND '2026-03-31';
```

The inquiry 2 query only subtracts years, so it can be off by one before someone's birthday. The website uses the exact age.

Useful sqlite commands:

| Command | Does |
| --- | --- |
| `.tables` | List tables |
| `.schema` | Show how the tables were made |
| `.headers on` and `.mode column` | Show results as a readable table |
| `.read file.sql` | Run a file |
| `.quit` | Exit |

---

## 8. If something goes wrong

| Problem | Fix |
| --- | --- |
| Red "Database not ready" message | Run `.\sqlite3.exe clinic.db ".read clinic.sql"`, then reload the page |
| It says a column is missing | The name in `config.py` is different from `clinic.sql`. Make them the same. |
| `No module named flask` | Run `.\vnv\Scripts\Activate.ps1`, then `pip install -r requirements.txt` |
| Cannot delete a Doctor or Patient | A Consultation still uses it. Delete the Consultation first. |
| Database is locked | Close sqlite (`.quit`) and stop the app (Ctrl+C), then try again |

---

## 9. Save your changes to GitHub

```powershell
git add .
git commit -m "my changes"
git push
```
