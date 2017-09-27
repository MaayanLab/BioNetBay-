from flask import render_template, request, redirect, send_from_directory
import os
import time
from bionetbay import app, db, models


@app.route('/')
@app.route('/index/', methods=['GET'])
def index():
        return render_template('index.html', title='Home')

@app.route('/resources/')
def resources():
    resources = models.DataSet.query.order_by(models.DataSet.name).all()
    return render_template('resources.html', title="Resources", resources=resources)

@app.route('/genes/')
def genes():
    genes = models.Gene.query.with_entities(models.Gene.symbol, models.Gene.name).all()
    return render_template('genes.html', title="Genes", genes=genes)

@app.route('/about/')
def about():
    return render_template('about.html', title="About")

@app.route('/search/', methods=['POST'])
def search():
    app.vars['gene'] = request.form['gene']
    return redirect('/genepage/'+app.vars['gene'])

@app.route('/genepage/<variable>')
def genapage(variable):
    gene = models.Gene.query.filter_by(symbol=variable).first()
    if gene != None:
        return render_template('genepage.html', title=gene.symbol, gene=gene)
    else:
        return render_template('genenotfound.html', title='Not Found', gene=gene)

@app.route('/resourcepage/<variable>')
def resourcepage(variable):
    resource = models.DataSet.query.filter_by(name=variable).first()
    directory = 'bionetbay/static/processedFiles/'+resource.name+'/'
    files = os.listdir(directory)
    return render_template('resourcepage.html', title=resource.name, resource=resource, files=files, directory=directory)

@app.route("/downloadfile/")
def downloadfile():
    filename = request.args.get('filename')
    directory = request.args.get('directory')
    directory = directory[10:-1]
    try:
        return send_from_directory(directory=directory, filename=filename, as_attachment=True)
    except Exception as e:
        return str(e)
