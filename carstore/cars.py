from models import *
from flask import render_template, redirect, url_for, flash, request, session


def cars_routes(app):
    @app.route('/view_cars')
    def view_cars():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        cars = Car.query.all()
        return render_template('view_cars.html', cars=cars)

    @app.route('/add_car', methods=['GET', 'POST'])
    def add_car():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        cars = Car.query.all()
        if request.method == 'POST':
            make = request.form['make']
            model = request.form['model']
            year = request.form['year']
            vin = request.form['vin']
            color = request.form['color']
            price = request.form['price']
            mileage = request.form['mileage']
            status = request.form['status']
            fuel_type = request.form['fuel_type']
            transmission = request.form['transmission']
            body_type = request.form['body_type']

            car = Car(make=make, model=model, year=year, vin=vin, color=color, price=price,
                      mileage=mileage, status=status, fuel_type=fuel_type, transmission=transmission,
                      body_type=body_type)

            try:
                db.session.add(car)
                db.session.commit()
                flash("Patient added successfully!", "success")
                return redirect(url_for('view_patients'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_car.html', cars=cars)

    @app.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
    def edit_car(car_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        car = Car.query.get_or_404(car_id)

        if request.method == 'POST':
            car.make = request.form['make']
            car.model = request.form['model']
            car.year = request.form['year']
            car.vin = request.form['vin']
            car.color = request.form['color']
            car.price = request.form['price']
            car.mileage = request.form['mileage']
            car.status = request.form['status']
            car.fuel_type = request.form['fuel_type']
            car.transmission = request.form['transmission']
            car.body_type = request.form['body_type']

            try:
                db.session.commit()
                flash("Patient updated successfully!", "success")
                return redirect(url_for('view_patients'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_car.html', car=car)

    @app.route('/delete_car/<int:car_id>', methods=['POST'])
    def delete_car(car_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        car = Car.query.get_or_404(car_id)
        try:
            db.session.delete(car)
            db.session.commit()
            flash("Patient deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_cars'))
