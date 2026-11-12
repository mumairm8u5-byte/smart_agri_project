from datetime import date, datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


def pk():
    return db.Column(db.Integer, primary_key=True)


def fk(table):
    return db.Column(db.Integer, db.ForeignKey(table + ".id"))


def text(size=100):
    return db.Column(db.String(size))


def num():
    return db.Column(db.Float)


def whole():
    return db.Column(db.Integer)


def day():
    return db.Column(db.Date, default=date.today)


def stamp():
    return db.Column(db.DateTime, default=datetime.now)


# ---------- Users ----------
class Role(db.Model):
    id = pk()
    name = db.Column(db.String(50), unique=True)


class User(UserMixin, db.Model):
    id = pk()
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = fk("role")
    created_at = stamp()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserProfile(db.Model):
    id = pk()
    user_id = fk("user")
    full_name = text()
    phone = text(30)
    address = text(200)


class Notification(db.Model):
    id = pk()
    user_id = fk("user")
    message = text(255)
    is_read = db.Column(db.Boolean, default=False)
    created_at = stamp()


# ---------- Farm layout ----------
class Farm(db.Model):
    id = pk()
    name = text()
    location = text()
    size_hectares = num()
    owner_id = fk("user")


class SoilType(db.Model):
    id = pk()
    name = text()
    description = text(255)


class Field(db.Model):
    id = pk()
    farm_id = fk("farm")
    name = text()
    area_hectares = num()
    soil_type = text()
    soil_type_id = fk("soil_type")


class SoilTest(db.Model):
    id = pk()
    field_id = fk("field")
    test_date = day()
    ph_level = num()
    nitrogen = num()
    phosphorus = num()
    potassium = num()


class Greenhouse(db.Model):
    id = pk()
    farm_id = fk("farm")
    name = text()
    capacity = whole()
    temperature_target = num()


# ---------- Crop lifecycle ----------
class Crop(db.Model):
    id = pk()
    name = text()
    category = text()
    growth_days = whole()


class CropVariety(db.Model):
    id = pk()
    crop_id = fk("crop")
    name = text()
    yield_per_hectare = num()


class Planting(db.Model):
    id = pk()
    field_id = fk("field")
    crop_id = fk("crop")
    plant_date = day()
    area_planted = num()
    status = text(30)


class GrowthStage(db.Model):
    id = pk()
    planting_id = fk("planting")
    stage_name = text()
    start_date = day()
    notes = text(255)


class Harvest(db.Model):
    id = pk()
    planting_id = fk("planting")
    harvest_date = day()
    quantity_kg = num()
    quality_grade = text(10)


class PestIssue(db.Model):
    id = pk()
    planting_id = fk("planting")
    pest_name = text()
    severity = text(30)
    reported_on = day()


# ---------- Resources ----------
class Seed(db.Model):
    id = pk()
    crop_id = fk("crop")
    brand = text()
    stock_kg = num()


class Fertilizer(db.Model):
    id = pk()
    name = text()
    npk_ratio = text(30)
    stock_kg = num()


class Pesticide(db.Model):
    id = pk()
    name = text()
    active_ingredient = text()
    stock_liters = num()


class FertilizerApplication(db.Model):
    id = pk()
    field_id = fk("field")
    fertilizer_id = fk("fertilizer")
    applied_on = day()
    amount_kg = num()


class PesticideApplication(db.Model):
    id = pk()
    field_id = fk("field")
    pesticide_id = fk("pesticide")
    applied_on = day()
    amount_liters = num()


# ---------- Field operations ----------
class Worker(db.Model):
    id = pk()
    farm_id = fk("farm")
    name = text()
    job_title = text()
    daily_wage = num()


class Task(db.Model):
    id = pk()
    field_id = fk("field")
    worker_id = fk("worker")
    title = text()
    due_date = day()
    status = text(30)


class WorkLog(db.Model):
    id = pk()
    task_id = fk("task")
    worker_id = fk("worker")
    hours = num()
    log_date = day()


class Inspection(db.Model):
    id = pk()
    field_id = fk("field")
    inspector_id = fk("user")
    inspection_date = day()
    result = text(255)


# ---------- IoT and weather ----------
class Sensor(db.Model):
    id = pk()
    field_id = fk("field")
    sensor_type = text(50)
    model_name = text()
    is_active = db.Column(db.Boolean, default=True)


class SensorReading(db.Model):
    id = pk()
    sensor_id = fk("sensor")
    value = num()
    unit = text(20)
    read_at = stamp()


class WeatherStation(db.Model):
    id = pk()
    farm_id = fk("farm")
    name = text()
    latitude = num()
    longitude = num()


class WeatherRecord(db.Model):
    id = pk()
    station_id = fk("weather_station")
    temperature = num()
    humidity = num()
    rainfall_mm = num()
    recorded_at = stamp()


class Alert(db.Model):
    id = pk()
    sensor_id = fk("sensor")
    message = text(255)
    level = text(30)
    created_at = stamp()


# ---------- Irrigation ----------
class WaterSource(db.Model):
    id = pk()
    farm_id = fk("farm")
    name = text()
    source_type = text(50)
    capacity_liters = num()


class IrrigationSystem(db.Model):
    id = pk()
    field_id = fk("field")
    water_source_id = fk("water_source")
    system_type = text(50)
    status = text(30)


class IrrigationSchedule(db.Model):
    id = pk()
    system_id = fk("irrigation_system")
    start_time = text(20)
    duration_minutes = whole()
    days_of_week = text(50)


class WaterUsage(db.Model):
    id = pk()
    system_id = fk("irrigation_system")
    usage_date = day()
    liters_used = num()


# ---------- Equipment ----------
class Equipment(db.Model):
    id = pk()
    farm_id = fk("farm")
    name = text()
    equipment_type = text(50)
    status = text(30)


class MaintenanceRecord(db.Model):
    id = pk()
    equipment_id = fk("equipment")
    service_date = day()
    description = text(255)
    cost = num()


class FuelLog(db.Model):
    id = pk()
    equipment_id = fk("equipment")
    log_date = day()
    liters = num()
    cost = num()


# ---------- Supply chain ----------
class Supplier(db.Model):
    id = pk()
    name = text()
    contact_email = text()
    phone = text(30)


class Warehouse(db.Model):
    id = pk()
    farm_id = fk("farm")
    name = text()
    capacity_kg = num()


class InventoryItem(db.Model):
    id = pk()
    warehouse_id = fk("warehouse")
    supplier_id = fk("supplier")
    item_name = text()
    quantity = num()


class Customer(db.Model):
    id = pk()
    name = text()
    email = text()
    city = text()


class SalesOrder(db.Model):
    id = pk()
    customer_id = fk("customer")
    order_date = day()
    status = text(30)


class SalesOrderItem(db.Model):
    id = pk()
    order_id = fk("sales_order")
    crop_id = fk("crop")
    quantity_kg = num()
    price_per_kg = num()


# ---------- Finance ----------
class Expense(db.Model):
    id = pk()
    farm_id = fk("farm")
    description = text(200)
    amount = num()
    expense_date = day()


class Income(db.Model):
    id = pk()
    farm_id = fk("farm")
    source = text(200)
    amount = num()
    income_date = day()


class Budget(db.Model):
    id = pk()
    farm_id = fk("farm")
    year = whole()
    category = text()
    planned_amount = num()
