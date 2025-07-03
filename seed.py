from database import SessionLocal
from models import CableDesign

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
        db.commit()
    db.close()
