from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from werkzeug.security import generate_password_hash, check_password_hash






#safe -> não expoem o html da frase (vai deixar em negrito)
#striptags -> retira o html da frase (não vai deixar negrito)
#title -> toda primeira letra da frase será maiscula
#trim -> removera os espaços antes e depois da frase
#upper -> tudo maisculo
#capitalize -> tudo minusculo

#Criando instância do flask
app = Flask(__name__) #__nome__ -> isto ajuda o flask a encontrar todos os nossos arquivos, sempre inicie um projeto flask assim
#adicionando database
#Antigo SQL db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
#NOVO SQL DB! (MySQL DB)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/users'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#Secret KEY
app.config['SECRET_KEY'] = 'essa é uma chave super secreta contra todo o mal do mundo!' #essa chave é uma forma de proteção do seu formulário, garantindo que a sincronização nos bastidores, para não haver nenhum tipode invasão e desvio de formulário 
#Inicializando  database

#Criando modelo de blog com post
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    slug = db.Column(db.String(255))


#criando modelo
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) #é um campo que não pode ficar nulo 'nullable=False'
    email = db.Column(db.String(120), nullable=False, unique=True) #é um campo que não pode ficar nulo 'nullable=False' e não pode ter mais que 1 'unique=True'
    favorite_color = db.Column(db.String(20))
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    # Do some password stuff!
    password_hash = db.Column(db.String(128)) #um hash  é uma representação irreversível da senha original, não é seguro armazenar senhas em texto simples

    @property #decorador property e um metodo getter chamado password. É utilizado para não tornar legivel a propriedade 'password'
    #Isso significa que não podemos acessar a senha original diretamente através desta propriedade
    def password(self):
        raise AttributeError('password is not a readable attribute!')#Se alguém tentar acessar user.password, uma exceção AttributeError será gerada, protegendo assim a senha original.
    
    @password.setter#metodo setter para a propriedade password. Quando definimos user.password = "nova_senha", este método é chamado.
    def password(self, password):
        self.password_hash = generate_password_hash(password) #O objetivo deste método é calcular o hash da senha fornecida e armazená-lo no campo password_hash, utilizando o generate_password_hash

    def verify_password(self, password):# Este método verify_password é usado para verificar se a senha fornecida pelo usuário corresponde ao hash armazenado no banco de dados. 
        return check_password_hash(self.password_hash, password)

#setter:setter é um método em Python que permite definir o valor de um atributo de um objeto.
#Ele é usado para controlar como os valores dos atributos são atribuídos e normalmente é usado em conjunto com o decorador @property

#A palavra-chave raise é usada em Python para levantar exceções.
#a linha raise AttributeError('password is not a readable attribute!') está levantando uma exceção do tipo AttributeError com a mensagem "password is not a readable attribute!" quando alguém tenta acessar a propriedade password. Isso é feito para proteger a senha original e impedir que alguém acesse diretamente.

#user.verify_password("senha"), o self é automaticamente preenchido com a instância do objeto user.
#password é usado como um nome de propriedade, um nome de método e um nome de atributo. É uma escolha de nome para representar a senha dos usuários.

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = StringField('Conteúdo', validators=[DataRequired()], widget=TextArea())
    author = StringField('Autor', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Enviar')


@app.route('/posts')
def posts():
    #publicação de posts

    posts = Posts.query.order_by(Posts.date_posted)

    return render_template('posts.html', posts=posts)

    

@app.route('/posts/delete/<int:id>')
def delete_post(id):
        post_to_delete = Posts.query.get_or_404(id)
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Post deletado com sucesso!')

            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)
            
                
        except:
            flash('Ops, tivemos um problema, tente novamente!')
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)




@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        #criando formulário
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        #adicionando post no db

        db.session.add(post)
        db.session.commit()

        flash('Postagem enviada com sucesso!')

        #redirecionando para a pagina
        

    return render_template('add_post.html', form=form)
    

#criando string

def __repr__(self):
        return '<Name %r>' % self.name

app.app_context().push()
db.create_all()


# criando uma classe de formulário 

class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class PasswordForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password_hash = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class UserForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Cor Favorita')
    password_hash = PasswordField('Senha',validators=[DataRequired(), EqualTo('password_hash2', message='As senhas precisam ser iguais!')])
    password_hash2 = PasswordField('Confirmar Senha',validators=[DataRequired()])
    submit = SubmitField('Enviar')


#Criando função delete
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Usuário deletado com sucesso!')

        users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', form=form, name=name, users=users)


    except:
        flash('Ops, tivemos um problema, tente novamente!')
        return render_template('add_user.html', form=form, name=name, users=users)


#Update Database
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def uptade(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash('Usuário atualizado com sucesso!')
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            db.session.commit()
            flash('Houve um problema, tente novamente!')
            return render_template('update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update,id=id)


#criando rota

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        #update no db
        db.session.add(post)
        db.session.commit()
        flash('Post atualizado com sucesso!')
        return redirect(url_for('post', id=post.id,))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html',form=form)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #hash password
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''
        flash('Usuário adicionado com sucesso!')
    users = Users.query.order_by(Users.date_added)


    return render_template('add_user.html', form=form, name=name, users=users)




@app.route('/')

#def index():
#    return "<h1>Hello World!</h1>"

def index():
    primeiro_nome = 'Gabriel'
    usando_safe = 'Isso é um exemplo da função safe' #ele não vai expor o html na minha frase e vai deixar em negrito
    pizza_favorita = ['Pepperoni', 'Queijo', 'Carne', 41]
    return render_template('index.html', primeiro_nome=primeiro_nome, usando_safe=usando_safe, pizza_favorita=pizza_favorita)
    
#localhost:5000/user/gabriel
@app.route('/user/<name>')

#def user(name):
#    return "<h1>Hello {}!</h1>".format(name) #funciona do mesmo jeito da de baixo, porém a de baixo é melhor

def user(name):
    return render_template('user.html', user_name=name)

#criando paginas de erro customizadas
#URL inválida

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Erro interno do servidor


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

#teste de senha

@app.route('/test_pw',methods=['GET', 'POST']) #metodo get e post para obeter ou postar o formulário que foi criado para pesquisa de nome
def test_pw():
    email = None 
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    if form.validate_on_submit(): 
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''


        #Encontrar usúrio por e-mail
        pw_to_check = Users.query.filter_by(email=email).first()

        # Checar hash da senha
        passed = check_password_hash(pw_to_check.password_hash, password)


        flash('Formulário enviado com sucesso!')

    return render_template('test_pw.html',email = email, password = password, form = form, pw_to_check=pw_to_check, passed = passed) 

#Pagina de nome
@app.route('/nome',methods=['GET', 'POST']) #metodo get e post para obeter ou postar o formulário que foi criado para pesquisa de nome
def name():
    name = None #o valor de nome precisa ser nulo porque no formulário está criando um nome, isso quer dizer que na primeira vez que a pagina for carregada, não haverá um nome
    form = NameForm() #basicamente estamos dizendo: 'Ei! Use o formulario que criamos na linha 20'
    #Validação de formulário
    if form.validate_on_submit(): #basicamente estamos dizendo o seguinte: 'Se vc vai buscar o formulario com um nome, então atribua a variável name, caso contrário o nome não está certo' -> Se eles preencheram, me de um nome que foi preenchido e ent vamos limpar para a próxima vez
        name = form.name.data
        form.name.data = ''
        flash('Formulário enviado com sucesso!')

    return render_template('name.html',name = name, form = form) #precisamos passar essas informações para a página! o Name é o name da linha 66 e o form é o da linha 67



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)






