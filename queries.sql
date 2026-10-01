-- =====================================================================
--  queries.sql  =  QUERIES TO COPY AND PASTE
--  Open:  .\sqlite3.exe clinic.db
--  Paste one query at a time. Change the table names, column names,
--  and the values to match your database.
-- =====================================================================

.headers on
.mode column

-- ---------- ADD ----------
INSERT INTO doctor VALUES (1006, 'Rosa', 'Cruz', '7 Banilad Rd, Cebu City', 'Neurology');

-- ---------- SEARCH ----------
SELECT * FROM doctor WHERE docID = 1006;

-- ---------- UPDATE ----------
UPDATE doctor SET docAddress = '9 Lahug, Cebu City' WHERE docID = 1006;

-- ---------- DELETE ----------
DELETE FROM doctor WHERE docID = 1006;

-- ---------- VIEW (with COUNT) ----------
SELECT COUNT(*) AS total FROM doctor;
SELECT * FROM doctor;

-- ---------- INQUIRY 1: doctors with a specialization ----------
SELECT COUNT(*) AS total FROM doctor WHERE docSpecial = 'Cardiology';
SELECT * FROM doctor WHERE docSpecial = 'Cardiology';

-- ---------- INQUIRY 2: patients from age 20 to 40 ----------
SELECT COUNT(*) AS total FROM patient
WHERE (strftime('%Y','now') - strftime('%Y', patBDate)) BETWEEN 20 AND 40;
SELECT * FROM patient
WHERE (strftime('%Y','now') - strftime('%Y', patBDate)) BETWEEN 20 AND 40;

-- ---------- INQUIRY 3: consultations of a patient ID ----------
SELECT COUNT(*) AS total FROM consultation WHERE patID = 2001;
SELECT * FROM consultation WHERE patID = 2001;

-- ---------- INQUIRY 4: consultations of a doctor ID ----------
SELECT COUNT(*) AS total FROM consultation WHERE docID = 1001;
SELECT * FROM consultation WHERE docID = 1001;

-- ---------- INQUIRY 5: consultations from date to date ----------
SELECT COUNT(*) AS total FROM consultation
WHERE date(consultDate) BETWEEN '2026-01-01' AND '2026-03-31';
SELECT * FROM consultation
WHERE date(consultDate) BETWEEN '2026-01-01' AND '2026-03-31';
