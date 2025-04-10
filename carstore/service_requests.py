from models import *
from flask import request, render_template, redirect, url_for, session, flash


def service_requests_routes(app):
    @app.route('/view_service_requests')
    def view_service_requests():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        service_requests = ServiceRequest.query.options(
            db.joinedload(ServiceRequest.client),
            db.joinedload(ServiceRequest.type)
        ).all()
        return render_template('view_service_requests.html',
                               service_requests=service_requests)

    @app.route('/add_service_request', methods=['GET', 'POST'])
    def add_service_request():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        if request.method == 'POST':
            client_id = request.form['client_id']
            service_type = request.form['service_type']
            description = request.form.get('description', '')

            service_request = ServiceRequest(
                client_id=client_id,
                service_type=service_type,
                description=description
            )

            try:
                db.session.add(service_request)
                db.session.commit()
                flash("Service request added successfully!", "success")
                return redirect(url_for('view_service_requests'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        clients = Client.query.all()
        service_types = ServiceType.query.all()
        return render_template('add_service_request.html',
                               clients=clients,
                               service_types=service_types)

    @app.route('/edit_service_request/<int:request_id>', methods=['GET', 'POST'])
    def edit_service_request(request_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        service_request = ServiceRequest.query.get_or_404(request_id)

        if request.method == 'POST':
            service_request.client_id = request.form['client_id']
            service_request.service_type = request.form['service_type']
            service_request.description = request.form.get('description', '')

            try:
                db.session.commit()
                flash("Service request updated successfully!", "success")
                return redirect(url_for('view_service_requests'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        clients = Client.query.all()
        service_types = ServiceType.query.all()
        return render_template('edit_service_request.html',
                               service_request=service_request,
                               clients=clients,
                               service_types=service_types)

    @app.route('/delete_service_request/<int:request_id>', methods=['POST'])
    def delete_service_request(request_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        service_request = ServiceRequest.query.get_or_404(request_id)
        try:
            db.session.delete(service_request)
            db.session.commit()
            flash("Данные заявки на сервис успешно удалены!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_service_requests'))
