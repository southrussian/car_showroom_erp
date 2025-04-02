from models import *
from flask import render_template, redirect, url_for, flash, request, session


def customer_feedback_routes(app):
    @app.route('/view_customer_feedback')
    def view_customer_feedback():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        customer_feedback = CustomerFeedback.query.all()
        return render_template('view_customer_feedback.html', customer_feedback=customer_feedback)

    @app.route('/add_customer_feedback', methods=['GET', 'POST'])
    def add_customer_feedback():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            client_id = request.form['client_id']
            car_id = request.form['car_id']
            feedback_date = request.form['feedback_date']
            rating = request.form['rating']
            comments = request.form['comments']

            customer_feedback = CustomerFeedback(client_id=client_id, car_id=car_id, feedback_date=feedback_date,
                                                 rating=rating, comments=comments)

            try:
                db.session.add(customer_feedback)
                db.session.commit()
                flash("Customer feedback added successfully!", "success")
                return redirect(url_for('view_customer_feedback'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('add_customer_feedback.html')

    @app.route('/edit_customer_feedback/<int:feedback_id>', methods=['GET', 'POST'])
    def edit_customer_feedback(feedback_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        customer_feedback = CustomerFeedback.query.get_or_404(feedback_id)

        if request.method == 'POST':
            customer_feedback.client_id = request.form['client_id']
            customer_feedback.car_id = request.form['car_id']
            customer_feedback.feedback_date = request.form['feedback_date']
            customer_feedback.rating = request.form['rating']
            customer_feedback.comments = request.form['comments']

            try:
                db.session.commit()
                flash("Customer feedback updated successfully!", "success")
                return redirect(url_for('view_customer_feedback'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {e}", "danger")

        return render_template('edit_customer_feedback.html', customer_feedback=customer_feedback)

    @app.route('/delete_customer_feedback/<int:feedback_id>', methods=['POST'])
    def delete_customer_feedback(feedback_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        customer_feedback = CustomerFeedback.query.get_or_404(feedback_id)
        try:
            db.session.delete(customer_feedback)
            db.session.commit()
            flash("Customer feedback deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('view_customer_feedback'))
