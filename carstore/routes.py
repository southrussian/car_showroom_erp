from users import user_routes
from orders import orders_routes
from test_drives import test_drives_routes
from suppliers import suppliers_routes
from service_records import service_records_routes
from maintenance_schedules import maintenance_schedules_routes
from inventory import inventory_routes
from employees import employees_routes
from customer_feedbacks import customer_feedback_routes
from clients import clients_routes
from cars import cars_routes


def register_routes(app):
    user_routes(app)
    orders_routes(app)
    test_drives_routes(app)
    suppliers_routes(app)
    service_records_routes(app)
    maintenance_schedules_routes(app)
    inventory_routes(app)
    employees_routes(app)
    customer_feedback_routes(app)
    clients_routes(app)
    cars_routes(app)
