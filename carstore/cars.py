from models import *
from flask import render_template, redirect, url_for, flash, request, session
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime


current_year = datetime.now().year


def train_model():
    cars = Car.query.all()
    data = [(car.year, car.engine_volume, car.mileage, car.price) for car in cars]
    df = pd.DataFrame(data, columns=['year', 'engine_volume', 'mileage', 'price'])

    X = df[['year', 'engine_volume', 'mileage']]
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model


def cars_routes(app):
    with app.app_context():
        model = train_model()

    @app.route('/view_cars')
    def view_cars():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        cars = Car.query.all()
        return render_template('view_cars.html', cars=cars)

    @app.route('/add_car', methods=['GET', 'POST'])
    def add_car():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
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
            engine_volume = request.form['engine_volume']
            status = request.form['status']
            fuel_type = request.form['fuel_type']
            transmission = request.form['transmission']
            body_type = request.form['body_type']

            car = Car(make=make, model=model, year=year, vin=vin, color=color, price=price,
                      mileage=mileage, engine_volume=engine_volume, status=status, fuel_type=fuel_type,
                      transmission=transmission, body_type=body_type)

            try:
                db.session.add(car)
                db.session.commit()
                flash("Автомобиль успешно добавлен!", "success")
                return redirect(url_for('view_cars'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        return render_template('add_car.html', cars=cars)

    @app.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
    def edit_car(car_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
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
            car.engine_volume = request.form['engine_volume']
            car.status = request.form['status']
            car.fuel_type = request.form['fuel_type']
            car.transmission = request.form['transmission']
            car.body_type = request.form['body_type']

            try:
                db.session.commit()
                flash("Информация об автомобиле успешно обновлена!", "success")
                return redirect(url_for('view_cars'))
            except Exception as e:
                db.session.rollback()
                flash(f"Возникла ошибка: {e}", "danger")

        return render_template('edit_car.html', car=car)

    @app.route('/delete_car/<int:car_id>', methods=['POST'])
    def delete_car(car_id):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        car = Car.query.get_or_404(car_id)
        try:
            db.session.delete(car)
            db.session.commit()
            flash("Информация об автомобиле удалена!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Возникла ошибка: {e}", "danger")
        return redirect(url_for('view_cars'))

    @app.route('/predict_price', methods=['GET', 'POST'])
    def predict_price():
        if 'user_id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        prediction = None
        form_data = {}

        if request.method == 'POST':
            try:
                form_data = {
                    'year': int(request.form['year']),
                    'engine_volume': float(request.form['engine_volume']),
                    'mileage': int(request.form['mileage'])
                }

                input_data = np.array([[form_data['year'], form_data['engine_volume'], form_data['mileage']]])
                predicted_price = model.predict(input_data)[0]

                if form_data['mileage'] < 100000 and form_data['year'] > 2015:
                    predicted_price *= 1.1

                prediction = round(predicted_price, 2)

            except Exception as e:
                flash(f"Ошибка при расчете стоимости: {str(e)}", "danger")

        return render_template('predict_price.html',
                               prediction=prediction,
                               form_data=form_data)
