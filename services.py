from typing import Dict, List
from models import CableDesign, DesignRequest
from database import SessionLocal
from typing import Dict
from models import Product, ProductEnquiry  

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
        field = FIELDS[step - 1]
        if field in ["num_cores", "quantity"]:
            data[field] = int(message)
        elif field in ["area", "length"]:
            data[field] = float(message)
        else:
            data[field] = message

    if step == len(FIELDS):
        match = db.query(Product).filter_by(
            cable_name=data["cable_name"],
            num_cores=data["num_cores"],
            conductor_type=data["conductor_type"],
            area=data["area"]
        ).first()

        if not match:
            reply = "No matching cable found. Please restart."
        else:
            data["product_code"] = match.product_code

            new_enquiry = ProductEnquiry(**data)
            db.add(new_enquiry)
            db.commit()

            reply = f"Enquiry saved! Product Code: {match.product_code}"

        del user_sessions[user_id]
        return {"reply": reply}

    session["step"] += 1
    return {"reply": QUESTIONS[FIELDS[step]]}
