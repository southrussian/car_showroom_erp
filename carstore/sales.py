from models import *
from flask import render_template, redirect, url_for, flash, request, session


def sales_routes(app):
    @app.route('/view_sales')
    def view_sales():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        sales = Sale.query.all()
        return render_template('view_sales.html', sales=sales)

    @app.route('/add_sale', methods=['GET', 'POST'])
    def add_sale():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            client_id = request.form['client_id']
            car_id = request.form['car_id']
            sale_date = request.form['sale_date']
            sale_price = request.form['sale_price']
            salesperson_id = request.form['salesperson_id']
            payment_method = request.form['payment_method']
            financing_details = request.form['financing_details']

            sale = Sale(client_id=client_id, car_id=car_id, sale_date=sale_date, sale_price=sale_price,
                        salesperson_id=salesperson_id, payment_method=payment_method,
                        financing_details=financing_details)

            try:
                db.session.add(sale)
                db.session.commit()
                flash("Sale added successfully!", "success")
                return redirect(url_for('view_sales'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_sale.html')

    @app.route('/edit_sale/<int:sale_id>', methods=['GET', 'POST'])
    def edit_sale(sale_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        sale = Sale.query.get_or_404(sale_id)

        if request.method == 'POST':
            sale.client_id = request.form['client_id']
            sale.car_id = request.form['car_id']
            sale.sale_date = request.form['sale_date']
            sale.sale_price = request.form['sale_price']
            sale.salesperson_id = request.form['salesperson_id']
            sale.payment_method = request.form['payment_method']
            sale.financing_details = request.form['financing_details']

            try:
                db.session.commit()
                flash("Sale updated successfully!", "success")
                return redirect(url_for('view_sales'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_sale.html', sale=sale)

    @app.route('/delete_sale/<int:sale_id>', methods=['POST'])
    def delete_sale(sale_id):
        if 'user_id' not in session:
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
