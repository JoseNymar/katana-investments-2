from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    salary = db.Column(db.Integer, index=True)
    phone = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    dnumber = db.Column(db.Integer, db.ForeignKey('departments.id'))
    children = db.relationship('Child', backref='parent')
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.id)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    dname = db.Column(db.String(40), unique=True)
    budget = db.Column(db.Integer)
    manager=db.Column(db.Integer, unique=True)
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Child(db.Model):
    """
    Create a Child table
    """

    __tablename__ = 'children'

    name = db.Column(db.String(40), primary_key=True)
    age = db.Column(db.Integer)
    enumber = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    # employees = db.relationship('Employee', backref='role',
    #                             lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
