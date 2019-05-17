from flask import abort, render_template
from flask_login import current_user, login_required

from . import home
from ..models import Department, Employee, Child

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    manage = Department.query.filter_by(manager=current_user.id).first()

    return render_template('home/dashboard.html', manage=manage, title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    employees = Employee.query.all()
    employees_no = len(employees)
    departments = Department.query.all()
    departments_no = len(departments)
    children = Child.query.all()
    children_no = len(children)
    return render_template('home/admin_dashboard.html', employees_no=employees_no, departments_no=departments_no,
                             children_no=children_no, title="Admin Dashboard")
