from models import *
from flask import render_template, redirect, url_for, flash, request, session


def services_routes(app):
    @app.route('/view_services')
    def view_services():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        services = Service.query.options(
            db.joinedload(Service.request).joinedload(ServiceRequest.client),
            db.joinedload(Service.request).joinedload(ServiceRequest.service_type_rel)
        ).all()
        return render_template('view_services.html', services=services)

    @app.route('/add_service', methods=['GET', 'POST'])
    def add_service():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        if request.method == 'POST':
            request_id = request.form['request_id']
            status = request.form['status']
            description = request.form.get('description', '')

            service = Service(
                request_id=request_id,
                status=status,
                description=description,
                service_date=datetime.now()
            )

            try:
                db.session.add(service)
                db.session.commit()
                flash("Service added successfully!", "success")
                return redirect(url_for('view_services'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        service_requests = ServiceRequest.query.options(
            db.joinedload(ServiceRequest.client),
            db.joinedload(ServiceRequest.service_type_rel)
        ).all()

        return render_template('add_service.html',
                               service_requests=service_requests,
                               statuses=['Pending', 'In Progress', 'Completed', 'Cancelled'])

    @app.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
    def edit_service(service_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        service = Service.query.get_or_404(service_id)

        if request.method == 'POST':
            service.request_id = request.form['request_id']
            service.status = request.form['status']
            service.description = request.form.get('description', '')

            try:
                db.session.commit()
                flash("Service updated successfully!", "success")
                return redirect(url_for('view_services'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        service_requests = ServiceRequest.query.options(
            db.joinedload(ServiceRequest.client),
            db.joinedload(ServiceRequest.service_type_rel)
        ).all()

        return render_template('edit_service.html',
                               service=service,
                               service_requests=service_requests,
                               statuses=['Pending', 'In Progress', 'Completed', 'Cancelled'])

    @app.route('/delete_service/<int:service_id>', methods=['POST'])
    def delete_service(service_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        service = Service.query.get_or_404(service_id)
        try:
            db.session.delete(service)
            db.session.commit()
            flash("Service deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_services'))
