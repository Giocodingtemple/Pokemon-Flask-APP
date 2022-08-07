from app import db, login
from flask_login import UserMixin # THIS IS ONLY FOR THE USER MODEL!!!!!!!!!!!!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)   

    # should return a unique identifing string
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'
    
    # Human readable repr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    # salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    #save user to db
    def save(self):
        db.session.add(self) # add the userr to the session
        db.session.commit() # sace the stuff in the session to the database
    
    def from_dict(self, data):
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=self.hash_password(data['password'])
        self.icon=data['icon']

    def get_icon_url(self):
        return f"http://avatars.dicebear.com/api/croodles/{self.icon}.svg"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # SELECT * FROM user WHERE id = ???

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ability = db.Column(db.String)
    exp = db.Column(db.String)
    attk = db.Column(db.String)
    hp = db.Column(db.String)
    defense = db.Column(db.String)
    sprite = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_caught = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f"<Pokemon: {self.id} | {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def release(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, poke_dict):
        self.name = poke_dict['Name']
        self.ability = poke_dict['Ability']
        self.exp = poke_dict['BaseExp']
        self.attk = poke_dict['BaseAttk']
        self.hp = poke_dict['BaseHP']
        self.defense = poke_dict['BaseDef']
        self.sprite = poke_dict['Sprite']
        self.user_id = poke_dict['User_id']

