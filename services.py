from typing import Dict, List
from models import CableDesign, DesignRequest
from database import SessionLocal
from typing import Dict

db = SessionLocal()

DESIGN_FIELDS = ["cable_type", "size", "color", "cut_length"]
DESIGN_QUESTIONS = {
    "cable_type": "What cable type are you looking for? (e.g., XHHW-2)",
    "size": "Please choose a size from the available options.",
    "color": "Please choose a color from the available options.",
    "cut_length": "Please choose a cut length from the available options."
}

design_user_sessions: Dict[str, Dict] = {}

def get_options(field: str, filters: Dict) -> List[str]:
    query = db.query(CableDesign)
    for key, value in filters.items():
        query = query.filter(getattr(CableDesign, key) == value)
    values = query.with_entities(getattr(CableDesign, field)).distinct().all()
    return sorted(set([str(v[0]) for v in values]))

def handle_design_chat(user_id: str, message: str):
    message = message.strip()

    if user_id not in design_user_sessions:
        design_user_sessions[user_id] = {"step": 0, "data": {}}
        return {"reply": DESIGN_QUESTIONS["cable_type"]}

    session = design_user_sessions[user_id]
    step = session["step"]
    data = session["data"]

    if step > 0:
        data[DESIGN_FIELDS[step - 1]] = message

    if step < len(DESIGN_FIELDS):
        current_field = DESIGN_FIELDS[step]
        filters = {k: v for k, v in data.items()}
        options = get_options(current_field, filters)

        if not options:
            del design_user_sessions[user_id]
            return {"reply": f"No available {current_field} options found. Please restart."}

        session["step"] += 1
        return {"reply": f"{DESIGN_QUESTIONS[current_field]}\nOptions: {', '.join(options)}"}

    final_match = db.query(CableDesign).filter_by(
        cable_type=data["cable_type"],
        size=float(data["size"]),
        color=data["color"],
        cut_length=float(data["cut_length"])
    ).first()

    if not final_match:
        del design_user_sessions[user_id]
        return {"reply": "No design found with this configuration. Please restart."}

    new_request = DesignRequest(**data, design_code=final_match.design_code)
    db.add(new_request)
    db.commit()

    del design_user_sessions[user_id]
    return {"reply": f"Design saved. Your design code is: {final_match.design_code}"}







dummy_products = [
    {"product_code": "A2N2XY116", "cable_name": "A2N2XY", "num_cores": 3, "conductor_type": "Aluminum", "area": 4.0,"customer_code": "CUST001", "quantity": 10, "length": 100},
    {"product_code": "A2N2XY117", "cable_name": "A2N2XY", "num_cores": 4, "conductor_type": "Copper", "area": 6.0, "customer_code": "CUST002", "quantity": 5, "length": 50},
    {"product_code": "A2XFY220", "cable_name": "A2XFY", "num_cores": 2, "conductor_type": "Aluminum", "area": 2.5, "customer_code": "CUST003", "quantity": 20, "length": 200},
    {"product_code": "A2XFY221", "cable_name": "A2XFY", "num_cores": 3, "conductor_type": "Copper", "area": 10.0, "customer_code": "CUST004", "quantity": 15, "length": 150},
    {"product_code": "A2B2XY330", "cable_name": "A2B2XY", "num_cores": 5, "conductor_type": "Aluminum", "area": 16.0, "customer_code": "CUST005", "quantity": 8, "length": 80}
]

FIELDS = [
    "cable_name", "num_cores", "conductor_type", "area",
    "customer_code", "quantity", "length"
]

QUESTIONS = {
    "cable_name": "What is the cable name?",
    "num_cores": "How many cores does the cable have?",
    "conductor_type": "What is the conductor type? (e.g., Aluminum or Copper)",
    "area": "What is the cross-sectional area (in mm²)?",
    "customer_code": "Please provide the customer code.",
    "quantity": "How many units are needed?",
    "length": "What is the length (in meters)?"
}

user_sessions: Dict[str, Dict] = {}

def handle_enquiry_chat(user_id: str, message: str):
    message = message.strip()

    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": 0, "data": {}}
        return {"reply": QUESTIONS[FIELDS[0]]}

    session = user_sessions[user_id]
    step = session["step"]
    data = session["data"]

    if step > 0:
        data[FIELDS[step - 1]] = message

    if step == len(FIELDS):
        match = next((p for p in dummy_products if
                      p["cable_name"].lower() == data["cable_name"].lower() and
                      p["num_cores"] == int(data["num_cores"]) and
                      p["conductor_type"].lower() == data["conductor_type"].lower() and
                      p["area"] == float(data["area"])), None)

        if not match:
            reply = "No matching cable found. Please restart."
        else:
            data["product_code"] = match["product_code"]
            reply = f"Enquiry saved! Product Code: {match['product_code']}"

        del user_sessions[user_id]
        return {"reply": reply}

    session["step"] += 1
    return {"reply": QUESTIONS[FIELDS[step]]}
