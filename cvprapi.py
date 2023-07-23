import json
import random
import smtplib
import string
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
import firebase_admin
from firebase_admin import credentials,firestore
from flask import Flask, jsonify, request
import bcrypt
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager
credentialData = credentials.Certificate("credentialscvpr.json")
firebase_admin.initialize_app(credentialData)
firestoreDb = firestore.client()


app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cvdestekinf@gmail.com'
app.config['MAIL_PASSWORD'] = 'jfuoqhrmerydazlp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.config['JWT_SECRET_KEY'] = 'my-secretkeyburak-1234'  # Bunu değiştirin!
jwt = JWTManager(app)
users = {
    "cvprmt": "200419000",
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# --------------------------------- test api ---------------------------------


@app.route('/', methods=['POST'])
@auth.login_required
def testapi():
    if auth.current_user() == 'cvprmt':
        pass
    else:
        return jsonify({"message": "Access denied"}), 403
    




# --------------------------------- auth ---------------------------------
# --------------------------------- auth ---------------------------------
# --------------------------------- auth ---------------------------------



@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    if auth.current_user() == 'cvprmt':
        mail = request.headers.get("mail")

        docs4 = firestoreDb.collection(f'Accounts').where('mail', '==', mail).get()
        if docs4:
            first_doc = docs4[0]
            username = first_doc.to_dict().get('username')
        else:
            return jsonify({"message":"wrong mail"}),403
        password = request.headers.get('password')
        type = request.headers.get('type')
        if type == "r":
            token=create_refresh_token(username=username)
            return (token)
        doc = firestoreDb.collection('Accounts').document(f'{username}').get()
        
        sdoc=doc.to_dict()

        hashpassword=sdoc["password"]

        if check_password(password=password,hashed_password=hashpassword) ==True:
                id=sdoc["id"]
                username=sdoc["id"]
                token=create_token(username=username)
                return jsonify({"message": "login succesful","user":sdoc,"token":token}), 200
        else:
            return jsonify({"message":"wrong password"}),403


    else:
        return jsonify({"message": "Access denied"}), 403

@app.route('/check_mail', methods=['POST'])
@auth.login_required
def check_mail():
    username = request.headers.get('username')
    number=request.headers.get('number')
    with open("numbers.json","r",encoding="utf-8") as f:
       exit_data= json.load(f)
    
    for i in exit_data:
        if i["username"] == username:
            if i["number"]==int(number):
                doc_ref = firestoreDb.collection(f'Accounts').document(f'{username}')
                doc_ref.update({'statusid': 1})
                doc_ref.update({'statusname': "onaylı"})

                return({"message":"Doğrulama Başarılı","messageid":0})

            else:
                return jsonify({"message":"Doğrulama Kodu yanlış !","messageid":2})
        else:
            return jsonify({"message":"Tekrar Doğrulama Kodu Gönderiniz !","messageid":1})
        
@app.route('/register', methods=['POST'])
@auth.login_required
def register():
    mail = request.headers.get('mail')
    username = request.headers.get('username')
    name = request.headers.get('name')
    lastname = request.headers.get('lastname')
    phone = request.headers.get('phone')
    unhashedpassword = request.headers.get('password')
    password = hash_password(unhashedpassword)
    if auth.current_user() == 'cvprmt':
        number=generate_random_number_and_save(username=username)
        sendingmail=send_mail(to=mail,subject="Mail Onay",body=f"Merhaba tek kullanimlik eposta onay kodu: {number}")
        user_ref = firestoreDb.collection(f'Accounts').where('phone', '==', phone).get()
        if len(user_ref) > 0:
            return jsonify({"message": "Bu numara zaten kullanılmakta.","messageid":1}), 400
        user_ref1 = firestoreDb.collection(f'Accounts').where('mail', '==', mail).get()
        if len(user_ref1) > 0:
            return jsonify({"message": "Bu mail zaten kullanılmakta.","messageid":2}), 400

        user_ref = firestoreDb.collection(f'Accounts').document(username)
        user = user_ref.get()
        if user.exists:
            return jsonify({"message": "Kullanıcı Adı Alınmış.","messageid":3}), 400
        else:
            id = generate_token()
            response = user_ref.set({"statusid":0,"statusname":"onaysız","mail": mail, "username": username, 'id': id, "password": password,"phone":phone,"name":name,
                                     "lastname":lastname})
            return jsonify({"message": f"Kayıt Başarılı","messageid":0})
    else:
        return jsonify({"message": "Access denied"}), 403

# --------------------------------- core func ---------------------------------
# --------------------------------- core func ---------------------------------
# --------------------------------- core func ---------------------------------


def hash_password(password: str) -> str:
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)

def generate_token(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def send_mail(to=str, subject=str, body=str):
    msg = Message(subject, sender='cvdestekinf@gmail.com', recipients=[to])
    msg.body = body
    mail.send(msg)
SECRET_KEY = 'my_very_secure_secret_key'

# Create a refresh token
def create_refresh_token(username):
    # Set the expiration time
    exp = datetime.utcnow() + timedelta(days=30)
    
    # Create the payload
    payload = {'username': username, 'exp': exp, 'type': 'refresh'}
    
    # Encode the token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token

# Create a JWT token
def create_token(username):
    # Set the expiration time
    exp = datetime.utcnow() + timedelta(hours=1)
    
    # Create the payload
    payload = {'username': username, 'exp': exp}
    
    # Encode the token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token
import jwt

# JWT secret key

# Verify a JWT token
def verify_token(token):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Get the username from the payload
        username = payload.get('username')
        
        return username
    
    except jwt.ExpiredSignatureError:
        # Token has expired
        return ("Token Süresi Dolmuş")
    
    except jwt.InvalidTokenError:
        # Token is invalid
        return ("Token Yanlış")

def generate_random_number_and_save(username: str):
    number = random.randint(100000, 999999)
    now = datetime.now()
    timestamp = now.timestamp()

    try:
        with open('numbers.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append({'username': username, 'number': number, 'timestamp': timestamp})

    one_hour_ago = (now - timedelta(hours=1)).timestamp()
    data = [item for item in data if item['timestamp'] > one_hour_ago]

    with open('numbers.json', 'w') as f:
        json.dump(data, f)

    return number


if __name__ == '__main__':
    app.run()
