# 'Unpack' information i Afstemning-tabel
# Kolonne konklusion indeholder information om hvem der har stemt for og imod
# Ikke færdig!
import re

VEDTAGET = {'Vedtaget' : True, 'Forkastet' : False}
REGEX_FOR = r"(\d+) stemmer for forslaget \((.*?)\)"
REGEX_NUL_FOR = r"0 stemmer for forslaget \((.*?)\)"
REGEX_NUL_IMOD = r"0 stemmer imod forslaget"
REGEX_IMOD = r"(\d+) stemmer imod forslaget \((.*?)\)"
REGEX_NUL_HVERKEN = r"0 stemmer hverken for eller imod forslaget"
REGEX_HVERKEN = r"(\d+) stemmer hverken for eller imod forslaget \((.*?)\)"

def get_content(konklusion: str):
    """ Parameter: En 'konklusion' fra en afstemning fra ft-data.
        Returns: En dictionary med indholdet - om forslaget blev vedtaget
    """
    result = {}
    for line in konklusion.split('\n'):
        # Blev forslaget vedtaget?
        if line in VEDTAGET.keys():
            result['Vedtaget'] = VEDTAGET[line]
        # Find hvilke partier stemte for forslaget? (hvis mindst 1 stemme for)
        pattern = re.compile(REGEX_FOR)
        match = pattern.match(line)
        if match:
            groups = match.groups()
            result['Antal for'] = int(groups[0])
            result['Partier for'] = groups[1].split(',')
            
    print(result)
    
# Testeksempel    

test_konklusion = """Forkastet

8 stemmer for forslaget (EL)

98 stemmer imod forslaget (V, S, DF, RV, SF, LA, KF)

0 stemmer hverken for eller imod forslaget

"""

get_content(test_konklusion)
          
          