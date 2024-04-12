from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

class AddItemForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired(), Length(min=2, max=75)])
  price = DecimalField('Price (Numbers only)', validators=[DataRequired()], render_kw={'type': 'number'})
  submit = SubmitField('Add')

class EditItemForm(FlaskForm):
  title = StringField('Title', validators=[])
  price = DecimalField('Price', validators=[], render_kw={'type': 'number'})
  date = DateField('Date', validators=[])
  submit = SubmitField('Edit')

class AddPaidMoneyForm(FlaskForm):
  amount = DecimalField('Amount', validators=[DataRequired()], render_kw={'type': 'number'})
  submit = SubmitField('Add')