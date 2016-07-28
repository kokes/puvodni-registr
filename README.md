Data z Portálu veřejné správy. Pár základních informací:

- predatuje současný [Registr smluv](http://smlouvy.gov.cz)
- obsahuje 50 tisíc smluv za dohromady 100 miliard
- kontraktorů je cca 12 tisíc, máte tu i informace z Registru ekonomických subjektů (den vzniku/zániku, NACE, ESA kód, ...)
- vkladatelé (objednatelé) bohužel nejsou plně identifikování - důvod je ten, že sice je u vkladatelů uvedena datová schránka, ale nepodařilo se mi ji namapovat na IČ u všech zadavatelů. A to zejména protože vkládaly odbory v rámci zadavatelů - a ty mají svoje vlastní DS. Veřejná databáze DS, zdá se, obsahuje pouze DS veřejných subjektů jako celků. Kdyby to uměl někdo napravit, dejte mi vědět.
- data jsou poskytovaná "as is", není tam žádná deduplikace, čištění IČ, nic
- kdybyste si data chtěli stahovat sami, následujte skripty tady a adaptujte si je dle potřeby - já původní XML neskladoval, protože součástí těch souborů byly i přílohy, takže to šlo do desítek gigabajtů
- všechny smlouvy jsou ve [vystupy/smlouvy.csv](vystupy/smlouvy.csv), původní XML konvertované do JSONu je ve [vstupy](vstupy)