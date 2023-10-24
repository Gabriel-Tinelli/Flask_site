from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#Criando modelo de blog com post
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    slug = db.Column(db.String(255))


#criando modelo
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False) #é um campo que não pode ficar nulo 'nullable=False'
    email = db.Column(db.String(120), nullable=False, unique=True) #é um campo que não pode ficar nulo 'nullable=False' e não pode ter mais que 1 'unique=True'
    favorite_color = db.Column(db.String(20))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    # Do some password stuff!
    password_hash = db.Column(db.String(128))

    @property #decorador property e um metodo getter chamado password. É utilizado para não tornar legivel a propriedade 'password'
    #Isso significa que não podemos acessar a senha original diretamente através desta propriedade
    def password(self):
        raise AttributeError('password is not a readable attribute!')#Se alguém tentar acessar user.password, uma exceção AttributeError será gerada, protegendo assim a senha original.
    
    @password.setter#metodo setter para a propriedade password. Quando definimos user.password = "nova_senha", este método é chamado.
    def password(self, password):
        self.password_hash = generate_password_hash(password) #O objetivo deste método é calcular o hash da senha fornecida e armazená-lo no campo password_hash, utilizando o generate_password_hash

    def verify_password(self, password):# Este método verify_password é usado para verificar se a senha fornecida pelo usuário corresponde ao hash armazenado no banco de dados. 
        return check_password_hash(self.password_hash, password)


