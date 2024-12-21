from models import *
from flask import render_template, redirect, url_for, flash, request


def view_employees(app):
    @app.route('/view_employees')
    def view_employees():
        employees = Employee.query.all()
        return render_template('view_employees.html', employees=employees)

def add_employee(app):
    @app.route('/add_employee', methods=['GET', 'POST'])
    def add_employee():
        if request.method == 'POST':
            user_id = request.form['user_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            position = request.form['position']
            phone_number = request.form['phone_number']
            email = request.form['email']
            hire_date = request.form['hire_date']
            department = request.form['department']

            employee = Employee(user_id=user_id, first_name=first_name, last_name=last_name, position=position,
                                phone_number=phone_number, email=email, hire_date=hire_date, department=department)

            try:
                db.session.add(employee)
                db.session.commit()
                flash("Employee added successfully!", "success")
                return redirect(url_for('view_employees'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_employee.html')

def edit_employee(app):
    @app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
    def edit_employee(employee_id):
        employee = Employee.query.get_or_404(employee_id)

        if request.method == 'POST':
            employee.user_id = request.form['user_id']
            employee.first_name = request.form['first_name']
            employee.last_name = request.form['last_name']
            employee.position = request.form['position']
            employee.phone_number = request.form['phone_number']
            employee.email = request.form['email']
            employee.hire_date = request.form['hire_date']
            employee.department = request.form['department']

            try:
                db.session.commit()
                flash("Employee updated successfully!", "success")
                return redirect(url_for('view_employees'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_employee.html', employee=employee)

def delete_employee(app):
    @app.route('/delete_employee/<int:employee_id>', methods=['POST'])
    def delete_employee(employee_id):
        employee = Employee.query.get_or_404(employee_id)
        try:
            db.session.delete(employee)
            db.session.commit()
            flash("Employee deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_employees'))