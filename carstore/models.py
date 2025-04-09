from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="employee")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)


class Car(db.Model):
    __tablename__ = 'cars'
    car_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    color = db.Column(db.String(20))
    price = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Integer)
    status = db.Column(db.String(20), nullable=False)
    fuel_type = db.Column(db.String(20))
    transmission = db.Column(db.String(20))
    body_type = db.Column(db.String(20))


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    expected_delivery_date = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False)

    car = db.relationship('Car', backref='orders')
    client = db.relationship('Client', backref='orders')


class Sale(db.Model):
    __tablename__ = 'sales'
    sale_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.now)
    sale_price = db.Column(db.Float, nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    payment_method = db.Column(db.String(20))

    order = db.relationship('Order', backref='sales')
    salesperson = db.relationship('Employee', backref='sales')


class ServiceType(db.Model):
    __tablename__ = 'service_types'
    type_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), nullable=False)


class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    request_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    requested_date = db.Column(db.DateTime, default=datetime.now)
    service_type = db.Column(db.Integer, db.ForeignKey('service_types.type_id'), nullable=False)
    description = db.Column(db.Text)

    client = db.relationship('Client', backref='service_requests')
    service_type_rel = db.relationship('ServiceType', backref='service_requests')


class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('service_requests.request_id'), nullable=False)
    service_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)


class Employee(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)

    user = db.relationship('User', backref=db.backref('employee', uselist=False))


class TestDrive(db.Model):
    __tablename__ = 'test_drives'
    test_drive_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    test_drive_date = db.Column(db.DateTime, default=datetime.now)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)

    client = db.relationship('Client', backref='test_drives')
    car = db.relationship('Car', backref='test_drives')
    employee = db.relationship('Employee', backref='test_drives')


class Consultation(db.Model):
    __tablename__ = 'consultations'
    consultation_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    consultation_date = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.Text)

    client = db.relationship('Client', backref='consultations')
    employee = db.relationship('Employee', backref='consultations')
