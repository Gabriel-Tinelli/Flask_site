from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea




# Criando uma classe de formulário 
'''
Isso significa que estamos criando um modelo, e dentro deste modelo
existe objetos que compartilham as mesmas características e funcionalidades

Exemplo: Em um quartel (class), temos recrutas (objetos), sargentos (objetos) e comandantes (objetos), todos são soldados.
A função (def) do recruta é vigiar o quartel, logo todos os recrutas devem vigiar o quartel. Para que os sargentos não tenham que
mandar 1 a 1 vigiar o quartel.

Para novos soldados no quartel, devem ser recutados (instaciados = criação de objetos)


#Explicando os objetos:
name = StringField('Nome', validators=[DataRequired()])

-> Estamos criando um objeto chamdo 'name', 'name' cria um campo dentro da class 'UserForm', um campo que é uma caixa de texto
onde podemos inserir o nome. A palavra 'StringField' indica que este é um campo de texto. 
O texto entre parênteses ('Nome') é um rótulo que aparecerá ao lado do campo no formulário.
O validators=[DataRequired()] indica que este campo é obrigatório, ou seja, você deve preenchê-lo para enviar o formulário.
Dentro do parênteses de DataRequired, podemos escrever alguma mensagem, como por exemplo 'Você deve preencher o nome!'

Obviamente, tudo isso está no contexto do Flask-WTF

password_hash = PasswordField('Senha',validators=[DataRequired(), EqualTo('password_hash2', message='As senhas precisam ser iguais!')])

-> Este é um campo para inserir as senhas, PasswordField é uma classe que importamos da biblioteca do WTForms e que não torno possível
a visualização das senhas.

DataRequired(): Isso significa que a senha é obrigatória, você deve preenchê-la.
EqualTo('password_hash2', message='As senhas precisam ser iguais!'): Isso garante que a senha 
que você digitar neste campo seja igual à senha digitada no campo password_hash2. 
Se as senhas não forem iguais, a mensagem 'As senhas precisam ser iguais!' será exibida como erro.

'''

class UserForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Cor Favorita')
    password_hash = PasswordField('Senha',validators=[DataRequired(), EqualTo('password_hash2', message='As senhas precisam ser iguais!')])
    password_hash2 = PasswordField('Confirmar Senha',validators=[DataRequired()])
    submit = SubmitField('Enviar')


class NameForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Enviar')


#Criando Post Form
class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = StringField('Conteúdo', validators=[DataRequired()], widget=TextArea())
    author = StringField('Autor')
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Enviar')



#criando login form

class LoginForm(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    password = PasswordField('Senha',validators=[DataRequired()])
    submit = SubmitField('Entrar')


class PasswordForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password_hash = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Enviar')