from models import *
from flask import render_template, redirect, url_for, flash, request, session


def view_maintenance_schedules(app):
    @app.route('/view_maintenance_schedules')
    def view_maintenance_schedules():
        maintenance_schedules = MaintenanceSchedule.query.all()
        return render_template('view_maintenance_schedules.html', maintenance_schedules=maintenance_schedules)

def add_maintenance_schedule(app):
    @app.route('/add_maintenance_schedule', methods=['GET', 'POST'])
    def add_maintenance_schedule():
        if request.method == 'POST':
            car_id = request.form['car_id']
            scheduled_date = request.form['scheduled_date']
            service_type = request.form['service_type']
            description = request.form['description']
            mechanic_id = request.form['mechanic_id']

            maintenance_schedule = MaintenanceSchedule(car_id=car_id, scheduled_date=scheduled_date,
                                                      service_type=service_type, description=description,
                                                      mechanic_id=mechanic_id)

            try:
                db.session.add(maintenance_schedule)
                db.session.commit()
                flash("Maintenance schedule added successfully!", "success")
                return redirect(url_for('view_maintenance_schedules'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_maintenance_schedule.html')

def edit_maintenance_schedule(app):
    @app.route('/edit_maintenance_schedule/<int:schedule_id>', methods=['GET', 'POST'])
    def edit_maintenance_schedule(schedule_id):
        maintenance_schedule = MaintenanceSchedule.query.get_or_404(schedule_id)

        if request.method == 'POST':
            maintenance_schedule.car_id = request.form['car_id']
            maintenance_schedule.scheduled_date = request.form['scheduled_date']
            maintenance_schedule.service_type = request.form['service_type']
            maintenance_schedule.description = request.form['description']
            maintenance_schedule.mechanic_id = request.form['mechanic_id']

            try:
                db.session.commit()
                flash("Maintenance schedule updated successfully!", "success")
                return redirect(url_for('view_maintenance_schedules'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_maintenance_schedule.html', maintenance_schedule=maintenance_schedule)

def delete_maintenance_schedule(app):
    @app.route('/delete_maintenance_schedule/<int:schedule_id>', methods=['POST'])
    def delete_maintenance_schedule(schedule_id):
        maintenance_schedule = MaintenanceSchedule.query.get_or_404(schedule_id)
        try:
            db.session.delete(maintenance_schedule)
            db.session.commit()
            flash("Maintenance schedule deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_maintenance_schedules'))