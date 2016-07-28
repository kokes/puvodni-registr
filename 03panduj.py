from lxml import etree
import os
import re
import json
from collections import OrderedDict
import tarfile
from glob import glob
import pandas as pd
import numpy as np


# Z ID do kodu datovy schranky

idpub = dict()
inds = glob(os.path.join('vstupy', 'indexy', '*.xml'))

for jf, ffn in enumerate(inds):
    # print('Stahuju z indexu {}/{}'.format(jf+1, len(inds)))
    et = etree.parse(ffn).getroot()
    pls = et.findall('./{%s}Polozka' % et.nsmap[None])

    fn = os.path.split(ffn)[-1]
    # zf = zipfile.ZipFile(os.path.join(vst, 'smlouvy', '%s.zip' % fn[:-4]), 'w', zipfile.ZIP_DEFLATED)

    for j, el in enumerate(pls):
        # print('Stahuju smlouvu {}/{}'.format(j+1, len(pls)), end='\r')
        if el.find('./{%s}Zneplatneny' % et.nsmap[None]).text == 'true': continue

        idd = el.find('./{%s}ID' % et.nsmap[None]).text
        pub = el.find('./{%s}Publikator' % et.nsmap[None]).text # datovka
        idpub[idd] = pub


# z datovky do ICO

ds = pd.read_csv('vystupy/ico_ds.csv')
dsico = ds.set_index('ds').to_dict()['ico']
dssubj = ds.set_index('ds').to_dict()['nazev']

els = 'PREDMET, PARTNER_NAZEV, PARTNER_ICO, PARTNER_ADRESA, DATUM_VYSTAVENI, AGENDA, CISLO, SCHVALIL, CASTKA_BEZ_DPH, CASTKA_S_DPH, TYP_DOKUMENTU'.split(', ')

dt = OrderedDict.fromkeys(['id', 'ds', 'ico', 'subjekt'] + els)
for j in dt:
    dt[j] = []

tf = tarfile.open('vstupy/smlouvy.tar.gz')

for ff in tf.getmembers():
    fn = os.path.split(ff.name)[-1].split('.')[0]
    if not fn.isdigit(): continue
    ds = idpub[fn]
    ico = str(int(dsico[ds])).rjust(8, '0') if ds in dsico else np.nan
    subj = dssubj[ds] if ds in dssubj else np.nan

    dt['id'].append(fn)
    dt['ds'].append(ds)
    dt['ico'].append(ico)
    dt['subjekt'].append(subj)


    da = json.loads(tf.extractfile(ff).read().decode('utf8'))

    for j,k in da.items():
        dt[j].append(k)


df = pd.DataFrame(dt)

df.sort_values(by='id').to_csv('vystupy/smlouvy.csv', index=None, encoding='utf8')
