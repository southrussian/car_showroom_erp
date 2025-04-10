from models import *
from flask import render_template, redirect, url_for, flash, request, session


def consultations_routes(app):
    @app.route('/view_consultations')
    def view_consultations():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        consultations = Consultation.query.options(
            db.joinedload(Consultation.client),
            db.joinedload(Consultation.employee)
        ).all()
        return render_template('view_consultations.html', consultations=consultations)

    @app.route('/add_consultation', methods=['GET', 'POST'])
    def add_consultation():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        if request.method == 'POST':
            client_id = request.form['client_id']
            consultation_date = datetime.strptime(request.form['consultation_date'], '%Y-%m-%dT%H:%M')
            employee_id = request.form['employee_id']
            description = request.form.get('description', '')

            consultation = Consultation(
                client_id=client_id,
                consultation_date=consultation_date,
                employee_id=employee_id,
                description=description
            )

            try:
                db.session.add(consultation)
                db.session.commit()
                flash("Консультация успешно добавлена", "success")
                return redirect(url_for('view_consultations'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        clients = Client.query.all()
        employees = Employee.query.all()
        return render_template('add_consultation.html', clients=clients, employees=employees)

    @app.route('/edit_consultation/<int:consultation_id>', methods=['GET', 'POST'])
    def edit_consultation(test_drive_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        consultation = Consultation.query.get_or_404(test_drive_id)

        if request.method == 'POST':
            consultation.client_id = request.form['client_id']
            consultation.consultation_date = datetime.strptime(request.form['consultation_date'], '%Y-%m-%dT%H:%M')
            consultation.employee_id = request.form['employee_id']
            consultation.description = request.form.get('description', '')

            try:
                db.session.commit()
                flash("Данные консультации успешно изменены", "success")
                return redirect(url_for('view_consultations'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        clients = Client.query.all()
        employees = Employee.query.all()
        return render_template('edit_consultation.html',
                               consultation=consultation,
                               clients=clients,
                               employees=employees)

    @app.route('/delete_consultation/<int:consultation_id>', methods=['POST'])
    def delete_consultation(consultation_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        consultation = Consultation.query.get_or_404(consultation_id)
        try:
            db.session.delete(consultation)
            db.session.commit()
            flash("Данные консультации успешно удалены", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_consultation'))
