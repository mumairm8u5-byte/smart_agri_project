from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, FloatField,
                     IntegerField, SelectField, DateField, SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                NumberRange, ValidationError)
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("That username is already taken.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("That email is already registered.")


class FarmForm(FlaskForm):
    name = StringField("Farm Name", validators=[DataRequired(), Length(max=100)])
    location = StringField("Location", validators=[DataRequired(), Length(max=100)])
    size_hectares = FloatField("Size (hectares)", validators=[DataRequired(), NumberRange(min=0.1)])
    submit = SubmitField("Save")


class FieldForm(FlaskForm):
    farm_id = SelectField("Farm", coerce=int)
    name = StringField("Field Name", validators=[DataRequired(), Length(max=100)])
    area_hectares = FloatField("Area (hectares)", validators=[DataRequired(), NumberRange(min=0.1)])
    soil_type = StringField("Soil Type", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Save")


class CropForm(FlaskForm):
    name = StringField("Crop Name", validators=[DataRequired(), Length(max=100)])
    category = StringField("Category", validators=[DataRequired(), Length(max=100)])
    growth_days = IntegerField("Growth Days", validators=[DataRequired(), NumberRange(min=1, max=800)])
    submit = SubmitField("Save")


class EquipmentForm(FlaskForm):
    name = StringField("Equipment Name", validators=[DataRequired(), Length(max=100)])
    equipment_type = StringField("Type", validators=[DataRequired(), Length(max=50)])
    status = SelectField("Status", choices=[("Working", "Working"), ("In Repair", "In Repair"), ("Retired", "Retired")])
    submit = SubmitField("Save")


class ExpenseForm(FlaskForm):
    description = StringField("Description", validators=[DataRequired(), Length(max=200)])
    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=0.01)])
    expense_date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Save")
