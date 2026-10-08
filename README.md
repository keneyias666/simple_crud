# Empty skills-test template (Flask + SQLite)

This is a **blank** CRUD website with a menu. There are 3 empty tables and 5 inquiry searches.
Every list shows `COUNT(*)`. Names are placeholders. When you get the questionnaire, you rename them.

Repo: https://github.com/keneyias666/simple_crud

---

## 1. Download (clone)

1. Install Git if needed: https://git-scm.com/download/win
2. Open **PowerShell**.
3. Go to your Desktop:

```powershell
cd $HOME\Desktop
```

4. Download the project:

```powershell
git clone https://github.com/keneyias666/simple_crud.git
cd simple_crud
```

5. If the sheet says the folder must be your family name:

```powershell
cd $HOME\Desktop
Rename-Item simple_crud YourFamilyName
cd YourFamilyName
```

No Git? On GitHub click **Code → Download ZIP**, extract it, then open PowerShell inside that folder.

Already cloned? Update it:

```powershell
cd $HOME\Desktop\simple_crud
git pull
```

---

## 2. One-time Python setup

Need Python 3.8+ (tick **Add python.exe to PATH** when installing).

```powershell
python -m venv vnv
.\vnv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- If `python` is not found, use `py` instead of `python`.
- If `Activate.ps1` is blocked, run this once, then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

You should see `(vnv)` at the start of the line.

---

## 3. Create the empty tables

The website does **not** create tables by itself. You create them from `database.sql`.

```powershell
.\sqlite3.exe database.db ".read database.sql"
```

Check:

```powershell
.\sqlite3.exe database.db ".tables"
```

You should see:

```text
TABLE_ONE    TABLE_THREE  TABLE_TWO
```

All counts are 0 until you add rows (from the website or from `sample_data.sql`).

---

## 4. Run the website

```powershell
python app.py
```

Open **http://127.0.0.1:5000**

Stop with **Ctrl+C**.

### What you should see

Top bar on every page:

- Menu
- Table One Management
- Table Two Management
- Table Three Transaction Management
- Inquiry

| Page | What to do |
| --- | --- |
| Table One / Two / Three | 1 Add, 2 Search then Update, 3 Search then Delete, 4 View (`COUNT(*)`) |
| Inquiry | 5 searches. Each result shows `COUNT(*)` |

On Table Three, the two ID boxes are drop-downs. Add Table One and Table Two rows first.

You cannot delete a Table One / Table Two row while a Table Three row still uses that ID.

---

## 5. If the questionnaire is a different system

The app always has this shape. Only the **names** change.

| Slot | Placeholder names | Meaning |
| --- | --- | --- |
| TABLE 1 | `TABLE_ONE`, `T1_ID`, `T1_COL1` … `T1_SEARCH` | First master table. Inquiry 1 searches `T1_SEARCH`. |
| TABLE 2 | `TABLE_TWO`, `T2_ID` … `T2_BDATE` | Second master table. Inquiry 2 uses birth date `T2_BDATE`. |
| TABLE 3 | `TABLE_THREE`, `T3_ID`, `T2_ID`, `T1_ID`, `T3_DATE` | Transaction. Points to TABLE 1 and TABLE 2. Inquiry 5 uses `T3_DATE`. |

**Do not change:** `t1` `t2` `t3` and the URLs `/manage/t1` `/manage/t2` `/manage/t3` `/inquiry`.
**Do change:** the words on the page and every `TABLE_ONE` / `T1_ID` style name.

You edit **the same names** in these files:

1. `database.sql`
2. `config.py`
3. HTML in `templates/`
4. (optional) `queries.sql` and `sample_data.sql`

Then rebuild:

```powershell
.\sqlite3.exe database.db ".read database.sql"
python app.py
```

If a name does not match, the page shows a red **Database not ready. Missing: ...** line.

### 5.1 `database.sql` (the tables)

Open `database.sql`. Replace `TABLE_ONE`, `TABLE_TWO`, `TABLE_THREE` and every column name.

Types from the sheet:

| Sheet says | Write |
| --- | --- |
| int | `INTEGER` |
| text | `TEXT` |
| date | `DATE` |
| datetime | `DATETIME` |
| PK | `INTEGER PRIMARY KEY` |
| FK | `INTEGER REFERENCES other_table(other_id)` |

Add a column: copy a line. Remove a column: delete the line. Keep TABLE 3 last in `CREATE` and first in `DROP`.

### 5.2 `config.py` (save and search)

Replace the same table and column names. Also change:

| Setting | What it is |
| --- | --- |
| `SYSTEM["name"]` | System name |
| `SYSTEM["database"]` | Database name on the sheet |
| `table` | Must equal the SQL table name |
| `pk` | Must equal the primary key column |
| `singular` / `plural` / `menu` | Words in messages |
| `fields` → `name` | Must equal the SQL column name |
| `fields` → `label` | Words in error messages |
| `fields` → `input` | `number`, `text`, `date`, `datetime-local`, or `textarea` |
| `"inquiry": "text"` | Keep on the TABLE 1 search column |
| `"inquiry": "age"` | Keep on the TABLE 2 birth-date column |
| `"inquiry": "date"` | Keep on the TABLE 3 date column |
| `"fk": "t1"` / `"fk": "t2"` | Keep on TABLE 3 ID columns. Do not change `t1`/`t2`. |

Do **not** change `"key": "t1"` `"t2"` `"t3"`.

### 5.3 HTML files (what you see)

Each HTML file has a **CHANGE / KEEP** comment at the top. Read that first.

| File | Page | What to change |
| --- | --- | --- |
| `templates/base.html` | Top bar on every page | `SYSTEM NAME` and the 4 link **words**. Keep the `href="/manage/t1"` etc. |
| `templates/menu.html` | Home menu | Link **words**. Keep the `href`. |
| `templates/t1.html` | TABLE 1 | Labels, headings, `name="T1_..."`, `r['T1_...']` |
| `templates/t2.html` | TABLE 2 | Same, with `T2_...` |
| `templates/t3.html` | TABLE 3 | Same, plus `choices.get('T2_ID')` / `choices.get('T1_ID')` |
| `templates/inquiry.html` | 5 searches | Headings, labels, `r['...']` table cells |
| `templates/_t3_rows.html` | TABLE 3 result table | Header words and `r['T3_...']` |
| `static/css/app.css` | Look | Colors and sizes only |

Example of one field on `t1.html`:

```html
<label>Table One ID</label>                 <!-- CHANGE: any words from the sheet -->
<input type="number" name="T1_ID" required> <!-- CHANGE: name="T1_ID" to the real column -->
<td>{{ r['T1_ID'] }}</td>                   <!-- CHANGE: T1_ID to the same column -->
```

**Leave these `name=` values alone** (they are not database columns):

- `mode` `old_pk` `pk` `searched` `update_id` `delete_id`
- Inquiry: `kind` `value` `age_from` `age_to` `date_from` `date_to`
- Inquiry `kind` values: `text` `age` `by_b` `by_a` `date`

### 5.4 Add or remove a column

Do all three:

1. `database.sql` — add or delete the column line.
2. `config.py` — add or delete the `{ "name": "...", "label": "...", "input": "..." }` line.
3. The table’s HTML file — add or delete the `<label>` + `<input>` in **Add** and **Update**, and the `<th>` + `<td>` in **Delete** and **View**. For TABLE 3 also edit `_t3_rows.html`.

### 5.5 Queries (optional)

`queries.sql` has COUNT searches you can paste into sqlite. Rename the tables/columns the same way.

```powershell
.\sqlite3.exe database.db
.read queries.sql
.quit
```

`sample_data.sql` is empty on purpose. Uncomment and rename the INSERT lines if you want practice rows.

---

## 6. Skills-test day (short)

1. Login as the sheet says (Local Admin).
2. `git clone https://github.com/keneyias666/simple_crud.git` then rename the folder if needed.
3. `python -m venv vnv` → `.\vnv\Scripts\Activate.ps1` → `pip install -r requirements.txt`
4. Rename placeholders in `database.sql`, `config.py`, and `templates/` to match the sheet.
5. `.\sqlite3.exe database.db ".read database.sql"`
6. `python app.py` → http://127.0.0.1:5000
7. Add a few rows, then show Add / Search-Update / Search-Delete / View / 5 inquiries.

---

## 7. Troubleshooting

| Problem | Fix |
| --- | --- |
| Red “Database not ready” | `.\sqlite3.exe database.db ".read database.sql"` |
| Missing column | Same spelling in `database.sql`, `config.py`, and the HTML `name=` / `r['...']` |
| `python` not found | Use `py` |
| `No module named flask` | Activate `vnv`, then `pip install -r requirements.txt` |
| `Activate.ps1` blocked | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `sqlite3.exe` not found | Run the command inside the project folder |
| Cannot delete a TABLE 1/2 row | Delete the TABLE 3 rows that use that ID first |
| Port 5000 in use | Stop the other `python app.py` with Ctrl+C |
| Inquiry 1 is 0 | Exact match. Type the full value, not a partial word |

---

## 8. Push your own changes (optional)

```powershell
git add .
git commit -m "describe the change"
git push
```

## 9. Must Note This on SQLITE3 Queries!!!

"SAVING DATABASE QUERIES"

sqlite> .save 'my_database.db'

"CREATING TABLE WITH FOREIGN KEYS"

CREATE TABLE DOCTOR (
    doctor_id TEXT,  -- :x: Missing "PRIMARY KEY" or "UNIQUE" keyword here!
    name TEXT
);

CREATE TABLE CONSULTATION (
    id INTEGER PRIMARY KEY,
    doc_id TEXT,
    FOREIGN KEY(doc_id) REFERENCES DOCTOR(doctor_id)
);

"TURNING ON FOREIGN_KEY ON SQLITE3"
sqlite3 your_database.db
sqlite> PRAGMA foreign_keys = ON;