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
                flash("Заказ успешно создан!", "success")
                return redirect(url_for('view_orders'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

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
                flash("Заказ успешно обновлен!", "success")
                return redirect(url_for('view_orders'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

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
            flash("Данные заказа успешно удалены!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_orders'))

    @app.route('/reserve_car/<int:car_id>', methods=['GET', 'POST'])
    def reserve_car(car_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        car = Car.query.get_or_404(car_id)
        if car.status == 'Продана':
            flash('Этот автомобиль уже продан и не может быть забронирован.', 'danger')
            return redirect(url_for('view_cars'))

        if request.method == 'POST':
            client_id = request.form['client_id']
            expected_delivery_date = request.form['expected_delivery_date']

            # Создаем заказ со статусом "Забронирована"
            order = Order(
                car_id=car_id,
                client_id=client_id,
                expected_delivery_date=datetime.strptime(expected_delivery_date,
                                                         '%Y-%m-%d').date() if expected_delivery_date else None,
                status='Забронирована'
            )

            try:
                # Обновляем статус автомобиля
                car.status = 'Забронирована'
                db.session.add(order)
                db.session.commit()
                flash("Автомобиль успешно забронирован!", "success")
                return redirect(url_for('view_orders'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        clients = Client.query.all()
        return render_template('reserve_car.html', car=car, clients=clients)

    @app.route('/complete_order/<int:order_id>', methods=['POST'])
    def complete_order(order_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        order = Order.query.get_or_404(order_id)
        if order.status != 'Забронирована':
            flash('Можно завершать только забронированные заказы.', 'danger')
            return redirect(url_for('view_orders'))

        try:
            # Обновляем статус заказа
            order.status = 'Оплачен'
            db.session.commit()
            flash("Заказ успешно оплачен!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")

        return redirect(url_for('view_orders'))
