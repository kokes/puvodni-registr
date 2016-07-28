
from urllib.request import urlretrieve
from lxml import etree
import pandas as pd


# seznam organu

szno = 'https://portal.gov.cz/portal/obcan/rejstriky/ogd/x-sovm.html'

szno = 'https://seznam.gov.cz/ovm/datafile.do?format=xml&service=seznamovm'
tfn = 'vstupy/org-ver-moc.xml'

urlretrieve(szno, tfn)


# otvirej

et = etree.parse(tfn).getroot()

mp = {
    'ico': [],
    'ds': [],
    'nazev': []
}
for subj in et.findall('./{%s}Subjekt' % et.nsmap[None]):
    ico = subj.find('./{%s}ICO' % et.nsmap[None])
#     if ico is None: continue
    idds = subj.find('./{%s}IdDS' % et.nsmap[None])
    nazev = subj.find('./{%s}Nazev' % et.nsmap[None])
    if nazev is None: continue

        
    mp['ico'].append(ico.text if ico is not None else '')
    mp['ds'].append(idds.text)
    mp['nazev'].append(nazev.text)
    

pd.DataFrame(mp).to_csv('vystupy/ico_ds.csv', index=None)

