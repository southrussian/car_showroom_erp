from models import *
from flask import render_template, redirect, url_for, flash, request, session


def orders_routes(app):
    @app.route('/view_orders')
    def view_orders():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)

    @app.route('/add_order', methods=['GET', 'POST'])
    def add_order():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        if request.method == 'POST':
            car_id = request.form['car_id']
            client_id = request.form['client_id']
            expected_delivery_date = request.form['expected_delivery_date']
            status = request.form['status']

            order = Order(
                car_id=car_id,
                client_id=client_id,
                expected_delivery_date=datetime.strptime(expected_delivery_date,
                                                         '%Y-%m-%d').date() if expected_delivery_date else None,
                status=status
            )

            try:
                db.session.add(order)
                db.session.commit()
                flash("Order added successfully!", "success")
                return redirect(url_for('view_orders'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        cars = Car.query.all()
        clients = Client.query.all()
        return render_template('add_order.html', cars=cars, clients=clients)

    @app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
    def edit_order(order_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        order = Order.query.get_or_404(order_id)

        if request.method == 'POST':
            order.car_id = request.form['car_id']
            order.client_id = request.form['client_id']
            order.expected_delivery_date = datetime.strptime(request.form['expected_delivery_date'],
                                                             '%Y-%m-%d').date() if request.form[
                'expected_delivery_date'] else None
            order.status = request.form['status']

            try:
                db.session.commit()
                flash("Order updated successfully!", "success")
                return redirect(url_for('view_orders'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        cars = Car.query.all()
        clients = Client.query.all()
        return render_template('edit_order.html', order=order, cars=cars, clients=clients)

    @app.route('/delete_order/<int:order_id>', methods=['POST'])
    def delete_order(order_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        order = Order.query.get_or_404(order_id)
        try:
            db.session.delete(order)
            db.session.commit()
            flash("Order deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_orders'))
