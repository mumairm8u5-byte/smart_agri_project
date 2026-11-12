from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from app.extensions import db
from app.models import Farm, Field, Crop, Equipment, Expense
from app.forms import FarmForm, FieldForm, CropForm, EquipmentForm, ExpenseForm

crud = Blueprint("crud", __name__, url_prefix="/manage")

tables = {
    "farms": (Farm, FarmForm),
    "fields": (Field, FieldForm),
    "crops": (Crop, CropForm),
    "equipment": (Equipment, EquipmentForm),
    "expenses": (Expense, ExpenseForm),
}


def get_table(name):
    if name not in tables:
        abort(404)
    return tables[name]


def make_form(name, form_class, item=None):
    form = form_class(obj=item)
    if name == "fields":
        form.farm_id.choices = [(f.id, f.name) for f in Farm.query.all()]
    return form


@crud.route("/<name>")
@login_required
def list_items(name):
    model, form_class = get_table(name)
    columns = [c.name for c in model.__table__.columns]
    rows = []
    for item in model.query.order_by(model.id.desc()).all():
        values = [getattr(item, c) for c in columns]
        rows.append((item.id, values))
    return render_template("list.html", name=name, columns=columns, rows=rows)


@crud.route("/<name>/add", methods=["GET", "POST"])
@login_required
def add_item(name):
    model, form_class = get_table(name)
    form = make_form(name, form_class)
    if name == "fields" and not form.farm_id.choices:
        flash("Add a farm first, then you can add fields.", "error")
        return redirect(url_for("crud.list_items", name="farms"))
    if form.validate_on_submit():
        item = model()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash("Record added.", "success")
        return redirect(url_for("crud.list_items", name=name))
    return render_template("form.html", name=name, form=form, action="Add")


@crud.route("/<name>/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(name, item_id):
    model, form_class = get_table(name)
    item = model.query.get_or_404(item_id)
    form = make_form(name, form_class, item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Record updated.", "success")
        return redirect(url_for("crud.list_items", name=name))
    return render_template("form.html", name=name, form=form, action="Edit")


@crud.route("/<name>/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(name, item_id):
    model, form_class = get_table(name)
    item = model.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Record deleted.", "success")
    return redirect(url_for("crud.list_items", name=name))
