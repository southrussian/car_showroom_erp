from cars import cars_routes
from clients import clients_routes
from consultations import consultations_routes
from employees import employees_routes
from orders import orders_routes
from sales import sales_routes
from service_requests import service_requests_routes
from service_types import service_types_routes
from services import services_routes
from test_drives import test_drives_routes
from users import user_routes


def register_routes(app):
    cars_routes(app)
    clients_routes(app)
    consultations_routes(app)
    employees_routes(app)
    orders_routes(app)
    sales_routes(app)
    service_requests_routes(app)
    service_types_routes(app)
    services_routes(app)
    test_drives_routes(app)
    user_routes(app)
