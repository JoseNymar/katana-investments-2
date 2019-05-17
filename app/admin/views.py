from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, EmployeeAssignForm, ChildForm
from .. import db
from ..models import Department, Employee, Child


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


"""""
----------------------------------------------------------------------
    Department Views
----------------------------------------------------------------------
"""""

#list all department
@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")

#add a department
@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        manager=form.manager.data
        department = Department(dname=form.name.data,
                                budget=form.budget.data,
                                manager=manager.id)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")

#edit department
@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        manager=form.manager.data
        department.dname = form.name.data
        department.budget = form.budget.data
        department.manager = manager.id
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.budget.data = department.budget
    form.name.data = department.dname
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")

#delete department
@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

"""""
----------------------------------------------------------------------
    Child Views
----------------------------------------------------------------------
"""""

#list all children
@admin.route('/children')
@login_required
def list_children():
    check_admin()
    """
    List all children
    """
    children = Child.query.all()
    return render_template('admin/children/children.html',
                           children=children, title='Children')

#add a child
@admin.route('/children/add', methods=['GET', 'POST'])
@login_required
def add_child():
    """
    Add a child to the database
    """
    check_admin()

    add_child = True

    form = ChildForm()
    if form.validate_on_submit():
        child = Child(name=form.name.data,
                    age=form.age.data)

        try:
            # add child to the database
            db.session.add(child)
            db.session.commit()
            #adding the QuerySelectFild:form.parent.data
            child = Child.query.get_or_404(form.name.data)
            child.parent=form.parent.data
            #notice the add() instead of just committing
            db.session.add(child)
            db.session.commit()
            flash('You have successfully added a new child.')
        except:
            # in case role name already exists
            flash('Error: child name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_children'))

    # load role template
    return render_template('admin/children/child.html', add_child=add_child,
                           form=form, title='Add Child')

#edit a child
@admin.route('/children/edit/<name>', methods=['GET', 'POST'])
@login_required
def edit_child(name):
    """
    Edit a child
    """
    check_admin()

    add_child = False

    child = Child.query.get_or_404(name)
    form = ChildForm(obj=child)
    if form.validate_on_submit():
        child.name = form.name.data
        child.age = form.age.data
        db.session.add(child)
        db.session.commit()
        flash('You have successfully edited the child.')

        # redirect to the children page
        return redirect(url_for('admin.list_children'))

    form.age.data = child.age
    form.name.data = child.name
    return render_template('admin/children/child.html', add_child=add_child,
                           form=form, title="Edit Child")

#delete a child
@admin.route('/children/delete/<name>', methods=['GET', 'POST'])
@login_required
def delete_child(name):
    """
    Delete a child from the database
    """
    check_admin()

    child = Child.query.get_or_404(name)
    db.session.delete(child)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_children'))

    return render_template(title="Delete Child")


"""""
----------------------------------------------------------------------
    Employee Views
----------------------------------------------------------------------
"""""
#list all employees
@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()
    
    employees = Employee.query.all()
    
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')

#assign department and salary
@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a salary to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.salary=form.salary.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and salary')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')

#delete an employee
@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete an employ from the database
    """
    check_admin()

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the employee.')

    # redirect to the roles page
    return redirect(url_for('admin.list_employees'))

    return render_template(title="Delete Employee")