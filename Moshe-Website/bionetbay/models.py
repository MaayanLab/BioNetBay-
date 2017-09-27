from bionetbay import db

class DataSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(120), index=True, unique=True)
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

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post %r>' % (self.body)
