from flask import Flask, render_template



#safe -> não expoem o html da frase (vai deixar em negrito)
#striptags -> retira o html da frase (não vai deixar negrito)
#title -> toda primeira letra da frase será maiscula
#trim -> removera os espaços antes e depois da frase
#upper -> tudo maisculo
#capitalize -> tudo minusculo



#Criando instância do flask
app = Flask(__name__) #__nome__ -> isto ajuda o flask a encontrar todos os nossos arquivos, sempre inicie um projeto flask assim

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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



