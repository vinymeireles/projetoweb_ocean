from flask import Flask, g, render_template, flash, request, redirect
import sqlite3

DATABASE = "blog.bd"
SECRET_KEY = "pudim"

app = Flask(__name__)
app.config.from_object(__name__)

#conectar a um banco de dados
def conectar_bd():
    return sqlite3.connect(DATABASE)

#abrir uma conexao
@app.before_request
def antes_requisicao():
    g.bd = conectar_bd()    

#terminar uma conexão
@app.teardown_request
def fim_requisicao(exc):
    g.bd.close()    

@app.route('/')
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC"
    cur = g.bd.execute(sql)
    entradas = []
    for titulo, texto in cur.fetchall(): #armazena o resultado do banco num dicionario {} do python
        entradas.append({
            "titulo" : titulo,
            "texto": texto
            })
    return render_template("exibir_entradas.html", posts=entradas)        #carregar o arquivo html que deve abrir 

@app.route('/inserir', methods=['POST'])
def inserir_entrada():
    sql = "INSERT INTO entradas(titulo, texto) VALUES (?, ?);"
    titulo = request.form['titulo']
    texto = request.form['texto']
    g.bd.execute(sql, [titulo, texto])
    g.bd.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)