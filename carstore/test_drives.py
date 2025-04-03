from models import *
from flask import render_template, redirect, url_for, flash, request, session


def test_drives_routes(app):
    @app.route('/view_test_drives')
    def view_test_drives():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        test_drives = TestDrive.query.all()
        return render_template('view_test_drives.html', test_drives=test_drives)

    @app.route('/add_test_drive', methods=['GET', 'POST'])
    def add_test_drive():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        if request.method == 'POST':
            client_id = request.form['client_id']
            car_id = request.form['car_id']
            test_drive_date = request.form['test_drive_date']
            employee_id = request.form['employee_id']
            feedback = request.form['feedback']
            rating = request.form['rating']

            test_drive = TestDrive(client_id=client_id, car_id=car_id, test_drive_date=test_drive_date,
                                   employee_id=employee_id, feedback=feedback, rating=rating)

            try:
                db.session.add(test_drive)
                db.session.commit()
                flash("Test drive added successfully!", "success")
                return redirect(url_for('view_test_drives'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_test_drive.html')

    @app.route('/edit_test_drive/<int:test_drive_id>', methods=['GET', 'POST'])
    def edit_test_drive(test_drive_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        test_drive = TestDrive.query.get_or_404(test_drive_id)

        if request.method == 'POST':
            test_drive.client_id = request.form['client_id']
            test_drive.car_id = request.form['car_id']
            test_drive.test_drive_date = request.form['test_drive_date']
            test_drive.employee_id = request.form['employee_id']
            test_drive.feedback = request.form['feedback']
            test_drive.rating = request.form['rating']

            try:
                db.session.commit()
                flash("Test drive updated successfully!", "success")
                return redirect(url_for('view_test_drives'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_test_drive.html', test_drive=test_drive)

    @app.route('/delete_test_drive/<int:test_drive_id>', methods=['POST'])
    def delete_test_drive(test_drive_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        test_drive = TestDrive.query.get_or_404(test_drive_id)
        try:
            db.session.delete(test_drive)
            db.session.commit()
            flash("Test drive deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_test_drives'))
