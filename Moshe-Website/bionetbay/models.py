from bionetbay import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

class DataSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    description = db.Column(db.String(250), index=True, unique=False)
    measurement = db.Column(db.String(120), index=True, unique=False)
    association = db.Column(db.String(250), index=True, unique=False)
    category = db.Column(db.String(120), index=True, unique=False)
    sub_category = db.Column(db.String(120), index=True, unique=False)
    resource = db.Column(db.String(120), index=True, unique=False)
    numb_genes = db.Column(db.Integer, index=True, unique=False)
    numb_associations = db.Column(db.Integer, index=True, unique=False)
    numb_gene_associations = db.Column(db.Integer, index=True, unique=False)
    #posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<DataSet %r>' % (self.name)

class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=True)
    description = db.Column(db.String(2000), index=True, unique=True)
    external_link = db.Column(db.String(500), index=True, unique=True)
    #posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<DataSet %r>' % (self.name)

class Gene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(200), index=True, unique=False)
    old_symbol = db.Column(db.String(200), index=True, unique=False)
    old_name = db.Column(db.String(600), index=True, unique=False)
    synonyms = db.Column(db.String(200), index=True, unique=False)
    name_synonyms = db.Column(db.String(600), index=True, unique=False)
    chromosome = db.Column(db.String(64), index=True, unique=False)
    accession_numbers = db.Column(db.String(64), index=True, unique=False)
    entrez_gene_id = db.Column(db.String(64), index=True, unique=False)
    ensembl_gene_id = db.Column(db.String(64), index=True, unique=False)
    pubmed_ids = db.Column(db.String(64), index=True, unique=False)
    refseq_ids = db.Column(db.String(200), index=True, unique=False)
    uniprot_id = db.Column(db.String(400), index=True, unique=False)


    def __repr__(self):
        return '<DataSet %r>' % (self.name)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True, unique=False)
    dataset = db.Column(db.String(200), index=True, unique=False)
    file_type = db.Column(db.String(60), index=True, unique=False)
    external_link = db.Column(db.String(500), index=True, unique=False)
    date_submission = db.Column(db.String(120), index=True, unique=False)
    submitter = db.Column(db.String(120), index=True, unique=False)
    #posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<DataSet %r>' % (self.name)

class Citations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.String(200), index=True, unique=False)
    citation = db.Column(db.String(500), index=True, unique=False)
    #posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<DataSet %r>' % (self.name)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=False)
    _password = db.Column(db.String(128), index=True, unique=False)
    email = db.Column(db.String(128), index=True, unique=False)
    active = db.Column(db.Boolean, index=True, unique=False)
    #posts = db.relationship('Post', backref='author', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def __repr__(self):
        return '<DataSet %r>' % (self.name)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    stat = db.Column(db.Integer, index=True, unique=False)

    def __repr__(self):
        return '<DataSet %r>' % (self.name)

class SubCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    category = db.Column(db.String(120), index=True, unique=False)
    stat = db.Column(db.Integer, index=True, unique=False)

    def __repr__(self):
        return '<DataSet %r>' % (self.name)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post %r>' % (self.body)
