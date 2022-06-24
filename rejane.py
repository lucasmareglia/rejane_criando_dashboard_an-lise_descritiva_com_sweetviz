from speech_recognition import Microphone, Recognizer, UnknownValueError
import mysql.connector
import pyttsx3
import random
import pandas as pd
import sweetviz as sv

criatura = pyttsx3.init()
recog = Recognizer()
mic = Microphone()

def fala_criatura(fala):
    criatura.setProperty('rate', 195)
    criatura.say(fala)
    criatura.runAndWait()
    return()

while True:
    with mic:
        fala_criatura('diga a senha')
        audio1 = recog.listen(mic)
    try:
        recognizedsenha = recog.recognize_google(audio1, language='pt').lower()         
        if recognizedsenha in 'lucas':
            fala_criatura('acesso, liberado... Vamos começaar, luucas')            
            while True:
                with mic:
                    fala_criatura('')
                    audio = recog.listen(mic)
                try:
                    recognized = recog.recognize_google(audio, language='pt').lower()
                    print('você disse: ', recognized)
                    
# COMANDOS CONVERSA >>>>>>>>>>>>>>>>>>>>>
                    if recognized in 'olá''oi''oie''olá rejane''oi rejane''oie rejane':
                        conv1 = ['olá, luucas ? no que posso ajudar ?','posso lhe ajudar? Luucas?','olá, Luucas ? o que vamos fazer agora ?', 'olá, o que iremos fazer hoje, Luucas']
                        fala_criatura(random.choice(conv1))
                    elif recognized in 'analisar banco de dados''analise o banco de dados''analisar o banco de dados':
                        while True:
                            with mic:
                                fala_criatura('qual o banco de dados deseja?')
                                audio1 = recog.listen(mic)
                                try:
                                    banco_de_dados = recog.recognize_google(audio1, language='pt').lower()
                                    banco_de_dados = str(banco_de_dados)
                                except UnknownValueError:
                                    fala_criatura('não intendi, repita o banco de dados, por favor')
                                except RequestError:
                                    fala_criatura('não intendi, repita o banco de dados por favor')
                                fala_criatura('qual tabela quer analisar?')
                                audio1 = recog.listen(mic)
                                try:
                                    tabela = recog.recognize_google(audio1, language='pt').lower()
                                    tabela = str(tabela)
                                except UnknownValueError:
                                    fala_criatura('não intendi, repita a tabela, por favor')
                                except RequestError:
                                    fala_criatura('não intendi, repita a  tabela por favor')
                                    
                                fala_criatura('deseja comparar categorias?')
                                audio1 = recog.listen(mic)
                                try:
                                    resp = recog.recognize_google(audio1, language='pt').lower()
                                    resposta = str(resp)
                                except UnknownValueError:
                                    fala_criatura('não intendi, pode repetir por favor')
                                except RequestError:
                                    fala_criatura('não intendi, pode repetir por favor')
                                if resposta in 'sim''Sim''SIM':
                                    import unidecode
                                    fala_criatura('deseja comparar categorias em qual coluna?')
                                    audio1 = recog.listen(mic)
                                    try:
                                        coluna = recog.recognize_google(audio1, language='pt').lower()
                                        coluna = str(coluna)
                                    except UnknownValueError:
                                        fala_criatura('não intendi, repita a coluna, por favor')
                                    except RequestError:
                                        fala_criatura('não intendi, repita a  coluna, por favor')

                                    fala_criatura('qual a primeira categoria a ser comparada?')
                                    audio1 = recog.listen(mic)
                                    try:
                                        primeira = recog.recognize_google(audio1, language='pt').title()
                                        label1=str(primeira)
                                        primeira= unidecode.unidecode(primeira)
                                    except UnknownValueError:
                                        fala_criatura('não intendi, repita a primeira categoria, por favor')
                                    except RequestError:
                                        fala_criatura('não intendi, repita a  primeira categoria, por favor')

                                    fala_criatura('qual a segunda categoria a ser comparada?')
                                    audio1 = recog.listen(mic)
                                    try:
                                        segunda = recog.recognize_google(audio1, language='pt').title()
                                        label2=str(segunda)
                                        segunda= unidecode.unidecode(segunda)
                                    except UnknownValueError:
                                        fala_criatura('não intendi, repita a segunda categoria, por favor')
                                    except RequestError:
                                        fala_criatura('não intendi, repita a  segunda categoria, por favor')

                                    conec= mysql.connector.connect(host='localhost',database=f'{banco_de_dados}',user='root',password='lucas123')
                                    if conec.is_connected():
                                        fala_criatura(f'analisando banco de dados {banco_de_dados}')
                                        fala_criatura('isso pode demorar um minuto...')
                                        cursor=conec.cursor()
                                        cursor.execute(f'select * from {tabela};')
                                        r= cursor.fetchall()
                                        r = pd.DataFrame(r)
                                    if banco_de_dados in 'world':
                                        r=r.rename(columns={2:'continente',3:'região',4:'area m²',6:'população',7:'expectativa de vida',8:'gnp'})
                                        del r[0],r[1],r[5],r[9],r[10],r[11],r[12],r[13],r[14]
                                        compare1= r.loc[r[coluna]== primeira]
                                        tam1=len(compare1)
                                        compare2= r.loc[r[coluna]==segunda]
                                        tam2=len(compare2)
                                        report_conp = sv.compare([compare1,label1], [compare2,label2])
                                        report_conp.show_html(layout='widescreen',scale=0.7)
                                        
                                    elif banco_de_dados in 'clientes':
                                        coluna=coluna.lower()
                                        r=r.rename(columns={0:'nome',1:'idade',2:'cpf'})
                                        primeira = primeira.lower()
                                        compare1= r.loc[r[coluna]== primeira]
                                        tam1=len(compare1)
                                        segunda=segunda.lower()
                                        compare2= r.loc[r[coluna]==segunda]
                                        tam2=len(compare2)
                                        report_conp = sv.compare([compare1,label1], [compare2,label2])
                                        report_conp.show_html(layout='widescreen',scale=0.7)
                                    fala_criatura(f'temos um total de {tam1} registros relacionados a categoria {label1}, e temos um total de {tam2} registros relacionados a categoria {label2}')
                                    break
                                else:
                                    conec= mysql.connector.connect(host='localhost',database=f'{banco_de_dados}',user='root',password='lucas123')
                                    if conec.is_connected():
                                        fala_criatura(f'analisando banco de dados {banco_de_dados}')
                                        fala_criatura('isso pode demorar um minuto...')
                                        cursor=conec.cursor()
                                        cursor.execute(f'select * from {tabela};')
                                        r= cursor.fetchall()
                                        r = pd.DataFrame(r)
                                        tam=len(r)
                                    if banco_de_dados in 'world':
                                        r=r.rename(columns={2:'continente',3:'região',4:'area m²',6:'população',7:'expectativa de vida',8:'gnp'})
                                        del r[0],r[1],r[5],r[9],r[10],r[11],r[12],r[13],r[14]
                                        report_conp=sv.analyze([r,f'{banco_de_dados}'])
                                        report_conp.show_html(layout='widescreen',scale=0.7)
                                    elif banco_de_dados in 'clientes':
                                         r=r.rename(columns={0:'nome',1:'idade',2:'cpf'})
                                         report_conp=sv.analyze([r,f'{banco_de_dados}'])
                                         report_conp.show_html(layout='widescreen',scale=0.7)
                                    else:    
                                        report_conp=sv.analyze([r,f'banco_de_dados'])
                                        report_conp.show_html(layout='widescreen',scale=0.7)
                                        fala_criatura(f'sua análise da tabela {tabela} está pronta')
                                    fala_criatura(f'no banco de dados {banco_de_dados} temos um total de {tam} registros que foram analisados')
                                    break

                except UnknownValueError:
                    fala_criatura('')
        else:
            fala_criatura('senha incorreta, acesso negado!')
    except UnknownValueError:
        fala_criatura('não intendi, repita a senha por favor')
