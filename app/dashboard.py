from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from app.extensions import db
from app.models import Farm, Field, Crop, Equipment, Expense

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
@login_required
def home():
    total_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0
    stats = [
        ("Farms", Farm.query.count()),
        ("Fields", Field.query.count()),
        ("Crops", Crop.query.count()),
        ("Equipment", Equipment.query.count()),
        ("Total Expenses", round(total_expenses, 2)),
        ("Database Tables", len(db.metadata.tables)),
    ]
    recent_farms = Farm.query.order_by(Farm.id.desc()).limit(5).all()
    return render_template("dashboard.html", stats=stats, recent_farms=recent_farms)
