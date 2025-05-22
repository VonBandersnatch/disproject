# 'Unpack' information in Afstemning table
# The 'konklusion' column contains information about who voted for and against
# Make a new table 'partistemmer' where data is arranged to be easier to access

import pandas as pd
import re

column_names = ['id', 'nummer', 'konklusion', 'vedtaget', 'kommentar', 'mødeid', 'typeid', 'sagstrinid', 'opdateringsdato']
VEDTAGET = {'vedtaget' : True, 'forkastet' : False}
# Database format has been changed twice, and the rows can be in 3 different formats.
REGEX_1 = r"\s*(Vedtaget|Forkastet)\s*(\d+) stemmer for forslaget (\D*)\s*(\d+) stemmer imod forslaget(\D*)\s*(\d+) stemmer hverken for eller imod forslaget(\D*)\s*"
REGEX_2 = r"\s*Forslaget blev (vedtaget|forkastet). For stemte (\d+) (\D*), imod stemte (\d+) ?(\D*), hverken for eller imod stemte (\d+)(\D*)"
REGEX_3 = r"\s*(Vedtaget|Forkastet)\s* For stemte (\d+) (\D*)\s*imod stemte (\d+) (\D*)\s*hverken for eller imod stemte (\d+) (\D*)\s*"
AFSTEMID = 'afstemningsid'
PARTI = 'parti'
FOR = 'stemme'

def clean_and_strip(partiliste:str):
    """Argument: A string containing a list of parti designations separated by commas
       Returns: The words from the list as a list of string, strippet for whitespace and
           trailing parantheses
    """
    partiliste = partiliste.replace(' og',',') # Replace 'og' (='and') with comma
    partiliste = partiliste.strip()
    if partiliste.startswith('('):
        partiliste = partiliste[1:]
    if partiliste.endswith(')'):
        partiliste = partiliste[:-1]
    if partiliste.endswith(').'):
        partiliste = partiliste[:-2]
    if partiliste.endswith(','):
        partiliste = partiliste[:-1]
    if partiliste in ['', '.']:
        return []
    else:
        return[parti.strip() for parti in partiliste.strip(' ').split(',')]


def unpack_conclusion(konklusion: str):
    """ Argument: One 'konklusion' from a vote from ft-data.
        Returns: A dictionary with the content:
            Whether the vote was passed, how many votes for, against and neither,
            and lists of parties voting for, against and neither.
            May return an empty dictionary for invalid input.
    """
    result = {}
    # Try matching konklusion with REGEX_1, REGEX_2 and REGEX_3
    pattern = re.compile(REGEX_1)
    match = pattern.match(konklusion)
    if not match:
        pattern = re.compile(REGEX_2)
        match = pattern.match(konklusion)
    if not match:
        pattern = re.compile(REGEX_3)
        match = pattern.match(konklusion)
    if match:
        grps = match.groups()
        result['Vedtaget'] = VEDTAGET[grps[0].lower()]
        result['Antal for'] = int(grps[1])
        result['Partier for'] = clean_and_strip(grps[2])
        result['Antal imod'] = int(grps[3])
        result['Partier imod'] = clean_and_strip(grps[4])
        result['Antal hverken for eller imod'] = int(grps[5])
        result['Partier hverken for eller imod'] = clean_and_strip(grps[6])
    return result

def get_subframe(df_row):
    """ Argument: One row from 'Afstemning.csv'
        Returns: A dataframe with voting data from that row, formatted as:
        (afstemningsid, parti, for eller imod)
        column names are decided by the constants AFSTEMID, PARTI, FOR
    """
    # A temporary list of rows, will be transformed into dataframe later
    rows = []
    s = df_row['konklusion']
    if isinstance(s,str):
        conclusion = unpack_conclusion(s)
        if conclusion != {}:
            afstemningsid = df_row['id']
            # Data is saved temporarily as a list of rows:
            for parti in conclusion['Partier for']:
                rows.append({AFSTEMID:afstemningsid, PARTI:parti, FOR:'For'})
            for parti in conclusion['Partier imod']:
                rows.append({AFSTEMID:afstemningsid, PARTI:parti, FOR:'Imod'})
            for parti in conclusion['Partier hverken for eller imod']:
                rows.append({AFSTEMID:afstemningsid, PARTI:parti, FOR:'Hverken'})
    # Create a dataframe with the rows found and return it.
    return pd.DataFrame(rows)

    
def create_partistemmer():
    """ Load and iterate through 'Afstemning.csv'
        Each row is split into several lines, one for each party
        (through the  get_subframe() function)
        Save the result in Partistemmer.csv
        Argument & return value: None.
    """    
    # afstemninger.csv has no column names.
    in_df =  pd.read_csv('afstemninger.csv', header=None, names = column_names)
    frames = [] # will hold subframes to be concatenated to form out_df
    for _, row in in_df.iterrows():
        new_data = get_subframe(row)
        frames.append(new_data)
    out_df = pd.concat(frames, ignore_index=True)
    # There are errors in the ft data: some data is repeated; remove this:
    out_df = out_df.drop_duplicates()
    out_df.to_csv('Partistemmer.csv')

create_partistemmer()



          
          