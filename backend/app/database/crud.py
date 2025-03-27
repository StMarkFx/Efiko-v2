from .supabase import db

def get_user(user_id: str):
    user_ref = db.collection("users").document(user_id)
    user = user_ref.get()
    return user.to_dict() if user.exists else None

def create_user(user_id: str, user_data: dict):
    db.collection("users").document(user_id).set(user_data)
