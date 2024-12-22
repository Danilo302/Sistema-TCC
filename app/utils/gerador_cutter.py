import json
import unicodedata

with open("app/utils/cutter.json", encoding='utf-8') as cutter:
    codCutter = json.load(cutter)


def geradorCutter(sobrenome,titulo):
    sobrenomeUse = sobrenome
    sobrenomeUse = remove_acentos(sobrenomeUse)
    sobrenomeUse = sobrenomeUse.split()
    sobrenomeUse = sobrenomeUse[0]
    
    nomesCutter = list(codCutter.keys())
    
    nomesCutter.append(sobrenomeUse)
    nomesCutter.sort()
    
    nomeProximo = ''
    
    for i in range(len(nomesCutter)):
        if nomesCutter[i] == sobrenomeUse:
            nomeProximo = nomesCutter[i-1]
            
    tituloUse = titulo
    tituloUse = remove_acentos(tituloUse)

    artigos = ["O", "A", "Os", "As", "Um", "Uma", "Uns", "Umas"]
    palavras = tituloUse.split()

    for palavra in palavras:
        if palavra.title() not in artigos:
            tituloUse = palavra[0]

            
    codigo = f'{sobrenomeUse[0].upper()}{codCutter[nomeProximo]}{tituloUse}'
    return codigo

def remove_acentos(texto):
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])