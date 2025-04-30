# 'Unpack' information i Afstemning-tabel
# Kolonne konklusion indeholder information om hvem der har stemt for og imod
# Lav en ny tabel med 'partistemmer' for hver afstemning

import pandas as pd
import re

VEDTAGET = {'Vedtaget' : True, 'Forkastet' : False}
REGEX_FOR = r"(\d+) stemmer for forslaget \((.*?)\)$"
REGEX_NUL_FOR = r"0 stemmer for forslaget \((.*?)\)"
REGEX_NUL_IMOD = r"0 stemmer imod forslaget"
REGEX_IMOD = r"(\d+) stemmer imod forslaget \((.*?)\)$"
REGEX_NUL_HVERKEN = r"0 stemmer hverken for eller imod forslaget"
REGEX_HVERKEN = r"(\d+) stemmer hverken for eller imod forslaget \((.*?)\)$"
AFSTEMID = 'Afstemningsid'
PARTI = 'Parti'
FOR = 'For/imod/hverken'

def clean_and_strip(partiliste:str):
    """Parameter: En string som indeholder liste med (f.eks.) partibetegnelser, kommasepareret
       Returns: Ordene i denne string som en liste, strippet for whitespace
    """
    return[parti.strip() for parti in partiliste.split(',')]


def unpack_conclusion(konklusion: str):
    """ Parameter: En 'konklusion' fra en afstemning fra ft-data.
        Returns: En dictionary med indholdet - om forslaget blev vedtaget
    """
    result = {}
    # Split conclusion into lines and remove whitespace
    lines = konklusion.split('\n')
    lines = [line.lstrip() for line in lines]
    # Match each line using regex and save the result in result
    for line in lines:
        # Blev forslaget vedtaget?
        if line in VEDTAGET.keys():
            result['Vedtaget'] = VEDTAGET[line]
        # Find hvilke partier stemte for forslaget? (hvis mindst 1 stemme for)
        pattern = re.compile(REGEX_FOR)
        match = pattern.match(line)
        if match:
            groups = match.groups()
            result['Antal for'] = int(groups[0])
            result['Partier for'] = clean_and_strip(groups[1])
        # Find hvilke partier stemte for forslaget? (hvis ingen for)
        pattern = re.compile(REGEX_NUL_FOR)
        match = pattern.match(line)
        if match:
            groups = match.groups()
            result['Antal for'] = 0
            result['Partier for'] = []
        # Find hvilke partier stemte imod forslaget? (hvis mindst 1 stemme imod)
        pattern = re.compile(REGEX_IMOD)
        match = pattern.match(line)
        if match:
            groups = match.groups()
            result['Antal imod'] = int(groups[0])
            result['Partier imod'] = clean_and_strip(groups[1])
        # Find hvilke partier stemte imod forslaget? (hvis ingen imod)
        pattern = re.compile(REGEX_NUL_IMOD)
        match = pattern.match(line)
        if match:
            groups = match.groups()
            result['Antal imod'] = 0
            result['Partier imod'] = []
        # Find hvilke partier stemte hverken for eller imod forslaget? (hvis mindst 1 stemme hverken for eller imod)
        pattern = re.compile(REGEX_HVERKEN)
        match = pattern.match(line)
        if match:
            groups = match.groups()
            result['Antal hverken for eller imod'] = int(groups[0])
            result['Partier hverken for eller imod'] = clean_and_strip(groups[1])
        # Find hvilke partier stemte hverken for eller imod forslaget? (hvis ingen stemmer hverken for eller imod)
        pattern = re.compile(REGEX_NUL_HVERKEN)
        match = pattern.match(line)
        if match:
            groups = match.groups()
            result['Antal hverken for eller imod'] = 0
            result['Partier hverken for eller imod'] = []            
    return result

def get_subframe(df_row):
    """ Parameter: En række fra 'Afstemning.csv'
        Returns: En dataframe med afstemningsdata fra rækken, i format:
        (afstemningsid, parti, for eller imod)
        kolonnenavne bestemmes af konstanterne AFSTEMID, PARTI, FOR
    """
    # Create an empty new dataframe to hold contents of the parameter row
    # df = pd.DataFrame(columns=[AFSTEMID,PARTI,FOR])
    conclusion = unpack_conclusion(df_row['konklusion'])
    afstemningsid = df_row['id']
    # Data is saved temporarily as a list of rows:
    rows = []
    for parti in conclusion['Partier for']:
        rows.append({AFSTEMID:afstemningsid, PARTI:parti, FOR:'For'})
    for parti in conclusion['Partier imod']:
        rows.append({AFSTEMID:afstemningsid, PARTI:parti, FOR:'Imod'})
    for parti in conclusion['Partier hverken for eller imod']:
        rows.append({AFSTEMID:afstemningsid, PARTI:parti, FOR:'Hverken'})

    return pd.DataFrame(rows)

    
def create_partistemmer():
    """ Indlæs 'Afstemning.csv', gennemløb denne.
        Hver række deles op i en linje for hvert parti (gennem at kalde get_subframe())
        Resultat gemmes i Partistemmer.csv
    """    
    in_df =  pd.read_csv('Afstemning.csv')
    frames = [] # will hold subframes to be concatenated to form out_df
    for _, row in in_df.iterrows():
        new_data = get_subframe(row)
        frames.append(new_data)
    out_df = pd.concat(frames, ignore_index=True)
    out_df.to_csv('Partistemmer.csv')




create_partistemmer()
          
          