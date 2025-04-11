from models import *
from flask import render_template, redirect, url_for, flash, request, session


def sales_routes(app):
    @app.route('/view_sales')
    def view_sales():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        sales = Sale.query.options(
            db.joinedload(Sale.order),
            db.joinedload(Sale.salesperson)
        ).all()
        return render_template('view_sales.html', sales=sales)

    @app.route('/add_sale', methods=['GET', 'POST'])
    def add_sale():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        if request.method == 'POST':
            order_id = request.form['order_id']
            sale_price = float(request.form['sale_price'])
            salesperson_id = request.form['salesperson_id']
            payment_method = request.form.get('payment_method')

            sale = Sale(
                order_id=order_id,
                sale_price=sale_price,
                salesperson_id=salesperson_id,
                payment_method=payment_method
            )

            try:
                db.session.add(sale)
                db.session.commit()
                flash("Sale added successfully!", "success")
                return redirect(url_for('view_sales'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        orders = Order.query.all()
        employees = Employee.query.all()
        return render_template('add_sale.html', orders=orders, employees=employees)

    @app.route('/edit_sale/<int:sale_id>', methods=['GET', 'POST'])
    def edit_sale(sale_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        sale = Sale.query.get_or_404(sale_id)

        if request.method == 'POST':
            sale.order_id = request.form['order_id']
            sale.sale_price = float(request.form['sale_price'])
            sale.salesperson_id = request.form['salesperson_id']
            sale.payment_method = request.form.get('payment_method')

            try:
                db.session.commit()
                flash("Sale updated successfully!", "success")
                return redirect(url_for('view_sales'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        orders = Order.query.all()
        employees = Employee.query.all()
        return render_template('edit_sale.html', sale=sale, orders=orders, employees=employees)

    @app.route('/delete_sale/<int:sale_id>', methods=['POST'])
    def delete_sale(sale_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        sale = Sale.query.get_or_404(sale_id)
        try:
            db.session.delete(sale)
            db.session.commit()
            flash("Данные продажи успешно удалены!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_sales'))

    # sales.py (добавления)
    @app.route('/create_sale_from_order/<int:order_id>', methods=['GET', 'POST'])
    def create_sale_from_order(order_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        order = Order.query.get_or_404(order_id)
        if order.status != 'Оплачен':
            flash('Можно создать продажу только для оплаченных заказов.', 'danger')
            return redirect(url_for('view_orders'))

        car = Car.query.get(order.car_id)
        if car.status == 'Продана':
            flash('Этот автомобиль уже продан.', 'danger')
            return redirect(url_for('view_orders'))

        if request.method == 'POST':
            sale_price = float(request.form['sale_price'])
            salesperson_id = request.form['salesperson_id']
            payment_method = request.form.get('payment_method')

            # Создаем продажу
            sale = Sale(
                order_id=order_id,
                sale_price=sale_price,
                salesperson_id=salesperson_id,
                payment_method=payment_method
            )

            try:
                # Обновляем статус заказа и автомобиля
                order.status = 'Завершен'
                car.status = 'Продана'
                db.session.add(sale)
                db.session.commit()
                flash("Продажа успешно оформлена!", "success")
                return redirect(url_for('view_sales'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        employees = Employee.query.all()
        return render_template('create_sale.html', order=order, car=car, employees=employees)
