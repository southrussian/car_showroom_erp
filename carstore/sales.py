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
                flash(f"An error occurred: {e}", "danger")

        orders = Order.query.all()
        employees = Employee.query.filter_by(position='salesperson').all()
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
                flash(f"An error occurred: {e}", "danger")

        orders = Order.query.all()
        employees = Employee.query.filter_by(position='salesperson').all()
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
            flash("Sale deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_sales'))
