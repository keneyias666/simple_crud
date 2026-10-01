# =====================================================================
#  config.py  =  WEBSITE LABELS
#
#  Change the words between "quotes" to match the questionnaire.
#  Every "name" must be spelled exactly like the column in clinic.sql.
#
#  Field options:
#    "name"     column name in clinic.sql                  (MUST MATCH)
#    "label"    words shown beside the input box           (anything)
#    "input"    "text" | "number" | "date" | "datetime-local" | "textarea"
#    "inquiry"  "text" -> inquiry 1 searches this column   (in PARENTS[0])
#               "age"  -> inquiry 2 uses this birth date   (in PARENTS[1])
#               "date" -> inquiry 5 uses this date         (in TRANSACTION)
#    "fk"       the "key" of the table this column points to (TRANSACTION only)
# =====================================================================

import re
from datetime import datetime

# ---------------- SYSTEM -------------------------------------------------
SYSTEM = {
    "name": "Clinic Consultations Logging System",          # CHANGE: system name
    "database": "Clinic",                                    # CHANGE: database name
    "db_file": "clinic.db",                                  # sqlite file (keep)
    "tagline": "A simple Clinic Consultations Logging System.",
    "school": "University of Cebu (UC-Main) — College of Computer Studies",
}

PARENTS = [
    # ---------------- TABLE 1 (first master table) -----------------------
    {
        "key": "doctor",                     # CHANGE: short id, lowercase
        "table": "doctor",                   # CHANGE: table name in clinic.sql
        "pk": "docID",                       # CHANGE: primary key column
        "singular": "Doctor",                # CHANGE
        "plural": "Doctors",                 # CHANGE
        "menu": "Doctors Management",        # CHANGE: menu text
        "fields": [                          # CHANGE: one line per column
            {"name": "docID", "label": "Doctor's License or ID Number", "input": "number"},
            {"name": "docFName", "label": "Doctor's First Name", "input": "text"},
            {"name": "docLName", "label": "Doctor's Last Name", "input": "text"},
            {"name": "docAddress", "label": "Doctor's Address", "input": "text"},
            {"name": "docSpecial", "label": "Doctor's Specialization", "input": "text", "inquiry": "text"},
        ],
    },
    # ---------------- TABLE 2 (second master table) ----------------------
    {
        "key": "patient",
        "table": "patient",
        "pk": "patID",
        "singular": "Patient",
        "plural": "Patients",
        "menu": "Patients Management",
        "fields": [
            {"name": "patID", "label": "Patient's ID Number", "input": "number"},
            {"name": "patFName", "label": "Patient's First Name", "input": "text"},
            {"name": "patLName", "label": "Patient's Last Name", "input": "text"},
            {"name": "patBDate", "label": "Patient's Birth Date", "input": "date", "inquiry": "age"},
            {"name": "patTelNo", "label": "Patient's Telephone Number", "input": "text"},
        ],
    },
]

# ---------------- TABLE 3 (transaction table) ----------------------------
TRANSACTION = {
    "key": "consultation",
    "table": "consultation",
    "pk": "consultID",
    "singular": "Consultation",
    "plural": "Consultations",
    "menu": "Consultations Transaction Management",
    "record": "transaction record",
    "fields": [
        {"name": "consultID", "label": "Consultation Transaction Number", "input": "number"},
        {"name": "patID", "label": "Patient's ID Number", "input": "number", "fk": "patient"},
        {"name": "docID", "label": "Doctor's License or ID Number", "input": "number", "fk": "doctor"},
        {"name": "consultDate", "label": "Consultation Date/Time", "input": "datetime-local", "inquiry": "date"},
        {"name": "diagnosis", "label": "Doctor's Diagnosis Details for Patient", "input": "textarea"},
        {"name": "prescription", "label": "Doctor's Prescription Details for Patient", "input": "textarea"},
    ],
}

# ---------------- INQUIRY PAGE TEXT (copy from the questionnaire) --------
INQUIRY = {
    "menu": "Consultations Inquiry",
    "card": "Search by specialization, age, patient, doctor, or date.",
    "note": "Each result uses COUNT(*).",
    "age_from": "From age",
    "age_to": "To age",
    "date_from": "From date",
    "date_to": "To date",
    "prompts": {
        "text": "Displays all Doctors with a particular/specified specialization",
        "age": "Displays all Patients from age ___ to age ___",
        "by_b": "Displays all of consultations related to a particular/specified patient ID",
        "by_a": "Displays all of consultations related to a particular/specified doctor ID",
        "date": "Displays all Consultations from specified date ___ to date ___",
    },
}

# =====================================================================
#  Nothing below needs to change.
# =====================================================================

SEED = {}

_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_SQL = re.compile(r"[A-Za-z0-9 (),]+")
_INPUTS = {"text", "number", "date", "datetime-local", "textarea"}
_PROMPTS = ("text", "age", "by_b", "by_a", "date")


class ConfigError(Exception):
    pass


def entities():
    return [*PARENTS, TRANSACTION]


def entity_by_key(key):
    for entity in entities():
        if entity["key"] == key:
            return entity
    return None


def pk_field(entity):
    for field in entity["fields"]:
        if field["name"] == entity["pk"]:
            return field
    raise ConfigError(f"{entity['key']} pk '{entity['pk']}' is not in its fields.")


def marked_field(entity, marker):
    hits = [field for field in entity["fields"] if field.get("inquiry") == marker]
    if len(hits) != 1:
        raise ConfigError(
            f"Mark exactly one field on '{entity['key']}' with inquiry='{marker}'."
        )
    return hits[0]


def fk_field_for(parent_key):
    hits = [field for field in TRANSACTION["fields"] if field.get("fk") == parent_key]
    if len(hits) != 1:
        raise ConfigError(f"Mark exactly one transaction field with fk='{parent_key}'.")
    return hits[0]


def columns_of(entity, extra=None):
    columns = [
        {"name": field["name"], "label": field["label"], "fk": field.get("fk")}
        for field in entity["fields"]
    ]
    if extra:
        columns.extend(extra)
    return columns


def display_name(entity, row):
    parts = []
    for field in entity["fields"]:
        if field["input"] == "text" and row.get(field["name"]):
            parts.append(str(row[field["name"]]))
        if len(parts) == 2:
            break
    return " ".join(parts) if parts else str(row[entity["pk"]])


def action_titles(entity):
    word = entity.get("record", "record")
    titles = {
        "add": f"Adding a {entity['singular']} {word}",
        "update": f"Searching/Updating a {entity['singular']} {word}",
        "delete": f"Searching/Deleting a {entity['singular']} {word}",
        "view": f"Viewing of {entity['singular']} {word}s",
    }
    for key, value in (entity.get("titles") or {}).items():
        if value:
            titles[key] = value
    return titles


def navigation():
    items = [{"key": "menu", "label": "Menu", "endpoint": "menu"}]
    for entity in entities():
        items.append({"key": entity["key"], "label": entity["menu"], "endpoint": "manage"})
    items.append({"key": "inquiry", "label": INQUIRY["menu"], "endpoint": "inquiry"})
    return items


def inquiry_panels():
    parent_a, parent_b = PARENTS[0], PARENTS[1]
    text_field = marked_field(parent_a, "text")
    return [
        {
            "kind": "text",
            "title": INQUIRY["prompts"]["text"],
            "inputs": [{"name": "value", "label": text_field["label"], "type": "text"}],
        },
        {
            "kind": "age",
            "title": INQUIRY["prompts"]["age"],
            "inputs": [
                {"name": "age_from", "label": INQUIRY["age_from"], "type": "number"},
                {"name": "age_to", "label": INQUIRY["age_to"], "type": "number"},
            ],
        },
        {
            "kind": "by_b",
            "title": INQUIRY["prompts"]["by_b"],
            "inputs": [{"name": "value", "label": pk_field(parent_b)["label"], "type": "number"}],
        },
        {
            "kind": "by_a",
            "title": INQUIRY["prompts"]["by_a"],
            "inputs": [{"name": "value", "label": pk_field(parent_a)["label"], "type": "number"}],
        },
        {
            "kind": "date",
            "title": INQUIRY["prompts"]["date"],
            "inputs": [
                {"name": "date_from", "label": INQUIRY["date_from"], "type": "date"},
                {"name": "date_to", "label": INQUIRY["date_to"], "type": "date"},
            ],
        },
    ]


def _check_name(label, value):
    if not _NAME.fullmatch(value or ""):
        raise ConfigError(f"{label} '{value}' must use letters, numbers, and underscores.")


def _check_entity(entity, *, require_text=None, require_age=False, require_date=False):
    _check_name("key", entity["key"])
    _check_name("table", entity["table"])
    for word in ("singular", "plural", "menu", "pk"):
        if not str(entity.get(word, "")).strip():
            raise ConfigError(f"{entity['key']} needs a {word}.")
    if not entity["fields"]:
        raise ConfigError(f"{entity['key']} needs fields.")
    seen = set()
    for field in entity["fields"]:
        _check_name(f"{entity['key']} column", field["name"])
        if field["name"] in seen:
            raise ConfigError(f"Duplicate column {field['name']} on {entity['key']}.")
        seen.add(field["name"])
        if not str(field.get("label", "")).strip():
            raise ConfigError(f"{field['name']} needs a label.")
        if field.get("input") not in _INPUTS:
            raise ConfigError(f"{field['name']} input must be one of: {', '.join(sorted(_INPUTS))}.")
        if "sql" in field and not _SQL.fullmatch(field["sql"]):
            raise ConfigError(f"{field['name']} sql type is not a plain SQLite type.")
    pk_field(entity)
    if require_text:
        field = marked_field(entity, "text")
        if field["input"] not in ("text", "textarea"):
            raise ConfigError("The text inquiry field must use a text input.")
    if require_age:
        field = marked_field(entity, "age")
        if field["input"] != "date":
            raise ConfigError("The age inquiry field must be a date (a birth date).")
    if require_date:
        field = marked_field(entity, "date")
        if field["input"] not in ("date", "datetime-local"):
            raise ConfigError("The date inquiry field must be a date or datetime-local input.")


def validate():
    if len(PARENTS) != 2:
        raise ConfigError("Keep exactly two parents: PARENTS[0] and PARENTS[1].")
    _check_entity(PARENTS[0], require_text=True)
    _check_entity(PARENTS[1], require_age=True)
    _check_entity(TRANSACTION, require_date=True)
    keys = [entity["key"] for entity in entities()]
    tables = [entity["table"] for entity in entities()]
    if len(set(keys)) != len(keys) or len(set(tables)) != len(tables):
        raise ConfigError("Keys and table names must be unique.")
    parent_keys = {parent["key"] for parent in PARENTS}
    linked = set()
    for field in TRANSACTION["fields"]:
        if field.get("fk"):
            if field["fk"] not in parent_keys:
                raise ConfigError(f"{field['name']} fk '{field['fk']}' is not a parent key.")
            linked.add(field["fk"])
    if linked != parent_keys:
        raise ConfigError("The transaction needs one fk field for each parent.")
    for prompt in _PROMPTS:
        if not str(INQUIRY.get("prompts", {}).get(prompt, "")).strip():
            raise ConfigError(f"INQUIRY prompts['{prompt}'] is empty.")
    for word in ("menu", "card", "note", "age_from", "age_to", "date_from", "date_to"):
        if not str(INQUIRY.get(word, "")).strip():
            raise ConfigError(f"INQUIRY['{word}'] is empty.")
