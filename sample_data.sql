-- =====================================================================
--  sample_data.sql  =  ADD PRACTICE ROWS  (run after clinic.sql)
--  Run:   .\sqlite3.exe clinic.db ".read sample_data.sql"
--  Add table 1 and table 2 rows before table 3.
-- =====================================================================

INSERT INTO doctor VALUES (1001, 'Maria', 'Santos',    '12 Junquera St, Cebu City', 'Cardiology');
INSERT INTO doctor VALUES (1002, 'Juan',  'Dela Cruz', '45 Colon St, Cebu City',    'Pediatrics');
INSERT INTO doctor VALUES (1003, 'Ana',   'Reyes',     '8 Osmena Blvd, Cebu City',  'Dermatology');
INSERT INTO doctor VALUES (1004, 'Pedro', 'Lim',       '90 Mango Ave, Cebu City',   'Cardiology');
INSERT INTO doctor VALUES (1005, 'Liza',  'Gomez',     '3 Escario St, Cebu City',   'Orthopedics');

INSERT INTO patient VALUES (2001, 'Andres', 'Ramos',      '1958-12-12', '09170001001');
INSERT INTO patient VALUES (2002, 'Bea',    'Navarro',    '1980-05-01', '09170001002');
INSERT INTO patient VALUES (2003, 'Carlo',  'Villanueva', '1996-08-20', '09170001003');
INSERT INTO patient VALUES (2004, 'Diana',  'Uy',         '2004-01-15', '09170001004');
INSERT INTO patient VALUES (2005, 'Elena',  'Tan',        '2014-11-02', '09170001005');
INSERT INTO patient VALUES (2006, 'Felix',  'Ong',        '2018-03-10', '09170001006');

INSERT INTO consultation VALUES (3001, 2001, 1001, '2026-01-12 09:30', 'Elevated blood pressure',      'Amlodipine 5mg daily');
INSERT INTO consultation VALUES (3002, 2001, 1004, '2026-03-02 14:00', 'Chest discomfort on exertion', 'ECG ordered');
INSERT INTO consultation VALUES (3003, 2005, 1002, '2026-02-18 10:15', 'Acute cough',                  'Salbutamol syrup for 5 days');
INSERT INTO consultation VALUES (3004, 2003, 1003, '2025-11-05 16:45', 'Acne vulgaris',                'Adapalene cream at night');
INSERT INTO consultation VALUES (3005, 2004, 1005, '2026-06-21 08:00', 'Right ankle sprain',           'Rest, ice, and ibuprofen');
INSERT INTO consultation VALUES (3006, 2002, 1001, '2026-08-09 11:20', 'High cholesterol',             'Atorvastatin 20mg at bedtime');
INSERT INTO consultation VALUES (3007, 2006, 1002, '2026-09-01 13:40', 'Routine well-child visit',     'Multivitamin daily');
INSERT INTO consultation VALUES (3008, 2003, 1001, '2025-06-14 15:10', 'Palpitations',                 'Observe and return if needed');
