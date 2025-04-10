from models import db, Employee, User
from flask import render_template, redirect, url_for, flash, request, session


def employees_routes(app):
    @app.route('/view_employees')
    def view_employees():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        employees = Employee.query.options(
            db.joinedload(Employee.user)
        ).all()
        return render_template('view_employees.html', employees=employees)

    @app.route('/add_employee', methods=['GET', 'POST'])
    def add_employee():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        if request.method == 'POST':
            user_id = request.form['user_id']
            first_name = request.form['first_name']
            middle_name = request.form.get('middle_name', '')
            last_name = request.form['last_name']
            position = request.form['position']
            phone_number = request.form.get('phone_number', '')
            email = request.form['email']

            employee = Employee(
                user_id=user_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                position=position,
                phone_number=phone_number,
                email=email
            )

            try:
                db.session.add(employee)
                db.session.commit()
                flash("Employee added successfully!", "success")
                return redirect(url_for('view_employees'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        users = User.query.all()
        positions = ['Manager', 'Salesperson', 'Technician', 'Administrator']
        return render_template('add_employee.html',
                               users=users,
                               positions=positions)

    @app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
    def edit_employee(employee_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        employee = Employee.query.get_or_404(employee_id)

        if request.method == 'POST':
            employee.user_id = request.form['user_id']
            employee.first_name = request.form['first_name']
            employee.middle_name = request.form.get('middle_name', '')
            employee.last_name = request.form['last_name']
            employee.position = request.form['position']
            employee.phone_number = request.form.get('phone_number', '')
            employee.email = request.form['email']

            try:
                db.session.commit()
                flash("Employee updated successfully!", "success")
                return redirect(url_for('view_employees'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        users = User.query.all()
        positions = ['Менеджер', 'Продавец', 'Инженер', 'Администратор']
        return render_template('edit_employee.html',
                               employee=employee,
                               users=users,
                               positions=positions)

    @app.route('/delete_employee/<int:employee_id>', methods=['POST'])
    def delete_employee(employee_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        employee = Employee.query.get_or_404(employee_id)
        try:
            db.session.delete(employee)
            db.session.commit()
            flash("Данные сотрудника успешно удалены!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_employees'))
