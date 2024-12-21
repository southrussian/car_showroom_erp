from models import *
from flask import render_template, redirect, url_for, flash, request, session


def view_clients(app):
    @app.route('/view_clients')
    def view_clients():
        clients = Client.query.all()
        return render_template('view_clients.html', clients=clients)

def add_client(app):
    @app.route('/add_client', methods=['GET', 'POST'])
    def add_client():
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone_number = request.form['phone_number']
            email = request.form['email']
            address = request.form['address']
            date_of_birth = request.form['date_of_birth']
            gender = request.form['gender']
            preferred_contact_method = request.form['preferred_contact_method']

            client = Client(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email,
                            address=address, date_of_birth=date_of_birth, gender=gender,
                            preferred_contact_method=preferred_contact_method)

            try:
                db.session.add(client)
                db.session.commit()
                flash("Client added successfully!", "success")
                return redirect(url_for('view_clients'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_client.html')

def edit_client(app):
    @app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
    def edit_client(client_id):
        client = Client.query.get_or_404(client_id)

        if request.method == 'POST':
            client.first_name = request.form['first_name']
            client.last_name = request.form['last_name']
            client.phone_number = request.form['phone_number']
            client.email = request.form['email']
            client.address = request.form['address']
            client.date_of_birth = request.form['date_of_birth']
            client.gender = request.form['gender']
            client.preferred_contact_method = request.form['preferred_contact_method']

            try:
                db.session.commit()
                flash("Client updated successfully!", "success")
                return redirect(url_for('view_clients'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_client.html', client=client)

def delete_client(app):
    @app.route('/delete_client/<int:client_id>', methods=['POST'])
    def delete_client(client_id):
        client = Client.query.get_or_404(client_id)
        try:
            db.session.delete(client)
            db.session.commit()
            flash("Client deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_clients'))
