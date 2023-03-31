from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/busca', methods=['POST'])
def busca():
    nome_produto = request.form['nome_produto']
    palavras = nome_produto.split()[:3]
    nome_produto = ' '.join(palavras)

    df = pd.read_excel('C:\\Users\\Administrador\\Desktop\\Pasta1.xlsx')
    df['Nome do Produto'] = df['Nome do Produto'].fillna('')
    produtos_similares = df.loc[df['Nome do Produto'].str.contains(nome_produto)]

    if produtos_similares is None or produtos_similares.empty:
        mensagem = 'Produtos similares não encontrados.'
        tabela = False
    else:
        tabela = True
        mensagem = '<table><tr><th>Código do Produto</th><th>Nome do Produto</th><th>Quantidade</th><th>Ações</th></tr>'
        for i, row in produtos_similares.iterrows():
            mensagem += f'<tr><td>{row["Código do Produto"]}</td><td>{row["Nome do Produto"]}</td><td>{row["Quantidade"]}</td><td><a href="/editar/{row["Código do Produto"]}" class="btn btn-primary">Editar</a></td></tr>'
        mensagem += '</table>'

    return render_template('resultado.html', tabela=tabela, mensagem=mensagem, produtos=produtos_similares)

@app.route('/adicionar')
def adicionar():
    return render_template('adicionar.html')

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    df = pd.read_excel('C:\\Users\\Administrador\\Desktop\\Pasta1.xlsx')

    codigo = request.form['codigo']
    nome = request.form['nome']
    quantidade = request.form['quantidade']

    novo_produto = pd.DataFrame({'Código do Produto': [codigo], 'Nome do Produto': [nome], 'Quantidade': [quantidade]})
    df = pd.concat([df, novo_produto])

    df.to_excel('C:\\Users\\Administrador\\Desktop\\Pasta1.xlsx', index=False)

    return redirect('/')

@app.route('/editar/<codigo>', methods=['GET', 'POST'])
def editar(codigo):
    df = pd.read_excel('C:\\Users\\Administrador\\Desktop\\Pasta1.xlsx')
    produto = df.loc[df['Código do Produto'] == codigo].iloc[0]

    if request.method == 'POST':
        produto['Nome do Produto'] = request.form['nome']
        produto['Quantidade'] = request.form['quantidade']
        df.loc[df['Código do Produto'] == codigo] = produto
        df.to_excel('C:\\Users\\Administrador\\Desktop\\Pasta1.xlsx', index=False)
        return redirect('/')
    else:
        return render_template('editar.html', produto=produto)

if __name__ == '__main__':
    app.run()
