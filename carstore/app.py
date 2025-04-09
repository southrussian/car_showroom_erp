from flask import Flask, render_template, redirect, url_for, flash, session, request
import logging
from logging.handlers import RotatingFileHandler
from routes import register_routes
from flask_migrate import Migrate
from models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autosalon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'oxxxymiron'

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
file_handler = RotatingFileHandler('autosalon.log', maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
app.logger.addHandler(file_handler)

app.logger.info("Приложение запущено.")

db.init_app(app)
migrate = Migrate(app, db)

register_routes(app)


@app.route('/')
def dashboard():
    if 'user_id' not in session:
        app.logger.warning("Попытка доступа к панели управления без аутентификации.")
        flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
        return redirect(url_for('login'))
    app.logger.info(f"Доступ к панели управления пользователем ID: {session['user_id']}.")
    return render_template('dashboard.html')


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f"Страница не найдена: {e}")
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Внутренняя ошибка сервера: {e}")
    return render_template('500.html'), 500


@app.before_request
def before_request():
    app.logger.debug(f"Запрос: {request.method} {request.url}")


@app.after_request
def after_request(response):
    app.logger.debug(f"Ответ: {response.status}")
    return response


with app.app_context():
    db.create_all()
    app.logger.info("База данных инициализирована.")

if __name__ == '__main__':
    app.logger.info("Приложение запущено в режиме отладки.")
    app.run(debug=True, port=8000)
