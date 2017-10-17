from flask import render_template, request, redirect, send_from_directory, flash, session
import os
import time
from bionetbay import app, db, models
import datetime

app.secret_key = 'random string'

@app.route('/')
@app.route('/home/', methods=['GET'])
def index():
    # genes_l = models.Gene.query.with_entities(models.Gene.symbol).all()
    # genes_list = [gene[0] for gene in genes_l]
    genes_list = []
    genes = models.Gene.query.count()
    datasets = models.DataSet.query.count()
    resources = models.Resources.query.count()
    return render_template('index.html', title='Home', genes=genes, datasets=datasets, resources=resources, genes_list=genes_list)

@app.route('/resources/')
def resources():
    resources = models.Resources.query.order_by(models.Resources.name).all()
    datasets = models.DataSet.query.with_entities(models.DataSet.category, models.DataSet.resource).distinct()
    return render_template('resources.html', title="Resources", resources=resources, datasets=datasets)
    # else:
    #     subquery = models.DataSet.query.filter(models.DataSet.category == request.form['filter']).with_entities(models.DataSet.resource).subquery()
    #     resources = models.Resources.query.filter(models.Resources.name.in_(subquery)).all()
    #     return render_template('resources.html', title="Resources", resources=resources)

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

@app.route("/contribute/")
def contribute():
    if session['logged_in'] == True:
        return render_template('contribute.html', title='Contribute')
    else:
        flash('You must be logged in to contribute!')
        return redirect('/loginPage')

@app.route("/contribute_resource", methods=['GET', 'POST'])
def contributeResource():
    if request.method == 'GET':
        return render_template('contributeResource.html', title='ContributeResource')
    else:
        entry = models.Resources(name=request.form['new_submission_name'], description=request.form['new_submission_description'], external_link=request.form['new_submission_link'])
        db.session.add(entry)
        db.session.commit()
        flash('Thank You for Contributing!')
        return redirect('/home/')


@app.route("/contribute_dataset", methods=['GET', 'POST'])
def contributeDataset():
    if request.method == 'GET':
        resources = models.Resources.query.with_entities(models.Resources.name).all()
        return render_template('contributeDataset.html', title='ContributeDataset', resources=resources)
    else:
        entry = models.DataSet(name=request.form['new_submission_name'],
                                description=request.form['new_submission_description'],
                                measurement=request.form['new_submission_measurement'],
                                association=request.form['new_submission_association'],
                                category=request.form['new_submission_category'],
                                resource=request.form['new_input_resource'],
                                numb_genes=request.form['new_submission_number_of_genes'],
                                numb_associations=request.form['new_submission_number_of_samples'],
                                numb_gene_associations=request.form['new_submission_number_of_associations'])
        db.session.add(entry)
        db.session.commit()
        flash('Thank You for Contributing!')
        return redirect('/home/')

@app.route("/contribute_file", methods=['GET', 'POST'])
def contributeFile():
    if request.method == 'GET':
        datasets = models.DataSet.query.with_entities(models.DataSet.name).all()
        return render_template('contributeFile.html', title='ContributeFile', datasets=datasets)
    else:
        format = "%m-%d-%Y"
        today = datetime.datetime.today()
        entry = models.Files(name=request.form['new_file_name'],
                                dataset=request.form['new_input_dataset'],
                                file_type=request.form['new_input_filetype'],
                                external_link=request.form['new_submission_link'],
                                date_submission=today.strftime(format)
                                )
        db.session.add(entry)
        db.session.commit()
        flash('Thank You for Contributing!')
        return redirect('/home/')

@app.route("/loginPage")
def loginPage():
    return render_template('login.html', title='Login')


@app.route("/login", methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    found = models.Users.query.filter_by(username=POST_USERNAME, password=POST_PASSWORD).first()

    if found:
        session['logged_in'] = True
        session['user'] = POST_USERNAME
        flash('Login Successful!')
        return redirect('/home/')
    else:
        flash('wrong password!')
        return redirect('/loginPage')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash('Successfully Logged Out!')
    return redirect('/home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Create Account')
    else:
        newUser = models.Users(username=request.form['new_username'],
                            password=request.form['new_password']
                            )
        db.session.add(newUser)
        db.session.commit()
        session['logged_in'] = True
        session['user'] = request.form['new_username']
        return redirect('/home')
