from models import *
from flask import render_template, redirect, url_for, flash, request, session


def view_suppliers(app):
    @app.route('/view_suppliers')
    def view_suppliers():
        suppliers = Supplier.query.all()
        return render_template('view_suppliers.html', suppliers=suppliers)

def add_supplier(app):
    @app.route('/add_supplier', methods=['GET', 'POST'])
    def add_supplier():
        if request.method == 'POST':
            name = request.form['name']
            contact_person = request.form['contact_person']
            phone_number = request.form['phone_number']
            email = request.form['email']
            address = request.form['address']

            supplier = Supplier(name=name, contact_person=contact_person, phone_number=phone_number, email=email,
                               address=address)

            try:
                db.session.add(supplier)
                db.session.commit()
                flash("Supplier added successfully!", "success")
                return redirect(url_for('view_suppliers'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_supplier.html')

def edit_supplier(app):
    @app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
    def edit_supplier(supplier_id):
        supplier = Supplier.query.get_or_404(supplier_id)

        if request.method == 'POST':
            supplier.name = request.form['name']
            supplier.contact_person = request.form['contact_person']
            supplier.phone_number = request.form['phone_number']
            supplier.email = request.form['email']
            supplier.address = request.form['address']

            try:
                db.session.commit()
                flash("Supplier updated successfully!", "success")
                return redirect(url_for('view_suppliers'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_supplier.html', supplier=supplier)

def delete_supplier(app):
    @app.route('/delete_supplier/<int:supplier_id>', methods=['POST'])
    def delete_supplier(supplier_id):
        supplier = Supplier.query.get_or_404(supplier_id)
        try:
            db.session.delete(supplier)
            db.session.commit()
            flash("Supplier deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_suppliers'))