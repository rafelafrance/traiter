"""Patterns for US states."""

# pylint: disable=too-many-lines

import re
from pylib.shared import patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog

CATALOG = RuleCatalog(patterns.CATALOG)

CATALOG.term('USA', r"""
    U\.?S\.?A\.? | U\.?S\.?
    | United \s? States \s? of \s? America | United \s? States
    | U\.? \s? of \s? A\.?""")

CATALOG.term('AL_abbrev', r""" A\.?L\.? | Ala\.? """)
CATALOG.term('Alabama', r' Alabama ')
CATALOG.grouper('AL', ' AL_abbrev | Alabama ')

CATALOG.term('AK_abbrev', r""" A\.?K\.? | Alas\.? """)
CATALOG.term('Alaska', r' Alaska ')
CATALOG.grouper('AK', ' AK_abbrev | Alaska ')

CATALOG.term('AZ_abbrev', r""" A\.?Z\.? | Ariz\.? """)
CATALOG.term('Arizona', r' Arizona ')
CATALOG.grouper('AZ', ' AZ_abbrev | Arizona ')

CATALOG.term('AR_abbrev', r""" A\.?R\.? | Ark\.? """)
CATALOG.term('Arkansas', r' Arkansas ')
CATALOG.grouper('AR', ' AR_abbrev | Arkansas ')

CATALOG.term('CA_abbrev', r""" C\.?A\.? | C\.?F\.? | Calif\.? | Cal\.? """)
CATALOG.term('California', r' California ')
CATALOG.grouper('CA', ' CA_abbrev | California ')

CATALOG.term('CO_abbrev', r""" C\.?O\.? | C\.?L\.? | Colo\.? | Col\.? """)
CATALOG.term('Colorado', r' Colorado ')
CATALOG.grouper('CO', ' CO_abbrev | Colorado ')

CATALOG.term('CT_abbrev', r""" C\.?T\.? | Conn\.? """)
CATALOG.term('Connecticut', r' Connecticut ')
CATALOG.grouper('CT', ' CT_abbrev | Connecticut ')

CATALOG.term('DE_abbrev', r""" D\.?E\.? | D\.?L\.? | Del\.? """)
CATALOG.term('Delaware', r' Delaware ')
CATALOG.grouper('DE', ' DE_abbrev | Delaware ')

CATALOG.term('FL_abbrev', r""" F\.?L\.? | Fla\.? | Flor\.? """)
CATALOG.term('Florida', r' Florida ')
CATALOG.grouper('FL', ' FL_abbrev | Florida ')

CATALOG.term('GA_abbrev', r""" G\.?A\.? | Geo\.? """)
CATALOG.term('Georgia', r' Georgia ')
CATALOG.grouper('GA', ' GA_abbrev | Georgia ')

CATALOG.term('HI_abbrev', r""" H\.?I\.? | H\.?A\.? """)
CATALOG.term('Hawaii', r' Hawaii ')
CATALOG.grouper('HI', ' HI_abbrev | Hawaii ')

CATALOG.term('ID_abbrev', r""" I\.?D\.? | Ida\.? """)
CATALOG.term('Idaho', r' Idaho ')
CATALOG.grouper('ID', ' ID_abbrev | Idaho ')

CATALOG.term('IL_abbrev', r"""  I\.?L\.? | Ill\.? | Ills\.? | Ill's """)
CATALOG.term('Illinois', r' Illinois ')
CATALOG.grouper('IL', ' IL_abbrev | Illinois ')

CATALOG.term('IN_abbrev', r""" I\.?N\.? | Ind\.? """)
CATALOG.term('Indiana', r' Indiana ')
CATALOG.grouper('IN', ' IN_abbrev | Indiana ')

CATALOG.term('IA_abbrev', r""" I\.?A\.? | Ioa\.? """)
CATALOG.term('Iowa', r' Iowa ')
CATALOG.grouper('IA', ' IA_abbrev | Iowa ')

CATALOG.term('KS_abbrev', r""" K\.?S\.? | K\.?A\.? | Kans\.? | Kan\.? """)
CATALOG.term('Kansas', r' Kansas ')
CATALOG.grouper('KS', ' KS_abbrev | Kansas ')

CATALOG.term('KY_abbrev', r""" K\.?Y\.? | Ken\.? | Kent\.? """)
CATALOG.term('Kentucky', r' Kentucky ')
CATALOG.grouper('KY', ' KY_abbrev | Kentucky ')

CATALOG.term('LA_abbrev', r""" L\.?A\.? """)
CATALOG.term('Louisiana', r' Louisiana ')
CATALOG.grouper('LA', ' LA_abbrev | Louisiana ')

CATALOG.term('ME_abbrev', r""" M\.?E\.? """)
CATALOG.term('Maine', r' Maine ')
CATALOG.grouper('ME', ' ME_abbrev | Maine ')

CATALOG.term('MD_abbrev', r""" M\.?D\.? | Mar\.? | Mary\.? """)
CATALOG.term('Maryland', r' Maryland ')
CATALOG.grouper('MD', ' MD_abbrev | Maryland ')

CATALOG.term('MA_abbrev', r""" M\.?A\.? | Mass\.? """)
CATALOG.term('Massachusetts', r' Massachusetts ')
CATALOG.grouper('MA', ' MA_abbrev | Massachusetts ')

CATALOG.term('MI_abbrev', r""" M\.?I\.? | M\.?C\.? | Mich\.? """)
CATALOG.term('Michigan', r' Michigan ')
CATALOG.grouper('MI', ' MI_abbrev | Michigan ')

CATALOG.term('MN_abbrev', r""" M\.?N\.? | Minn\.? """)
CATALOG.term('Minnesota', r' Minnesota ')
CATALOG.grouper('MN', ' MN_abbrev | Minnesota ')

CATALOG.term('MS_abbrev', r""" M\.?S\.? | Miss\.? """)
CATALOG.term('Mississippi', r' Mississippi ')
CATALOG.grouper('MS', ' MS_abbrev | Mississippi ')

CATALOG.term('MO_abbrev', r""" M\.?O\.? """)
CATALOG.term('Missouri', r' Missouri ')
CATALOG.grouper('MO', ' MO_abbrev | Missouri ')

CATALOG.term('MT_abbrev', r""" M\.?T\.? | Mont\.? """)
CATALOG.term('Montana', r' Montana ')
CATALOG.grouper('MT', ' MT_abbrev | Montana ')

CATALOG.term('NE_abbrev', r""" N\.?E\.? | N\.?B\.? | Nebr\.? | Neb\.? """)
CATALOG.term('Nebraska', r' Nebraska ')
CATALOG.grouper('NE', ' NE_abbrev | Nebraska ')

CATALOG.term('NV_abbrev', r""" N\.?V\.? | Nev\.? """)
CATALOG.term('Nevada', r' Nevada ')
CATALOG.grouper('NV', ' NV_abbrev | Nevada ')

CATALOG.term('NH_abbrev', r""" N\.?H\.? """)
CATALOG.term('New_Hampshire', r' New \s? Hampshire ')
CATALOG.grouper('NH', ' NH_abbrev | New_Hampshire ')

CATALOG.term('NJ_abbrev', r""" N\.?J\.? | N\.?Jersey """)
CATALOG.term('New_Jersey', r' New \s? Jersey ')
CATALOG.grouper('NJ', ' NJ_abbrev | New_Jersey ')

CATALOG.term('NM_abbrev', r""" N\.?M\.? | N\.? \s? Mex\.? | New \s? M\.? """)
CATALOG.term('New_Mexico', r' New \s? Mexico ')
CATALOG.grouper('NM', ' NM_abbrev | New_Mexico ')

CATALOG.term('NY_abbrev', r""" N\.? \s? Y\.? | N\.? \s? York """)
CATALOG.term('New_York', r' New \s? York ')
CATALOG.grouper('NY', ' NY_abbrev | New_York ')

CATALOG.term('NC_abbrev', r""" N\.?C\.? | N\.? \s? Car\.? """)
CATALOG.term('North_Carolina', r' North \s? Carolina ')
CATALOG.grouper('NC', ' NC_abbrev | North_Carolina ')

CATALOG.term('ND_abbrev', r""" N\.?D\.? | N\.? Dak\.? | No\.? \s? Dak """)
CATALOG.term('North_Dakota', r' North \s? Dakota ')
CATALOG.grouper('ND', ' ND_abbrev | North_Dakota ')

CATALOG.term('OH_abbrev', r""" O\.?H\.? """)
CATALOG.term('Ohio', r' Ohio ')
CATALOG.grouper('OH', ' OH_abbrev | Ohio ')

CATALOG.term('OK_abbrev', r""" O\.?K\.? | Okla\.? """)
CATALOG.term('Oklahoma', r' Oklahoma ')
CATALOG.grouper('OK', ' OK_abbrev | Oklahoma ')

CATALOG.term('OR_abbrev', r""" O\.?R\.? | Oreg\.? | Ore\.? """)
CATALOG.term('Oregon', r' Oregon ')
CATALOG.grouper('OR', ' OR_abbrev | Oregon ')

CATALOG.term('PA_abbrev', r""" P\.?A\.? | Penn\.? | Penna\.? """)
CATALOG.term('Pennsylvania', r' Pennsylvania ')
CATALOG.grouper('PA', ' PA_abbrev | Pennsylvania ')

CATALOG.term('RI_abbrev', r""" R\.?I\.? | P\.?P\.? | R\.? \s? Isl\.? """)
CATALOG.term('Rhode_Island', r' Rhode \s? Island ')
CATALOG.grouper('RI', ' RI_abbrev | Rhode_Island ')

CATALOG.term('SC_abbrev', r""" S\.?C\.? | S\.? \s? Car\.? """)
CATALOG.term('South_Carolina', r' South \s? Carolina ')
CATALOG.grouper('SC', ' SC_abbrev | South_Carolina ')

CATALOG.term('SD_abbrev', r""" S\.?D\.? | S\.? \s? Dak\.? | So\.? \s? Dak """)
CATALOG.term('South_Dakota', r' South \s? Dakota ')
CATALOG.grouper('SD', ' SD_abbrev | South_Dakota ')

CATALOG.term('TN_abbrev', r""" T\.?N\.? | Tenn\.? """)
CATALOG.term('Tennessee', r' Tennessee ')
CATALOG.grouper('TN', ' TN_abbrev | Tennessee ')

CATALOG.term('TX_abbrev', r""" T\.?X\.? | Tex\.? """)
CATALOG.term('Texas', r' Texas ')
CATALOG.grouper('TX', ' TX_abbrev | Texas ')

CATALOG.term('UT_abbrev', r""" U\.?T\.? """)
CATALOG.term('Utah', r' Utah ')
CATALOG.grouper('UT', ' UT_abbrev | Utah ')

CATALOG.term('VT_abbrev', r"""  V\.?T\.? """)
CATALOG.term('Vermont', r' Vermont ')
CATALOG.grouper('VT', ' VT_abbrev | Vermont ')

CATALOG.term('VA_abbrev', r"""  V\.?A\.? | Virg\.? """)
CATALOG.term('Virginia', r' Virginia ')
CATALOG.grouper('VA', ' VA_abbrev | Virginia ')

CATALOG.term('WA_abbrev', r""" W\.?A\.? | W\.?N\.?| Wash\.? """)
CATALOG.term('Washington', r' Washington ')
CATALOG.grouper('WA', ' WA_abbrev | Washington ')

CATALOG.term('WV_abbrev', r""" W\.?V\.? | W\.? \s? Va\.? | W\.? \s? Virg\.? """)
CATALOG.term('West_Virginia', r' West \s? Virginia ')
CATALOG.grouper('WV', ' WV_abbrev | West_Virginia ')

CATALOG.term('WI_abbrev', r""" W\.?I\.? | W\.?S\.? | Wis\.? | Wisc\.? """)
CATALOG.term('Wisconsin', r' Wisconsin ')
CATALOG.grouper('WI', ' WI_abbrev | Wisconsin ')

CATALOG.term('WY_abbrev', r""" W\.?Y\.? | Wyo\.? """)
CATALOG.term('Wyoming', r' Wyoming ')
CATALOG.grouper('WY', ' WY_abbrev | Wyoming ')

CATALOG.term('DC', r"""
    D\.?C\.? | Wash\.? D\.?C\.? | District \s? of \s? Columbia """)

CATALOG.term('AS', r"""
    A\.?S\.? | ASM | American \s? Samoa """)

CATALOG.term('GU', r""" G\.?U\.? | GUM | Guam """)

CATALOG.term('MP', r"""
    M\.?P\.? | MNP | C\.?M\.?| CNMI | Northern \s? Mariana \s? Islands """)

CATALOG.term('PR', r""" P\.?R\.? | PRI | Puerto \s? Rico """)

CATALOG.term('VI', r"""
    V\.?I\.? | VIR | U\.?S\.?V\.?I\.? | Virgin \s? Islands """)

CATALOG.term('UM', r"""
    U\.?M\.? | United \s? States \s? Minor \s? Outlying \s? Islands """)

CATALOG.grouper('us_state', """
    AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS
    MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI
    WY AS GU MP PR VI UM """.split())

NORMALIZE_US_STATE = {
    'al': 'Alabama', 'ala': 'Alabama',
    'ak': 'Alaska', 'alas': 'Alaska',
    'az': 'Arizona', 'ariz': 'Arizona',
    'ar': 'Arkansas', 'ark': 'Arkansas',
    'ca': 'California', 'cf': 'California', 'calif': 'California',
    'cal': 'California',
    'co': 'Colorado', 'cl': 'Colorado', 'colo': 'Colorado', 'col': 'Colorado',
    'ct': 'Connecticut', 'conn': 'Connecticut',
    'de': 'Delaware', 'dl': 'Delaware', 'del': 'Delaware',
    'fl': 'Florida', 'fla': 'Florida', 'flor': 'Florida',
    'ga': 'Georgia', 'geo': 'Georgia',
    'hi': 'Hawaii', 'ha': 'Hawaii',
    'id': 'Idaho', 'Ida': 'Idaho',
    'il': 'Illinois', 'ill': 'Illinois', 'ills': 'Illinois',
    'in': 'Indiana', 'ind': 'Indiana',
    'ia': 'Iowa', 'Ioa': 'Iowa',
    'ks': 'Kansas', 'ka': 'Kansas', 'kans': 'Kansas', 'kan': 'Kansas',
    'ky': 'Kentucky', 'ken': 'Kentucky', 'kent': 'Kentucky',
    'la': 'Louisiana',
    'me': 'Maine',
    'md': 'Maryland', 'mar': 'Maryland', 'mary': 'Maryland',
    'ma': 'Massachusetts', 'mass': 'Massachusetts',
    'mi': 'Michigan', 'mc': 'Michigan', 'mich': 'Michigan',
    'mn': 'Minnesota', 'minn': 'Minnesota',
    'ms': 'Mississippi', 'miss': 'Mississippi',
    'mo': 'Missouri',
    'mt': 'Montana', 'mont': 'Montana',
    'ne': 'Nebraska', 'nb': 'Nebraska', 'nebr': 'Nebraska', 'neb': 'Nebraska',
    'nv': 'Nevada', 'nev': 'Nevada',
    'nh': 'New Hampshire',
    'nj': 'New Jersey', 'njersey': 'New Jersey',
    'nm': 'New Mexico', 'nmex': 'New Mexico', 'newm': 'New Mexico',
    'ny': 'New York', 'nyork': 'New York',
    'nc': 'North Carolina', 'ncar': 'North Carolina',
    'nd': 'North Dakota', 'ndak': 'North Dakota', 'nodak': 'North Dakota',
    'oh': 'Ohio',
    'ok': 'Oklahoma', 'okla': 'Oklahoma',
    'or': 'Oregon', 'oreg': 'Oregon', 'ore': 'Oregon',
    'ri': 'Rhode Island', 'pp': 'Rhode Island', 'risl': 'Rhode Island',
    'sc': 'South Carolina', 'scar': 'South Carolina',
    'sd': 'South_Dakota', 'sdak': 'South_Dakota', 'sodak': 'South_Dakota',
    'tn': 'Tennessee', 'tenn': 'Tennessee',
    'tx': 'Texas', 'tex': 'Texas',
    'ut': 'Utah',
    'vt': 'Vermont',
    'va': 'Virginia', 'virg': 'Virginia',
    'wa': 'Washington', 'wn': 'Washington', 'wash': 'Washington',
    'wv': 'West Virginia', 'wva': 'West Virginia', 'wvirg': 'West Virginia',
    'wi': 'Wisconsin', 'ws': 'Wisconsin', 'wis': 'Wisconsin',
    'wisc': 'Wisconsin',
    'wy': 'Wyoming', 'wyo': 'Wyoming',
    'dc': 'Washington D.C.', 'washdc': 'Washington D.C.',
    'districtofcolumbia': 'Washington D.C.',
    'as': 'American Samoa', 'asm': 'American Samoa',
    'gu': 'Guam', 'gum': 'Guam',
    'mp': 'Northern Mariana Islands', 'mnp': 'Northern Mariana Islands',
    'cm': 'Northern Mariana Islands', 'cnmi': 'Northern Mariana Islands',
    'pr': 'Puerto Rico', 'pri': 'Puerto Rico',
    'vi': 'U.S. Virgin Islands', 'vir': 'U.S. Virgin Islands',
    'usvi': 'U.S. Virgin Islands',
    'um': 'United States Minor Outlying Islands',
}


def normalize_state(state: str) -> str:
    """Convert state abbreviations to the state name."""
    norm = re.sub(r'[^a-z]+', '', state.lower())
    return NORMALIZE_US_STATE.get(norm, state.title())
