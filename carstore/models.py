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
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(150))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    preferred_contact_method = db.Column(db.String(20))


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


class Sale(db.Model):
    __tablename__ = 'sales'
    sale_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    sale_price = db.Column(db.Float, nullable=False)
    salesperson_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    payment_method = db.Column(db.String(20))
    financing_details = db.Column(db.Text)

    client = db.relationship('Client', backref='sales')
    car = db.relationship('Car', backref='sales')
    salesperson = db.relationship('Employee', backref='sales')


class ServiceRecord(db.Model):
    __tablename__ = 'service_records'
    service_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    service_date = db.Column(db.DateTime, default=datetime.utcnow)
    service_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Float, nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)

    car = db.relationship('Car', backref='service_records')
    mechanic = db.relationship('Employee', backref='service_records')


class Employee(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(50))

    user = db.relationship('User', backref=db.backref('employee', uselist=False))


class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100))
    arrival_date = db.Column(db.Date, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)

    car = db.relationship('Car', backref='inventory')
    supplier = db.relationship('Supplier', backref='inventory')


class TestDrive(db.Model):
    __tablename__ = 'test_drives'
    test_drive_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    test_drive_date = db.Column(db.DateTime, default=datetime.utcnow)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)

    client = db.relationship('Client', backref='test_drives')
    car = db.relationship('Car', backref='test_drives')
    employee = db.relationship('Employee', backref='test_drives')


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(150))


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    expected_delivery_date = db.Column(db.Date)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    car = db.relationship('Car', backref='orders')
    supplier = db.relationship('Supplier', backref='orders')


class MaintenanceSchedule(db.Model):
    __tablename__ = 'maintenance_schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)

    car = db.relationship('Car', backref='maintenance_schedule')
    mechanic = db.relationship('Employee', backref='maintenance_schedule')


class CustomerFeedback(db.Model):
    __tablename__ = 'customer_feedback'
    feedback_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    feedback_date = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text)

    client = db.relationship('Client', backref='customer_feedback')
    car = db.relationship('Car', backref='customer_feedback')
