from models import *
from flask import render_template, redirect, url_for, flash, request, session


def clients_routes(app):
    @app.route('/view_clients')
    def view_clients():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        clients = Client.query.all()
        return render_template('view_clients.html', clients=clients)

    @app.route('/add_client', methods=['GET', 'POST'])
    def add_client():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        if request.method == 'POST':
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            phone_number = request.form['phone_number']
            email = request.form['email']

            client = Client(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email
            )

            try:
                db.session.add(client)
                db.session.commit()
                flash("Клиент успешно добавлен!", "success")
                return redirect(url_for('view_clients'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        return render_template('add_client.html')

    @app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
    def edit_client(client_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        client = Client.query.get_or_404(client_id)

        if request.method == 'POST':
            client.first_name = request.form['first_name']
            client.middle_name = request.form['middle_name']
            client.last_name = request.form['last_name']
            client.phone_number = request.form['phone_number']
            client.email = request.form['email']

            try:
                db.session.commit()
                flash("Данные клиента успешно обновлены!", "success")
                return redirect(url_for('view_clients'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        return render_template('edit_client.html', client=client)

    @app.route('/delete_client/<int:client_id>', methods=['POST'])
    def delete_client(client_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        client = Client.query.get_or_404(client_id)
        try:
            db.session.delete(client)
            db.session.commit()
            flash("Данные клиенты успешно удалены!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_clients'))
