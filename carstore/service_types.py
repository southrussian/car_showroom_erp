from models import *
from flask import request, render_template, redirect, url_for, session, flash


def service_types_routes(app):
    @app.route('/view_service_types')
    def view_service_types():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        service_types = ServiceType.query.all()
        return render_template('view_service_types.html', service_types=service_types)

    @app.route('/add_service_type', methods=['GET', 'POST'])
    def add_service_type():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        if request.method == 'POST':
            service_name = request.form['service_name']

            service_type = ServiceType(service_name=service_name)

            try:
                db.session.add(service_type)
                db.session.commit()
                flash("Service type added successfully!", "success")
                return redirect(url_for('view_service_types'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        return render_template('add_service_type.html')

    @app.route('/edit_service_type/<int:type_id>', methods=['GET', 'POST'])
    def edit_service_type(type_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        service_type = ServiceType.query.get_or_404(type_id)

        if request.method == 'POST':
            service_type.service_name = request.form['service_name']

            try:
                db.session.commit()
                flash("Service type updated successfully!", "success")
                return redirect(url_for('view_service_types'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        return render_template('edit_service_type.html', service_type=service_type)

    @app.route('/delete_service_type/<int:type_id>', methods=['POST'])
    def delete_service_type(type_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        service_type = ServiceType.query.get_or_404(type_id)
        try:
            db.session.delete(service_type)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_service_types'))
