from models import *
from flask import render_template, redirect, url_for, flash, request, session


def service_records_routes(app):
    @app.route('/view_service_records')
    def view_service_records():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        service_records = ServiceRecord.query.all()
        return render_template('view_service_records.html', service_records=service_records)

    @app.route('/add_service_record', methods=['GET', 'POST'])
    def add_service_record():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            car_id = request.form['car_id']
            service_date = request.form['service_date']
            service_type = request.form['service_type']
            description = request.form['description']
            cost = request.form['cost']
            mechanic_id = request.form['mechanic_id']

            service_record = ServiceRecord(car_id=car_id, service_date=service_date, service_type=service_type,
                                           description=description, cost=cost, mechanic_id=mechanic_id)

            try:
                db.session.add(service_record)
                db.session.commit()
                flash("Service record added successfully!", "success")
                return redirect(url_for('view_service_records'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_service_record.html')

    @app.route('/edit_service_record/<int:service_id>', methods=['GET', 'POST'])
    def edit_service_record(service_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        service_record = ServiceRecord.query.get_or_404(service_id)

        if request.method == 'POST':
            service_record.car_id = request.form['car_id']
            service_record.service_date = request.form['service_date']
            service_record.service_type = request.form['service_type']
            service_record.description = request.form['description']
            service_record.cost = request.form['cost']
            service_record.mechanic_id = request.form['mechanic_id']

            try:
                db.session.commit()
                flash("Service record updated successfully!", "success")
                return redirect(url_for('view_service_records'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_service_record.html', service_record=service_record)

    @app.route('/delete_service_record/<int:service_id>', methods=['POST'])
    def delete_service_record(service_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        service_record = ServiceRecord.query.get_or_404(service_id)
        try:
            db.session.delete(service_record)
            db.session.commit()
            flash("Service record deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_service_records'))
