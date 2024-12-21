from models import *
from flask import Flask, render_template, redirect, url_for, flash, session, request
import logging
from logging.handlers import RotatingFileHandler

from users import login, logout, register, view_users
from clients import view_clients, edit_client, add_client, delete_client
from cars import view_cars, edit_car, add_car, delete_car
from sales import view_sales, edit_sale, add_sale, delete_sale
from service_records import view_service_records, edit_service_record, add_service_record, delete_service_record
from employees import view_employees, edit_employee, add_employee, delete_employee
from inventory import view_inventory, edit_inventory, add_inventory, delete_inventory
from test_drives import view_test_drives, edit_test_drive, add_test_drive, delete_test_drive
from suppliers import view_suppliers, edit_supplier, add_supplier, delete_supplier
from orders import view_orders, edit_order, add_order, delete_order
from maintenance_schedules import (view_maintenance_schedules, edit_maintenance_schedule, add_maintenance_schedule,
                                   delete_maintenance_schedule)
from customer_feedbacks import (view_customer_feedback, edit_customer_feedback, add_customer_feedback,
                                delete_customer_feedback)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autosalon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'oxxxymiron'

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
file_handler = RotatingFileHandler('autosalon.log', maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
app.logger.addHandler(file_handler)

# Логирование запуска приложения
app.logger.info("Приложение запущено.")

db.init_app(app)

login(app)
logout(app)
register(app)
view_users(app)

view_clients(app)
edit_client(app)
add_client(app)
delete_client(app)

view_cars(app)
edit_car(app)
add_car(app)
delete_car(app)

view_sales(app)
edit_sale(app)
add_sale(app)
delete_sale(app)

view_service_records(app)
edit_service_record(app)
add_service_record(app)
delete_service_record(app)

view_customer_feedback(app)
edit_customer_feedback(app)
add_customer_feedback(app)
delete_customer_feedback(app)

view_orders(app)
edit_order(app)
add_order(app)
delete_order(app)

view_maintenance_schedules(app)
edit_maintenance_schedule(app)
add_maintenance_schedule(app)
delete_maintenance_schedule(app)

view_suppliers(app)
edit_supplier(app)
add_supplier(app)
delete_supplier(app)

view_test_drives(app)
edit_test_drive(app)
add_test_drive(app)
delete_test_drive(app)

view_inventory(app)
edit_inventory(app)
add_inventory(app)
delete_inventory(app)

view_employees(app)
edit_employee(app)
add_employee(app)
delete_employee(app)

@app.route('/')
def dashboard():
    if 'user_id' not in session:
        app.logger.warning("Попытка доступа к панели управления без аутентификации.")
        flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
        return redirect(url_for('login'))
    app.logger.info(f"Доступ к панели управления пользователем ID: {session['user_id']}.")
    return render_template('dashboard.html')

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f"Страница не найдена: {e}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Внутренняя ошибка сервера: {e}")
    return render_template('500.html'), 500

@app.before_request
def before_request():
    app.logger.debug(f"Запрос: {request.method} {request.url}")

@app.after_request
def after_request(response):
    app.logger.debug(f"Ответ: {response.status}")
    return response

with app.app_context():
    db.create_all()
    app.logger.info("База данных инициализирована.")

if __name__ == '__main__':
    app.logger.info("Приложение запущено в режиме отладки.")
    app.run(debug=True)
