import pandas as pd
import numpy as np

def GMT_to_SIG(gmt_data, filename):
    
    gmt_dict = {x[0]: x[2:] for x in gmt_data}
                
    sig = pd.DataFrame([[x[0], y] for x in gmt_data for y in x[2:]])

    #Insert first four columns for .sig file format (NaNs)
    sig.insert(1, 'NA-1', str(np.nan))
    sig.insert(2, 'NA-2', str(np.nan))
    sig.insert(3, 'NA-3', str(np.nan))
    sig.insert(4, 'NA-4', str(np.nan))
                
    #Insert first four columns for .sig file format (NaNs)
    sig.insert(6, 'NA-5', str(np.nan))
    sig.insert(7, 'NA-6', str(np.nan))
    sig.insert(8, 'NA-7', str(np.nan))
    sig.insert(9, 'NA-8', str(np.nan))

    #Insert column corresponding to sign 
    sig.insert(10, 'Sign', str(np.nan))
                
    #Insert column specifying interaction type as unknown
    sig.insert(11, 'Interaction', str(np.nan))

    #Insert column specifying interaction type as unknown
    sig.insert(12, 'PubMed', str(np.nan))
    return sig

def SIG_to_Genes(sig, submission_fk, organism, engine):

    if len(sig.columns) != 13:
        return "Error"

    sig.columns = [0, 1, 2, 3, 4,5 , 6, 7, 8, 9, 10, 11, 12]

    #Read in species dataframe for use in program
    species_dataframe = pd.read_sql_query('SELECT * FROM species', engine)
    species_dataframe.head()
    
    interaction_dataframe = sig[[0, 5]]
    
    #Must obtain Organism of the individual kinases (if none available, use organism submitted by users)
    if interaction_dataframe[0].str.contains('_').all():
        interaction_dataframe['species'] = [x.split('_')[-1] for x in interaction_dataframe[0]]

        for index, species in interaction_dataframe.species.iteritems():
            if species in ['HUMAN', 'human', 'Human', 'hg19']:
                interaction_dataframe.species[index] = 'Homo sapiens'
            if species in ['MOUSE', 'mouse', 'Mouse', 'mm9']:
                interaction_dataframe.species[index] = 'Mus musculus'
            else:
                interaction_dataframe.species[index] = '%s' %organism
    elif interaction_dataframe[0].str.contains('-').all():
        interaction_dataframe['species'] = [x.split('-')[-1] for x in interaction_dataframe[0]]

        for index, species in interaction_dataframe.species.iteritems():
            if species in ['HUMAN', 'human', 'Human']:
                interaction_dataframe.species[index] = 'Homo sapiens'
            if species in ['MOUSE', 'mouse', 'Mouse']:
                interaction_dataframe.species[index] = 'Mus musculus' 
            else:
                interaction_dataframe.species[index] = '%s' %organism      
    else:
        interaction_dataframe['species'] = '%s' %organism
        
    
    pairs = interaction_dataframe.merge(species_dataframe, left_on='species', right_on='species_name', how='left')

    #Remove indication of species from name of the source and drop unnecessary columns if needed
    if interaction_dataframe[0].str.contains('_').all():
        pairs['source'] = [x.split('_')[:-1] for x in interaction_dataframe[0]]
        pairs['source'] = ['_'.join(x) for x in pairs['source']]
        pairs.drop(0, axis=1, inplace=True)
        pairs.drop('species', axis = 1, inplace = True)
        pairs.drop('species_name', axis =1, inplace = True)
        pairs.columns = ['target', 'species_id', 'source']
    elif interaction_dataframe[0].str.contains('-').all():
        pairs['source'] = [x.split('-')[:-1] for x in interaction_dataframe[0]]
        pairs['source'] = ['-'.join(x) for x in pairs['source']]
        pairs.drop(0, axis=1, inplace=True)
        pairs.drop('species', axis = 1, inplace = True)
        pairs.drop('species_name', axis =1, inplace = True)
        pairs.columns = ['target', 'species_id', 'source']
    else:
        pairs.drop('species', axis = 1, inplace = True)
        pairs.drop('species_name', axis =1, inplace = True)
        pairs.columns = ['source', 'target', 'species_id']
    
    # Need to uppercase all names in the dataframe to standardize names
    # across different files

    if type(pairs.source[0]) != type("Error"):
        return "Error"

    if type(pairs.target[0]) != type("Error"):
        return "Error"

    pairs['source'] = [name.upper() for name in pairs.source]
    pairs['target'] = [name.upper() for name in pairs.target]


    pairs.drop_duplicates(inplace=True)
    
    #Create separate dataframes for the source and target genes
    source_genes = pd.DataFrame(dict(gene_symbol = pairs.source, species_fk = pairs.species_id))
    source_genes.drop_duplicates(inplace=True)
    source_genes.reset_index(inplace=True, drop=True)
    target_genes = pd.DataFrame(dict(gene_symbol = pairs.target, species_fk = pairs.species_id))
    target_genes.drop_duplicates(inplace = True)
    target_genes.reset_index(inplace=True, drop=True)
    
    #Concat these genes into a single dataframe
    genes = pd.concat([source_genes, target_genes])
    genes.drop_duplicates(inplace=True)
    
    #Use INSERT_IGNORE to add these genes and targets to the dataframe
    insert_ignore = "INSERT IGNORE INTO genes (gene_symbol, species_fk) VALUES" + ', '.join(['("{gene_symbol}", {species_fk})'.format(**rowData) for index, rowData in genes.iterrows()])
    # Create or add new entries to the genes table using 'insert-ignore' functionality
    engine.execute(insert_ignore)
    genes_df = pd.read_sql_query('SELECT * FROM genes', engine)
    
    #Use genes table to isolate fk of these source and target genes
    #fk will later be used when creating the interaction database
    source_fk = pairs.merge(genes_df, how='left', left_on=['source', 'species_id'], 
                          right_on=['gene_symbol', 'species_fk'])
    source_fk.drop_duplicates(['source', 'target', 'species_id'], inplace = True)
    source_fk.drop(['source', 'target', 'species_id', 'species_fk',
                           'gene_symbol', 'description'], axis=1, inplace=True)
    target_fk = pairs.merge(genes_df, how='left', left_on=['target', 'species_id'], 
                        right_on=['gene_symbol', 'species_fk'])
    target_fk.drop_duplicates(['source', 'target', 'species_id'], inplace = True)
    target_fk.drop(['source', 'target', 'species_id', 
                           'gene_symbol', 'species_fk', 'description'], axis=1, inplace=True)

    #Create and format dataframe 'interactions' corresponding to all interactions in this SIG file
    interactions=pd.concat([source_fk, target_fk], axis = 1)
    interactions.insert(2, 'submission_fk', submission_fk)
    interactions.columns = ['source_gene_fk', 'target_gene_fk', 'submission_fk']

    if interaction_dataframe.isnull().values.any():
        return "Error"

    return interactions
