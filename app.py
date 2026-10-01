"""
Routes stay the same for every questionnaire. Edit config.py to rename the system
and the database.
"""

from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

import config
import dbhelper

app = Flask(__name__)
app.secret_key = "local-skills-test"
_ready = False


def ensure_db():
    global _ready
    if not _ready:
        dbhelper.init_db()
        _ready = True


@app.before_request
def _open_db():
    ensure_db()


@app.context_processor
def inject_shell():
    return {
        "system": config.SYSTEM,
        "inquiry": config.INQUIRY,
        "db_missing": dbhelper.what_is_missing(),
        "nav": config.navigation(),
        "labels": {entity["key"]: entity["singular"] for entity in config.entities()},
        "input_value": input_value,
    }


def input_value(record, field):
    if not record:
        return ""
    raw = record.get(field["name"])
    if raw is None:
        return ""
    text = str(raw).strip()
    if field["input"] == "datetime-local":
        return text.replace(" ", "T")[:16]
    if field["input"] == "date":
        return text[:10]
    return text


def _whole_number(raw, label):
    raw = (raw or "").strip()
    if raw == "":
        return None, f"Enter {label}."
    if not raw.isdigit():
        return None, f"{label} must be a whole number."
    return int(raw), None


def _date_text(raw, label):
    raw = (raw or "").strip()
    if raw == "":
        return None, f"Enter {label}."
    try:
        datetime.strptime(raw, "%Y-%m-%d")
    except ValueError:
        return None, f"{label} must be a valid date."
    return raw, None


def parse_form(entity, form):
    data = {}
    for field in entity["fields"]:
        raw = (form.get(field["name"]) or "").strip()
        label = field["label"]
        if raw == "":
            return None, f"Enter {label}."
        if field["input"] == "number":
            number, error = _whole_number(raw, label)
            if error:
                return None, error
            data[field["name"]] = number
        elif field["input"] == "date":
            day, error = _date_text(raw, label)
            if error:
                return None, error
            data[field["name"]] = day
        elif field["input"] == "datetime-local":
            normalized = raw.replace("T", " ")
            if len(normalized) == 16:
                normalized += ":00"
            try:
                datetime.strptime(normalized[:19], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None, f"{label} must be a valid date and time."
            data[field["name"]] = normalized[:16]
        else:
            data[field["name"]] = raw
        if field.get("fk"):
            parent = config.entity_by_key(field["fk"])
            if not dbhelper.get_one(parent, data[field["name"]]):
                return None, f"Select an existing {parent['singular']}."
    return data, None


def _load_existing(entity, raw):
    field = config.pk_field(entity)
    if field["input"] == "number":
        if not str(raw).isdigit():
            return None, f"{field['label']} must be a whole number."
        value = int(raw)
    else:
        value = str(raw).strip()
    row = dbhelper.get_one(entity, value)
    if not row:
        return None, f"No {entity['singular']} record found for {field['label']} {raw}."
    return row, None


def _load_search(entity, raw, searched, which):
    raw = (raw or "").strip()
    if searched != which:
        if raw == "":
            return None, None
        return _load_existing(entity, raw)
    if raw == "":
        return None, f"Enter {config.pk_field(entity)['label']} to search."
    return _load_existing(entity, raw)


@app.route("/")
def menu():
    ready = dbhelper.tables_ready()
    cards = []
    for entity in config.entities():
        cards.append({
            "key": entity["key"],
            "href": url_for("manage", key=entity["key"]),
            "title": entity["menu"],
            "text": f"Add, search, update, delete, and view {entity['plural'].lower()}.",
            "count": dbhelper.count_records(entity["table"]) if ready else "—",
            "caption": "COUNT(*)",
        })
    cards.append({
        "key": "inquiry",
        "href": url_for("inquiry"),
        "title": config.INQUIRY["menu"],
        "text": config.INQUIRY["card"],
        "count": len(config.inquiry_panels()),
        "caption": "searches",
    })
    return render_template("menu.html", cards=cards, active="menu", tables_ready=ready)


@app.route("/manage/<key>", methods=["GET"])
def manage(key):
    entity = config.entity_by_key(key)
    if not entity:
        abort(404)
    if not dbhelper.tables_ready():
        return render_template(
            f"{key}.html",
            entity=entity,
            titles=config.action_titles(entity),
            pk_field=config.pk_field(entity),
            all_rows=[],
            total=0,
            choices={},
            names={},
            update_record=None,
            delete_record=None,
            update_id="",
            delete_id="",
            active=key,
            tables_ready=False,
        )
    update_id = request.args.get("update_id", "")
    delete_id = request.args.get("delete_id", "")
    searched = request.args.get("searched", "")
    update_record, update_error = _load_search(entity, update_id, searched, "update")
    delete_record, delete_error = _load_search(entity, delete_id, searched, "delete")
    if update_error or delete_error:
        if update_error:
            flash(update_error, "error")
        if delete_error:
            flash(delete_error, "error")
        args = {}
        if update_record is not None:
            args["update_id"] = update_id
        if delete_record is not None:
            args["delete_id"] = delete_id
        return redirect(url_for("manage", key=key, **args))
    choices = {}
    for field in entity["fields"]:
        if field.get("fk"):
            choices[field["name"]] = dbhelper.choice_list(field["fk"])
    return render_template(
        f"{key}.html",
        entity=entity,
        titles=config.action_titles(entity),
        pk_field=config.pk_field(entity),
        all_rows=dbhelper.fetch_all(entity),
        total=dbhelper.count_records(entity["table"]),
        choices=choices,
        names=dbhelper.lookup_names(),
        update_record=update_record,
        delete_record=delete_record,
        update_id=update_id,
        delete_id=delete_id,
        active=key,
        tables_ready=True,
    )


@app.route("/manage/<key>/save", methods=["POST"])
def save_record(key):
    entity = config.entity_by_key(key)
    if not entity:
        abort(404)
    if not dbhelper.tables_ready():
        flash("Create the tables first: .\\sqlite3.exe database.db \".read database.sql\"", "error")
        return redirect(url_for("manage", key=key))
    data, error = parse_form(entity, request.form)
    if error:
        flash(error, "error")
        return redirect(url_for("manage", key=key))
    if request.form.get("mode") == "update":
        old_raw = (request.form.get("old_pk") or "").strip()
        pk = config.pk_field(entity)
        if pk["input"] == "number":
            if not old_raw.isdigit():
                flash(f"Enter {pk['label']}.", "error")
                return redirect(url_for("manage", key=key))
            old_pk = int(old_raw)
        else:
            old_pk = old_raw
        ok, error = dbhelper.update_record(entity, old_pk, data)
        flash(error or f"{entity['singular']} {data[entity['pk']]} updated.", "error" if error else "success")
    else:
        ok, error = dbhelper.insert_record(entity, data)
        flash(error or f"{entity['singular']} {data[entity['pk']]} added.", "error" if error else "success")
    return redirect(url_for("manage", key=key))


@app.route("/manage/<key>/delete", methods=["POST"])
def remove_record(key):
    entity = config.entity_by_key(key)
    if not entity:
        abort(404)
    if not dbhelper.tables_ready():
        flash("Create the tables first: .\\sqlite3.exe database.db \".read database.sql\"", "error")
        return redirect(url_for("manage", key=key))
    raw = (request.form.get("pk") or "").strip()
    pk_field = config.pk_field(entity)
    if pk_field["input"] == "number":
        if not raw.isdigit():
            flash(f"Enter {pk_field['label']}.", "error")
            return redirect(url_for("manage", key=key))
        pk = int(raw)
    else:
        pk = raw
    ok, error = dbhelper.delete_record(entity, pk)
    flash(error or f"{entity['singular']} {pk} deleted.", "error" if error else "success")
    return redirect(url_for("manage", key=key))


def _run_inquiry(kind, args):
    parent_a, parent_b = config.PARENTS[0], config.PARENTS[1]
    transaction = config.TRANSACTION
    if kind == "text":
        field = config.marked_field(parent_a, "text")
        value = (args.get("value") or "").strip()
        if not value:
            return None, f"Enter {field['label']}."
        total, rows = dbhelper.search_text(parent_a, field["name"], value)
        return _pack(kind, total, rows, config.columns_of(parent_a), f"{field['label']}: {value}"), None
    if kind == "age":
        start, start_error = _whole_number(args.get("age_from"), config.INQUIRY["age_from"])
        end, end_error = _whole_number(args.get("age_to"), config.INQUIRY["age_to"])
        if start_error or end_error:
            return None, start_error or end_error
        if start > end:
            return None, f"{config.INQUIRY['age_from']} must be less than or equal to {config.INQUIRY['age_to']}."
        field = config.marked_field(parent_b, "age")
        total, rows = dbhelper.search_age(parent_b, field["name"], start, end)
        columns = config.columns_of(parent_b, [{"name": "age", "label": "Age", "fk": None}])
        return _pack(kind, total, rows, columns, f"Age {start} to {end}"), None
    if kind in ("by_a", "by_b"):
        parent = parent_a if kind == "by_a" else parent_b
        field = config.fk_field_for(parent["key"])
        value, error = _whole_number(args.get("value"), field["label"])
        if error and config.pk_field(parent)["input"] != "number":
            value = (args.get("value") or "").strip()
            error = None if value else f"Enter {field['label']}."
        if error:
            return None, error
        total, rows = dbhelper.search_id(field["name"], value)
        return _pack(kind, total, rows, config.columns_of(transaction), f"{field['label']}: {value}"), None
    if kind == "date":
        start, start_error = _date_text(args.get("date_from"), config.INQUIRY["date_from"])
        end, end_error = _date_text(args.get("date_to"), config.INQUIRY["date_to"])
        if start_error or end_error:
            return None, start_error or end_error
        if start > end:
            return None, f"{config.INQUIRY['date_from']} must be on or before {config.INQUIRY['date_to']}."
        field = config.marked_field(transaction, "date")
        total, rows = dbhelper.search_dates(field["name"], start, end)
        return _pack(kind, total, rows, config.columns_of(transaction), f"{start} to {end}"), None
    return None, "Choose a search from the menu."


def _pack(kind, total, rows, columns, summary):
    return {"kind": kind, "count": total, "rows": rows, "columns": columns, "summary": summary}


@app.route("/inquiry")
def inquiry():
    kind = (request.args.get("kind") or "").strip()
    result = None
    ready = dbhelper.tables_ready()
    if kind and not ready:
        flash("Create the tables first: .\\sqlite3.exe database.db \".read database.sql\"", "error")
    elif kind:
        result, error = _run_inquiry(kind, request.args)
        if error:
            flash(error, "error")
            result = None
    return render_template(
        "inquiry.html",
        panels=config.inquiry_panels(),
        result=result,
        kind=kind,
        filters=request.args,
        names=dbhelper.lookup_names() if ready else {},
        active="inquiry",
        tables_ready=ready,
    )


@app.errorhandler(404)
def missing(_error):
    flash("That page is not on the menu.", "error")
    return redirect(url_for("menu"))


if __name__ == "__main__":
    ensure_db()
    missing = dbhelper.what_is_missing()
    if missing:
        print("Database not ready. Missing:", ", ".join(missing))
        print('Run:  .\\sqlite3.exe database.db ".read database.sql"')
    print("Open http://127.0.0.1:5000")
    app.run(debug=True)
