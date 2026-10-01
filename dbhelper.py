"""
Runs SQL against clinic.db. Tables come from clinic.sql; names come from config.py.
Every list and every inquiry runs SELECT COUNT(*).
"""

import os
import sqlite3

import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, config.SYSTEM["db_file"])


def q(name):
    if not config._NAME.fullmatch(name or ""):
        raise config.ConfigError(f"Invalid SQL name '{name}'.")
    return f'"{name}"'


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def query(sql, params=()):
    conn = connect()
    try:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def scalar(sql, params=()):
    return query(sql, params)[0]["total"]


def execute(sql, params=()):
    conn = connect()
    try:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.rowcount
    except sqlite3.IntegrityError:
        conn.rollback()
        raise
    finally:
        conn.close()


def count_records(table):
    return scalar(f"SELECT COUNT(*) AS total FROM {q(table)}")


def count_filtered(table, where_sql, params):
    return scalar(f"SELECT COUNT(*) AS total FROM {q(table)} {where_sql}", params)


def missing_columns(conn):
    """Return 'table.column' names from config.py that the database does not have."""
    missing = []
    for entity in config.entities():
        have = {row[1].lower() for row in conn.execute(f"PRAGMA table_info({q(entity['table'])})")}
        if not have:
            missing.append(entity["table"])
            continue
        for field in entity["fields"]:
            if field["name"].lower() not in have:
                missing.append(f"{entity['table']}.{field['name']}")
    return missing


def init_db():
    """Open the database file. Tables are created from clinic.sql, not here."""
    config.validate()
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = connect()
    conn.close()


def tables_ready():
    return not what_is_missing()


def what_is_missing():
    conn = connect()
    try:
        return missing_columns(conn)
    finally:
        conn.close()


def fetch_all(entity):
    return query(
        f"SELECT * FROM {q(entity['table'])} ORDER BY {q(entity['pk'])}"
    )


def get_one(entity, pk):
    rows = query(
        f"SELECT * FROM {q(entity['table'])} WHERE {q(entity['pk'])} = ?",
        (pk,),
    )
    return rows[0] if rows else None


def choice_list(parent_key):
    parent = config.entity_by_key(parent_key)
    return [
        {"id": row[parent["pk"]], "label": config.display_name(parent, row)}
        for row in fetch_all(parent)
    ]


def lookup_names():
    names = {}
    for parent in config.PARENTS:
        names[parent["key"]] = {
            row[parent["pk"]]: config.display_name(parent, row) for row in fetch_all(parent)
        }
    return names


def _friendly(exc, entity):
    text = str(exc).lower()
    if "foreign key" in text:
        return f"Choose a {config.PARENTS[0]['singular']} and a {config.PARENTS[1]['singular']} that already exist."
    return f"That {entity['singular']} ID already exists."


def insert_record(entity, data):
    cols = [field["name"] for field in entity["fields"]]
    sql = (
        f"INSERT INTO {q(entity['table'])} ({', '.join(q(col) for col in cols)}) "
        f"VALUES ({', '.join('?' for _ in cols)})"
    )
    try:
        execute(sql, [data[col] for col in cols])
    except sqlite3.IntegrityError as exc:
        return False, _friendly(exc, entity)
    return True, None


def update_record(entity, old_pk, data):
    assignments = ", ".join(f"{q(field['name'])} = ?" for field in entity["fields"])
    values = [data[field["name"]] for field in entity["fields"]]
    values.append(old_pk)
    sql = f"UPDATE {q(entity['table'])} SET {assignments} WHERE {q(entity['pk'])} = ?"
    try:
        changed = execute(sql, values)
    except sqlite3.IntegrityError as exc:
        return False, _friendly(exc, entity)
    if changed == 0:
        return False, f"No {entity['singular']} record found."
    return True, None


def delete_record(entity, pk):
    if entity["key"] != config.TRANSACTION["key"]:
        for field in config.TRANSACTION["fields"]:
            if field.get("fk") != entity["key"]:
                continue
            total = count_filtered(config.TRANSACTION["table"], f"WHERE {q(field['name'])} = ?", (pk,))
            if total:
                noun = config.TRANSACTION["singular"] if total == 1 else config.TRANSACTION["plural"]
                verb = "uses" if total == 1 else "use"
                return False, f"Cannot delete this {entity['singular']}. {total} {noun} still {verb} this ID."
    try:
        changed = execute(
            f"DELETE FROM {q(entity['table'])} WHERE {q(entity['pk'])} = ?",
            (pk,),
        )
    except sqlite3.IntegrityError:
        return False, f"Cannot delete this {entity['singular']}. Another record still uses this ID."
    if changed == 0:
        return False, f"No {entity['singular']} record found."
    return True, None


def age_expression(column_name):
    column = q(column_name)
    return (
        "(CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', "
        + column
        + ") AS INTEGER) - (CASE WHEN strftime('%m-%d', 'now') < strftime('%m-%d', "
        + column
        + ") THEN 1 ELSE 0 END))"
    )


def search_text(entity, field_name, value):
    where = f"WHERE LOWER({q(field_name)}) = LOWER(?)"
    total = count_filtered(entity["table"], where, (value,))
    rows = query(
        f"SELECT * FROM {q(entity['table'])} {where} ORDER BY {q(entity['pk'])}",
        (value,),
    )
    return total, rows


def search_age(entity, field_name, start, end):
    expr = age_expression(field_name)
    where = f"WHERE {expr} BETWEEN ? AND ?"
    total = count_filtered(entity["table"], where, (start, end))
    rows = query(
        f"SELECT *, {expr} AS age FROM {q(entity['table'])} {where} ORDER BY age, {q(entity['pk'])}",
        (start, end),
    )
    return total, rows


def search_id(field_name, value):
    entity = config.TRANSACTION
    where = f"WHERE {q(field_name)} = ?"
    total = count_filtered(entity["table"], where, (value,))
    rows = query(
        f"SELECT * FROM {q(entity['table'])} {where} ORDER BY {q(entity['pk'])}",
        (value,),
    )
    return total, rows


def search_dates(field_name, start, end):
    entity = config.TRANSACTION
    where = f"WHERE date({q(field_name)}) BETWEEN date(?) AND date(?)"
    total = count_filtered(entity["table"], where, (start, end))
    rows = query(
        f"SELECT * FROM {q(entity['table'])} {where} ORDER BY {q(field_name)}",
        (start, end),
    )
    return total, rows
