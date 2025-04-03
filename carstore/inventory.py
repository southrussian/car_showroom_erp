from models import *
from flask import render_template, redirect, url_for, flash, request, session


def inventory_routes(app):
    @app.route('/view_inventory')
    def view_inventory():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        inventory = Inventory.query.all()
        return render_template('view_inventory.html', inventory=inventory)

    @app.route('/add_inventory', methods=['GET', 'POST'])
    def add_inventory():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        if request.method == 'POST':
            car_id = request.form['car_id']
            quantity = request.form['quantity']
            location = request.form['location']
            arrival_date = request.form['arrival_date']
            supplier_id = request.form['supplier_id']

            inventory = Inventory(car_id=car_id, quantity=quantity, location=location, arrival_date=arrival_date,
                                  supplier_id=supplier_id)

            try:
                db.session.add(inventory)
                db.session.commit()
                flash("Inventory added successfully!", "success")
                return redirect(url_for('view_inventory'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_inventory.html')

    @app.route('/edit_inventory/<int:inventory_id>', methods=['GET', 'POST'])
    def edit_inventory(inventory_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        inventory = Inventory.query.get_or_404(inventory_id)

        if request.method == 'POST':
            inventory.car_id = request.form['car_id']
            inventory.quantity = request.form['quantity']
            inventory.location = request.form['location']
            inventory.arrival_date = request.form['arrival_date']
            inventory.supplier_id = request.form['supplier_id']

            try:
                db.session.commit()
                flash("Inventory updated successfully!", "success")
                return redirect(url_for('view_inventory'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_inventory.html', inventory=inventory)

    @app.route('/delete_inventory/<int:inventory_id>', methods=['POST'])
    def delete_inventory(inventory_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        inventory = Inventory.query.get_or_404(inventory_id)
        try:
            db.session.delete(inventory)
            db.session.commit()
            flash("Inventory deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_inventory'))
