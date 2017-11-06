from flask import render_template, request, redirect, send_from_directory, flash, session, url_for
import os
import time
from bionetbay import app, db, models, mail
import datetime
from flask_mail import Message
from .emails import send_email
from itsdangerous import URLSafeTimedSerializer
from .forms import RegistrationForm, UsernamePasswordForm, EmailForm, PasswordForm, ResourceForm, DatasetForm, FileForm
from flask_login import login_user, logout_user, login_required, current_user
from collections import Counter

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
    files = models.Files.query.count()
    categories = models.DataSet.query.with_entities(models.DataSet.category).all()
    lst = []
    for element in categories:
        lst.append(element[0])
    count = dict(Counter(lst))
    return render_template('index.html', title='Home', genes=genes, datasets=datasets, resources=resources, files=files, genes_list=genes_list, count=count)

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
    form = ResourceForm()
    if form.validate_on_submit():
        entry = models.Resources(name=form.name.data, description=form.description.data, external_link=form.link.data)
        db.session.add(entry)
        db.session.commit()
        flash('Thank You for Contributing!', "alert alert-success")
        return redirect('/home')

    return render_template('contributeResource.html', title='ContributeResource', form=form)


@app.route("/contribute_dataset", methods=['GET', 'POST'])
def contributeDataset():
    resources = models.Resources.query.with_entities(models.Resources.name).all()
    form = DatasetForm()
    if form.validate_on_submit():
        entry = models.DataSet(name=form.name.data,
                                description=form.description.data,
                                measurement=form.measurement.data,
                                association=form.association.data,
                                category=form.category.data,
                                resource=form.resource.data,
                                numb_genes=form.number_of_genes.data,
                                numb_associations=form.number_of_samples.data,
                                numb_gene_associations=form.number_of_associations.data)
        db.session.add(entry)
        db.session.commit()
        flash('Thank You for Contributing!', "alert alert-success")
        return redirect('/home')

    return render_template('contributeDataset.html', title='ContributeDataset', resources=resources, form=form)

@app.route("/contribute_file", methods=['GET', 'POST'])
def contributeFile():
    form = FileForm()
    datasets = models.DataSet.query.with_entities(models.DataSet.name).all()
    if form.validate_on_submit():
        format = "%m-%d-%Y"
        today = datetime.datetime.today()
        entry = models.Files(name=form.name.data,
                                dataset=form.dataset.data,
                                file_type=form.file_type.data,
                                external_link=form.link.data,
                                date_submission=today.strftime(format),
                                submitter=current_user.username
                                )
        db.session.add(entry)
        db.session.commit()
        flash('Thank You for Contributing!', "alert alert-success")
        return redirect('/home')

    return render_template('contributeFile.html', title='ContributeFile', datasets=datasets, form=form)

@app.route("/loginPage")
def loginPage():
    return render_template('login.html', title='Login')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UsernamePasswordForm()
    if form.validate_on_submit():
        user = models.Users.query.filter_by(username=form.username.data).first()
        if user:
            if user.is_correct_password(form.password.data):
                if user.active==1:
                    login_user(user)

                    flash('Login Successful!')
                    return redirect('/home/')
                else:
                    flash('account not activated!', 'alert alert-danger')
                    return redirect("/login")
            else:
                flash('wrong password!', 'alert alert-danger')
                return redirect("/login")
        else:
            flash('username not in system!', 'alert alert-danger')
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
        if not models.Users.query.filter_by(username=form.username.data).first():
            if not models.Users.query.filter_by(email=form.email.data).first():
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
                flash('Account created', 'alert alert-success')
                flash('An email was sent to confimr your email', 'alert alert-success')
                return redirect('/home')
            else:
                flash('email already in system, please use unique email!', 'alert alert-danger')
                render_template('register.html', title='Create Account', form=form)
        else:
            flash('username already taken!', 'alert alert-danger')
            render_template('register.html', title='Create Account', form=form)
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

@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = models.Users.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"

        # Here we use the URLSafeTimedSerializer we created in `util` at the
        # beginning of the chapter
        token = ts.dumps(user.email, salt='recover-key')

        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'recover.html',
            recover_url=recover_url)

        # Let's assume that send_email was defined in myapp/util.py
        send_email(subject, [user.email], html)

        flash('An email has been sent')
        return redirect('/home')
    return render_template('reset.html', form=form)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = models.Users.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        flash('Password Reset Successful!', "alert alert-success")
        return redirect('/login')

    return render_template('reset_with_token.html', form=form, token=token)
