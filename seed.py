from database import SessionLocal
from models import CableDesign, Product

def seed_data():
    db = SessionLocal()

    if db.query(CableDesign).count() == 0:
        designs = [
            {"cable_type": "XHHW-2", "size": 2.5, "color": "red", "cut_length": 500, "design_code": "C0001_500"},
            {"cable_type": "XHHW-2", "size": 4.0, "color": "black", "cut_length": 1000, "design_code": "C0001_1000"},
            {"cable_type": "XHHW-2", "size": 6.0, "color": "blue", "cut_length": 500, "design_code": "C0002_500"},
        ]
        for d in designs:
            db.add(CableDesign(**d))

    if db.query(Product).count() == 0:
        products = [
            {"product_code": "A2N2XY116", "cable_name": "A2N2XY", "num_cores": 3, "conductor_type": "Aluminum", "area": 4.0, "customer_code": "CUST001", "quantity": 10, "length": 100},
            {"product_code": "A2N2XY117", "cable_name": "A2N2XY", "num_cores": 4, "conductor_type": "Copper", "area": 6.0, "customer_code": "CUST002", "quantity": 5, "length": 50},
            {"product_code": "A2XFY220", "cable_name": "A2XFY", "num_cores": 2, "conductor_type": "Aluminum", "area": 2.5, "customer_code": "CUST003", "quantity": 20, "length": 200},
            {"product_code": "A2XFY221", "cable_name": "A2XFY", "num_cores": 3, "conductor_type": "Copper", "area": 10.0, "customer_code": "CUST004", "quantity": 15, "length": 150},
            {"product_code": "A2B2XY330", "cable_name": "A2B2XY", "num_cores": 5, "conductor_type": "Aluminum", "area": 16.0, "customer_code": "CUST005", "quantity": 8, "length": 80}
        ]
        for p in products:
            db.add(Product(**p))

    db.commit()
    db.close()
