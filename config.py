# =====================================================================
#  config.py  =  THE COLUMN LIST THE APP SAVES AND SEARCHES
#
#  Find-and-replace the UPPERCASE placeholders (TABLE_ONE, T1_ID, ...)
#  with the names from the questionnaire. Use the SAME names in
#  database.sql and in templates/*.html.
#
#  Do NOT change the "key" values (t1, t2, t3). They are the page
#  addresses (/manage/t1) and the HTML file names (t1.html).
#
#  Field options:
#    "name"     column name in database.sql                (MUST MATCH)
#    "label"    words used in messages                     (anything)
#    "input"    "text" | "number" | "date" | "datetime-local" | "textarea"
#    "inquiry"  "text" -> inquiry 1 searches this column   (TABLE 1)
#               "age"  -> inquiry 2 uses this birth date   (TABLE 2)
#               "date" -> inquiry 5 uses this date         (TABLE 3)
#    "fk"       on TABLE 3: which table this column points to ("t1" or "t2")
# =====================================================================

import re
from datetime import datetime

SYSTEM = {
    "name": "SYSTEM NAME",                  # CHANGE: system name on the sheet
    "database": "DATABASE NAME",            # CHANGE: database name on the sheet
    "db_file": "database.db",               # keep
    "tagline": "",
    "school": "University of Cebu (UC-Main) — College of Computer Studies",
}

PARENTS = [
    # ---------------- TABLE 1 (first master table) -----------------------
    {
        "key": "t1",                         # do not change
        "table": "TABLE_ONE",                # CHANGE: table name
        "pk": "T1_ID",                       # CHANGE: primary key column
        "singular": "Table One",             # CHANGE: used in messages
        "plural": "Table Ones",
        "menu": "Table One Management",
        "fields": [
            {"name": "T1_ID", "label": "Table One ID", "input": "number"},
            {"name": "T1_COL1", "label": "Table One Column 1", "input": "text"},
            {"name": "T1_COL2", "label": "Table One Column 2", "input": "text"},
            {"name": "T1_COL3", "label": "Table One Column 3", "input": "text"},
            {"name": "T1_SEARCH", "label": "Table One Search Column", "input": "text", "inquiry": "text"},
        ],
    },
    # ---------------- TABLE 2 (second master table) ----------------------
    {
        "key": "t2",                         # do not change
        "table": "TABLE_TWO",
        "pk": "T2_ID",
        "singular": "Table Two",
        "plural": "Table Twos",
        "menu": "Table Two Management",
        "fields": [
            {"name": "T2_ID", "label": "Table Two ID", "input": "number"},
            {"name": "T2_COL1", "label": "Table Two Column 1", "input": "text"},
            {"name": "T2_COL2", "label": "Table Two Column 2", "input": "text"},
            {"name": "T2_BDATE", "label": "Table Two Birth Date", "input": "date", "inquiry": "age"},
            {"name": "T2_COL3", "label": "Table Two Column 3", "input": "text"},
        ],
    },
]

# ---------------- TABLE 3 (transaction table) ----------------------------
TRANSACTION = {
    "key": "t3",                             # do not change
    "table": "TABLE_THREE",
    "pk": "T3_ID",
    "singular": "Table Three",
    "plural": "Table Threes",
    "menu": "Table Three Transaction Management",
    "record": "transaction record",
    "fields": [
        {"name": "T3_ID", "label": "Table Three ID", "input": "number"},
        {"name": "T2_ID", "label": "Table Two ID", "input": "number", "fk": "t2"},
        {"name": "T1_ID", "label": "Table One ID", "input": "number", "fk": "t1"},
        {"name": "T3_DATE", "label": "Table Three Date/Time", "input": "datetime-local", "inquiry": "date"},
        {"name": "T3_COL1", "label": "Table Three Column 1", "input": "textarea"},
        {"name": "T3_COL2", "label": "Table Three Column 2", "input": "textarea"},
    ],
}

INQUIRY = {
    "menu": "Inquiry",
    "card": "Five searches.",
    "note": "Each result uses COUNT(*).",
    "age_from": "From age",
    "age_to": "To age",
    "date_from": "From date",
    "date_to": "To date",
    "prompts": {
        "text": "Inquiry 1",
        "age": "Inquiry 2",
        "by_b": "Inquiry 3",
        "by_a": "Inquiry 4",
        "date": "Inquiry 5",
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
