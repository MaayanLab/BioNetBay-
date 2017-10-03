from flask import render_template, request, redirect, send_from_directory
import os
import time
from bionetbay import app, db, models


@app.route('/')
@app.route('/index/', methods=['GET'])
def index():
    genes_l = models.Gene.query.with_entities(models.Gene.symbol).all()
    genes_list = [gene[0] for gene in genes_l]
    genes = models.Gene.query.count()
    datasets = models.DataSet.query.count()
    resources = models.Resources.query.count()
    return render_template('index.html', title='Home', genes=genes, datasets=datasets, resources=resources, genes_list=genes_list)

@app.route('/resources/')
def resources():
    resources = models.Resources.query.order_by(models.Resources.name).all()
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
        return render_template('genenotfound.html', title='Gene Not Found', gene=variable)


@app.route('/resourcepage/<variable>')
def resourcepage(variable):
    resource = models.Resources.query.filter_by(name=variable).first()
    datasets = models.DataSet.query.filter_by(resource=variable).all()
    citations = models.Citations.query.filter_by(resource=variable).all()
    return render_template('resourcepage.html', title=resource.name, resource=resource, datasets=datasets, citations=citations)

@app.route('/datasetpage/<variable>')
def datasetpage(variable):
    dataset = models.DataSet.query.filter_by(name=variable).first()
    files = models.Files.query.filter_by(dataset=variable).all()
    if dataset != None:
        return render_template('datasetpage.html', title=dataset.name, dataset=dataset, files=files)
    else:
        return render_template('datasetpage.html', title='Not Found', dataset=dataset)

@app.route("/downloadfile/")
def downloadfile():
    filename = request.args.get('filename')
    directory = request.args.get('directory')
    directory = directory[10:-1]
    try:
        return send_from_directory(directory=directory, filename=filename, as_attachment=True)
    except Exception as e:
        return str(e)
