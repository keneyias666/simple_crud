-- =====================================================================
--  clinic.sql  =  CREATE THE TABLES
--  Run:   .\sqlite3.exe clinic.db ".read clinic.sql"
--
--  To change the system: rename the tables and columns below,
--  then use the SAME names in config.py.
--
--  Types:  int -> INTEGER    text -> TEXT    date -> DATE    datetime -> DATETIME
-- =====================================================================

-- Remove old tables (the table with foreign keys goes first)
DROP TABLE IF EXISTS consultation;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS doctor;

-- TABLE 1
CREATE TABLE doctor (
  docID      INTEGER PRIMARY KEY,
  docFName   TEXT,
  docLName   TEXT,
  docAddress TEXT,
  docSpecial TEXT
);

-- TABLE 2
CREATE TABLE patient (
  patID    INTEGER PRIMARY KEY,
  patFName TEXT,
  patLName TEXT,
  patBDate DATE,
  patTelNo TEXT
);

-- TABLE 3 (transaction, links table 1 and table 2)
CREATE TABLE consultation (
  consultID    INTEGER PRIMARY KEY,
  patID        INTEGER REFERENCES patient(patID),
  docID        INTEGER REFERENCES doctor(docID),
  consultDate  DATETIME,
  diagnosis    TEXT,
  prescription TEXT
);
