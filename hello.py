from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


#safe -> não expoem o html da frase (vai deixar em negrito)
#striptags -> retira o html da frase (não vai deixar negrito)
#title -> toda primeira letra da frase será maiscula
#trim -> removera os espaços antes e depois da frase
#upper -> tudo maisculo
#capitalize -> tudo minusculo

#Criando instância do flask
app = Flask(__name__) #__nome__ -> isto ajuda o flask a encontrar todos os nossos arquivos, sempre inicie um projeto flask assim
app.config['SECRET_KEY'] = 'essa é uma chave super secreta contra todo o mal do mundo!' #essa chave é uma forma de proteção do seu formulário, garantindo que a sincronização nos bastidores, para não haver nenhum tipode invasão e desvio de formulário 

# criando uma classe de formulário 

class nome_src_forms(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Enviar')






#criando rota
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

#Pagina de nome
@app.route('/nome',methods=['GET', 'POST']) #metodo get e post para obeter ou postar o formulário que foi criado para pesquisa de nome
def name():
    name = None #o valor de nome precisa ser nulo porque no formulário está criando um nome, isso quer dizer que na primeira vez que a pagina for carregada, não haverá um nome
    form = nome_src_forms() #basicamente estamos dizendo: 'Ei! Use o formulario que criamos na linha 20'
    #Validação de formulário
    if form.validate_on_submit(): #basicamente estamos dizendo o seguinte: 'Se vc vai buscar o formulario com um nome, então atribua a variável name, caso contrário o nome não está certo' -> Se eles preencheram, me de um nome que foi preenchido e ent vamos limpar para a próxima vez
        name = form.name.data
        form.name.data = ''

    return render_template('name.html',name = name, form = form) #precisamos passar essas informações para a página! o Name é o name da linha 66 e o form é o da linha 67



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)





