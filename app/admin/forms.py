from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Department, Child, Employee


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    budget = StringField('budget', validators=[DataRequired()])
    manager = QuerySelectField(query_factory=lambda: Employee.query.all(),
                                  get_label="name" )
    submit = SubmitField('Submit')


class ChildForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    parent=QuerySelectField(query_factory=lambda: Employee.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="dname")
    salary= IntegerField('Salary', validators=[DataRequired()])
    submit = SubmitField('Submit')
