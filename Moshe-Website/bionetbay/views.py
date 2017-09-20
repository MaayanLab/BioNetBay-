from flask import render_template, request, redirect
from bionetbay import app


@app.route('/')
@app.route('/index/', methods=['GET'])
def index():
        return render_template('index.html', title='Home')

@app.route('/resources/')
def resources():
    resources = ['GTEx', 'hu.MAP']
    return render_template('resources.html', title="Resources", resources=resources)

@app.route('/about/')
def about():
    return render_template('about.html', title="About")

@app.route('/search/', methods=['POST'])
def search():
    app.vars['gene'] = request.form['gene']
    return redirect('/genepage/'+app.vars['gene'])

@app.route('/genepage/<variable>' , methods=['GET'])
def genapage(variable):
    return render_template('genepage.html', title=variable, gene=variable)

@app.route('/resourcepage/<variable>')
def resourcepage(variable):
    return render_template('resourcepage.html', title=variable, resource=variable)
