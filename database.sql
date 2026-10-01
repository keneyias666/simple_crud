-- =====================================================================
--  database.sql  =  CREATE THE TABLES
--  Run:   .\sqlite3.exe database.db ".read database.sql"
--
--  Find-and-replace the UPPERCASE placeholders with the names
--  from the questionnaire. Use the SAME names in config.py and the HTML.
--
--  Types:  int -> INTEGER    text -> TEXT    date -> DATE    datetime -> DATETIME
--  Add a column: copy a line.  Remove a column: delete the line.
-- =====================================================================

-- Remove old tables (TABLE 3 first, because it points to the others)
DROP TABLE IF EXISTS TABLE_THREE;
DROP TABLE IF EXISTS TABLE_TWO;
DROP TABLE IF EXISTS TABLE_ONE;

-- TABLE 1 (first master table)
CREATE TABLE TABLE_ONE (
  T1_ID     INTEGER PRIMARY KEY,
  T1_COL1   TEXT,
  T1_COL2   TEXT,
  T1_COL3   TEXT,
  T1_SEARCH TEXT                       -- inquiry 1 searches this column
);

-- TABLE 2 (second master table)
CREATE TABLE TABLE_TWO (
  T2_ID    INTEGER PRIMARY KEY,
  T2_COL1  TEXT,
  T2_COL2  TEXT,
  T2_BDATE DATE,                       -- inquiry 2 (age) uses this birth date
  T2_COL3  TEXT
);

-- TABLE 3 (transaction table, points to TABLE 1 and TABLE 2)
CREATE TABLE TABLE_THREE (
  T3_ID   INTEGER PRIMARY KEY,
  T2_ID   INTEGER REFERENCES TABLE_TWO(T2_ID),   -- inquiry 3
  T1_ID   INTEGER REFERENCES TABLE_ONE(T1_ID),   -- inquiry 4
  T3_DATE DATETIME,                              -- inquiry 5
  T3_COL1 TEXT,
  T3_COL2 TEXT
);
