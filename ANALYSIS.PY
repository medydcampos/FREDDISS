####### Código Piloto: testando a extração de dados de arquivos jurídicos PDF
##### Autor do projeto: Frederico Gomes
##### Assistente de pesquisa: Maria Luiza Campos
###### Data: Junho 2025


#### Importanto bibliotecas

import fitz ## importando o pymupdf para leitura de arquivo PDF.
import re  ##  procurar, validar, extrair ou substituir padrões de texto de maneira avançada.   
import os  ##  manipular arquivos e diretórios.
import pandas as pd ##  manipular dados em formato de tabelas.

## Vamos criar uma função de extração de texto de um arquivo PDF

def extrair_info_acordao(texto):
    return {
        "idade_vitima": "; ".join(re.findall(r"(?:v[ií]tima|menor)[^.\n]{0,30}?(\d{1,2})\s*(?:anos|anos de idade)", texto, re.IGNORECASE)),
        "idade_reu": "; ".join(re.findall(r"(?:r[eé]u|acusado)[^.\n]{0,30}?(\d{1,2})\s*(?:anos|anos de idade)", texto, re.IGNORECASE)),
        "vinculo_familiar": bool(re.search(r"(pai|m[ãa]e|tio|tia|primo|prima|irm[ãa]o|familiar|enteado|companheiro|esposo|esposa)", texto, re.IGNORECASE)),
        "coabitacao": bool(re.search(r"(resid[ií]a|morava|convivia|habitava)[^.\n]{0,30}?(juntos|com o acusado|na mesma casa|sob o mesmo teto)", texto, re.IGNORECASE)),
        "consentimento": bool(re.search(r"(consentimento|concord[oua]|permit[iu])[^\n.]{0,50}?(v[ií]tima|famil[ií]a|pais)", texto, re.IGNORECASE))
    }

def processar_pdfs_em_diretorio(diretorio):
    dados = []

    for nome_arquivo in os.listdir(diretorio):
        if nome_arquivo.endswith(".pdf"):
            caminho = os.path.join(diretorio, nome_arquivo)
            doc = fitz.open(caminho)
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
            doc.close()

            info = extrair_info_acordao(texto)
            info["arquivo"] = nome_arquivo
            dados.append(info)

    df = pd.DataFrame(dados)
    df.to_csv("dados_extraidos_acordaos.csv", index=False, encoding='utf-8-sig')
    print("✅ Arquivo CSV gerado com sucesso: dados_extraidos_acordaos.csv")

#Chamada principal para o caminho:

processar_pdfs_em_diretorio("/Users/malucampos/Documents/FREDISS")