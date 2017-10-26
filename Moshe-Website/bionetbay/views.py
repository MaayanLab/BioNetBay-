from flask import render_template, request, redirect, send_from_directory, flash, session, url_for
import os
import time
from bionetbay import app, db, models, mail
import datetime
from flask_mail import Message
from .emails import send_email
from itsdangerous import URLSafeTimedSerializer
from .forms import RegistrationForm, UsernamePasswordForm
from flask_login import login_user, logout_user, login_required

app.secret_key = 'fbhwgcovmy'

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

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
@login_required
def contribute():
    return render_template('contribute.html', title='Contribute')

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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UsernamePasswordForm()
    if form.validate_on_submit():
        user = models.Users.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data) and user.active==1:
            login_user(user)

            flash('Login Successful!')
            return redirect('/home/')

        else:
            flash('wrong password!')
            return redirect("/login")

    return render_template('login.html', title='Login', form=form)

    # POST_USERNAME = str(request.form['username'])
    # POST_PASSWORD = str(request.form['password'])
    #
    # found = models.Users.query.filter_by(username=POST_USERNAME, password=POST_PASSWORD).first()
    #
    # if found and found.active==1:
    #     session['logged_in'] = True
    #     session['user'] = POST_USERNAME
    #     flash('Login Successful!')
    #     return redirect('/home/')
    # else:
    #     flash('wrong password!')
    #     return redirect('/loginPage')

@app.route("/logout")
def logout():
    logout_user()
    flash('Successfully Logged Out!')
    return redirect('/home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        newUser = models.Users(username=form.username.data,
                            password=form.password.data,
                            email=form.email.data,
                            active=0
                            )
        db.session.add(newUser)
        db.session.commit()

        # Now we'll send the email confirmation link
        subject = "Confirm your email"

        token = ts.dumps('moshe.silverstein@mssm.edu', salt='email-confirm-key')

        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)

        html = render_template(
            'activate.html',
            confirm_url=confirm_url)

        send_email(subject, [newUser.email], html)

        return redirect('/home')
    return render_template('register.html', title='Create Account', form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = models.Users.query.filter_by(email=email).first_or_404()

    user.active = 1

    db.session.add(user)
    db.session.commit()

    session['logged_in'] = True
    session['user'] = user.username

    flash('Your account is now active!')
    return redirect('/home')
