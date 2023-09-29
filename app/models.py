from app import db
from app import app
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime
from time import time
import jwt


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = "users" 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Integer, default=0) # 0 not admin, 1 admin
    enabled = db.Column(db.Integer, default=1) # 0 not enabled, 1 enabled
    point= db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)




# Ders tablosu (Daha önce tanımladık)
class Ders(db.Model):
    __tablename__ = 'dersler'

    id = db.Column(db.Integer, primary_key=True)
    ders_adi = db.Column(db.String(100), nullable=False)
    ders_kodu = db.Column(db.String(20), unique=True, nullable=False)
    ders_aciklamasi = db.Column(db.Text)

    def __init__(self, ders_adi, ders_kodu, ders_aciklamasi):
        self.ders_adi = ders_adi
        self.ders_kodu = ders_kodu
        self.ders_aciklamasi = ders_aciklamasi

# Sınav tablosu (Daha önce tanımladık)
class Sinav(db.Model):
    __tablename__ = 'sinavlar'

    id = db.Column(db.Integer, primary_key=True)
    ders_id = db.Column(db.Integer, db.ForeignKey('dersler.id'), nullable=False)
    sinav_tarihi = db.Column(db.Date, nullable=False)
    soru_sayisi = db.Column(db.Integer, nullable=False)
    zorluk_seviyesi = db.Column(db.String(20), nullable=False)

    ders = db.relationship('Ders', backref='sinavlar')

    def __init__(self, ders_id, sinav_tarihi, soru_sayisi, zorluk_seviyesi):
        self.ders_id = ders_id
        self.sinav_tarihi = sinav_tarihi
        self.soru_sayisi = soru_sayisi
        self.zorluk_seviyesi = zorluk_seviyesi

# Soru tablosu
class Soru(db.Model):
    __tablename__ = 'sorular'

    id = db.Column(db.Integer, primary_key=True)
    sinav_id = db.Column(db.Integer, db.ForeignKey('sinavlar.id'), nullable=False)
    soru_metni = db.Column(db.Text, nullable=False)

    sinav = db.relationship('Sinav', backref='sorular')

    def __init__(self, sinav_id, soru_metni):
        self.sinav_id = sinav_id
        self.soru_metni = soru_metni

# Şık tablosu
class Sik(db.Model):
    __tablename__ = 'siklar'

    id = db.Column(db.Integer, primary_key=True)
    soru_id = db.Column(db.Integer, db.ForeignKey('sorular.id'), nullable=False)
    sik_metni = db.Column(db.Text, nullable=False)
    dogru_mu = db.Column(db.Boolean, default=False)

    soru = db.relationship('Soru', backref='siklar')

    def __init__(self, soru_id, sik_metni, dogru_mu=False):
        self.soru_id = soru_id
        self.sik_metni = sik_metni
        self.dogru_mu = dogru_mu
        