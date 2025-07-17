from flask import Blueprint, request, jsonify
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

auth = Blueprint('auth', __name__)

# -----------------------------
# ✅ Register Route
# -----------------------------
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    profile_image_url = data.get('profile_image_url')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    if User.objects(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    hashed_pw = generate_password_hash(password)
    user = User(
        username=username,
        password=hashed_pw,
        profile_image_url=profile_image_url or ""
    )
    user.save()

    return jsonify({"msg": "User registered successfully"}), 201

# -----------------------------
# ✅ Login Route
# -----------------------------
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.objects(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token), 200

# -----------------------------
# ✅ Profile (GET / PUT)
# -----------------------------
@auth.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if request.method == 'GET':
        return jsonify({
            "username": user.username,
            "profile_image_url": user.profile_image_url or ""
        }), 200

    # ---------- PUT (update profile) ----------
    data = request.get_json()
    new_username = data.get('username')
    new_profile_image_url = data.get('profile_image_url')

    if new_username:
        # ตรวจสอบว่า username ใหม่ ไม่ซ้ำกับของคนอื่น
        existing_user = User.objects(username=new_username).first()
        if existing_user and str(existing_user.id) != str(user.id):
            return jsonify({"msg": "Username already taken"}), 400
        user.username = new_username

    if new_profile_image_url is not None:
        user.profile_image_url = new_profile_image_url

    user.save()
    return jsonify({
        "msg": "Profile updated successfully",
        "username": user.username,
        "profile_image_url": user.profile_image_url or ""
    }), 200
