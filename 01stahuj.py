from lxml import etree
import requests
from urllib.request import urlretrieve
from urllib.parse import urlsplit
import os
import zipfile
from glob import glob
import json
from collections import OrderedDict

vst = 'vstupy'
vyst = 'vystupy'


# In[33]:

try:
    os.makedirs(os.path.join(vst, 'indexy'))
except:
    pass

try:
    os.makedirs(os.path.join(vst, 'smlouvy'))
except:
    pass


# Stahuj index

ind_url = 'https://portal.gov.cz/portal/rejstriky/data/10013/index.xml'

urlretrieve(ind_url, os.path.join(vst, 'index.xml'))


# Parsuj index
et = etree.parse(os.path.join(vst, 'index.xml')).getroot()

szn = et.findall('.//{%s}Seznam' % et.nsmap[None])


# Stahuj indexy

for sz in szn:
    url = sz.find('.//{%s}SeznamURL' % et.nsmap[None]).text
    fn = os.path.split(urlsplit(url).path)[-1]
    tfn = os.path.join(vst, 'indexy', fn)
    if os.path.isfile(tfn): continue
    
    r = requests.get(url)
    with open(tfn, 'wb') as f:
        f.write(r.content)


# Stahuj v ramci indexu

els = 'PREDMET, PARTNER_NAZEV, PARTNER_ICO, PARTNER_ADRESA, DATUM_VYSTAVENI, AGENDA, CISLO, SCHVALIL, CASTKA_BEZ_DPH, CASTKA_S_DPH, TYP_DOKUMENTU'.split(', ')

inds = glob(os.path.join(vst, 'indexy', '*.xml'))

for jf, ffn in enumerate(inds):
    print('Stahuju z indexu {}/{}'.format(jf+1, len(inds)))
    et = etree.parse(ffn).getroot()
    pls = et.findall('./{%s}Polozka' % et.nsmap[None])

    fn = os.path.split(ffn)[-1]
    # zf = zipfile.ZipFile(os.path.join(vst, 'smlouvy', '%s.zip' % fn[:-4]), 'w', zipfile.ZIP_DEFLATED)

    for j, el in enumerate(pls):
        print('Stahuju smlouvu {}/{}'.format(j+1, len(pls)), end='\r')
        if el.find('./{%s}Zneplatneny' % et.nsmap[None]).text == 'true': continue

        idd = el.find('./{%s}ID' % et.nsmap[None]).text
        url = el.find('./{%s}PolozkaURL' % et.nsmap[None]).text

        tdir = os.path.join(vst, 'smlouvy', '%d' % (int(idd) % 100))
        try:
            os.makedirs(tdir)
        except:
            pass
        tfn = os.path.join(tdir, '%s.json' % idd)
        if os.path.isfile(tfn): continue

        r = requests.get(url)
        if not r.ok:
            print('failnul %s/%s' % (fn, idd))
            continue
            
        try:
            sml = etree.fromstring(r.content)
        except:
            continue
            
        dt = OrderedDict.fromkeys(els)

        for el in els:
            dt[el] = sml.find('./{%s}%s' % (sml.nsmap[None], el)).text

        with open(tfn, 'w') as f:
            json.dump(dt, f, ensure_ascii=False)
        # zf.writestr('%s.json' % idd, dd)

    # zf.close()

