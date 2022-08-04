global nome, link

# Importando módulos
from tkinter import *
import json
import datetime
import speech_recognition as sr
import sounddevice as sd
import wavio as wv
import wikipedia
import webbrowser
import random
from gtts import gTTS
from playsound import playsound
import pywhatkit
import bs4
import requests
import joblib
import os
import requests

with open("dados2.json") as jsonFile:
    dados = json.load(jsonFile)
nick = dados['name']
idade = dados['age']
local = dados['local']


# Função de fala

def fala(text):
    global file1
    for i in range(0, 3):
        tts = gTTS(text, lang='pt')
        file1 = str("testandoaudio" + str(i) + ".mp3")
        tts.save(file1)
    playsound(file1, True)
    os.remove(file1)

def iaon():
    # Listas
    denada = ['De nada', 'Por nada', 'A seu dispor!', 'Até logo!']
    denada = random.choice(denada)


    sitespadrao = [['whatsapp', 'https://web.whatsapp.com/'], ['youtube', 'https://youtube.com/'],
                   ['instagram', 'https://www.instagram.com/']]

    # Importando arquivos de voz
    filename = "minhavoz.wav"
    falaia = "falaia.mp3"

    # Declarar globalmente a variável
    global says


    def addsite():
        snome = input('Qual o nome do site? ')
        slink = input('Qual o link do site? ')
        listabase = [snome, slink]
        sitespadrao.append(listabase)

    # Função de gravar áudio para reconhecimento.
    def grava():
        freq = 48000  # Altere a frequência se achar necessário
        duration = 5  # Altere a duração de cada gravação
        recording = sd.rec(int(duration * freq),
                           samplerate=freq, channels=2)
        print('Fale agora!')
        sd.wait()
        wv.write("minhavoz.wav", recording, freq, sampwidth=2)
        print('Ok! Processando')

    # Função de pegar informações sobre ativos
    def get_crypto_price(coin):
        url = "https://www.google.com/search?q=" + coin + "+hoje"
        HTML = requests.get(url)
        soup = bs4.BeautifulSoup(HTML.text, 'html.parser')
        text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        fala(f'O preço de {coin} é de {text}')

    while True:
        grava()

        # Iniciando o reconhecimento de fala
        r = sr.Recognizer()

        try:
            with sr.AudioFile(filename) as source:
                # "Escutando" o arquivo
                audio_data = r.record(source)
                # Convertendo de audio para texto
                says = r.recognize_google(audio_data, language='pt-BR')
                # Escrevendo o que foi dito.

                print('Você disse: ' + says.lower())
                texto = says.lower()

                # Desligar
                f = open('shutdown.txt', 'r')
                fec = f.read()
                if texto in fec:
                    fala('Ok! Desligando')
                    janela.destroy()
                    break

                # Horas
                elif 'horas' in texto or 'hora' in texto:
                    hora = datetime.datetime.now().strftime('%H:%M')
                    fala('Agora são' + hora)
                    return

                # Pesquisas
                elif 'procure por' in texto:
                    procurar = texto.replace('procure por', '')
                    wikipedia.set_lang('pt')
                    resultado = wikipedia.summary(procurar, 2)
                    fala(resultado)
                    return

                # Tocar músicas
                elif 'toque' in texto or 'tocar' in texto:
                    tocar = texto.replace('toque', '')
                    fala(f'Ok, tocando música!')
                    resultado = pywhatkit.playonyt(tocar)
                    return

                # Abrir sites
                elif 'abrir site' in texto:
                    site = texto.replace('abrir site', '')
                    mysites = joblib.load('sitesadd.obj')
                    for i in mysites:
                        if i[0] in site:
                            webbrowser.open(i[1])
                    return

                elif 'adicionar site' in texto:
                    addsite()
                    joblib.dump(sitespadrao, 'sitesadd.obj')
                    return

                # Valor criptomoedas
                elif 'valor hoje' in texto:
                    coin = texto.replace('valor hoje', '')
                    get_crypto_price(coin)
                    return

                if 'jogue uma moeda' in texto:
                    moeda = ['cara', 'coroa']
                    fala(random.choice(moeda))
                    return

                # Respostas simples
                elif 'bom dia' in texto:
                    fala(f'Bom dia {nick}')
                    return
                elif 'boa tarde' in texto:
                    fala(f'Boa tarde {nick}')
                    return
                elif 'boa noite' in texto:
                    fala(f'Boa noite {nick}')
                    return
                elif 'idade' in texto:
                    fala(f'Você tem {idade} anos')
                    return
                elif 'moro' in texto:
                    fala(f'Você mora no {local}')
                    return

        # Se ocorrer algum erro, retornará:
        except Exception as e:
            print('Ocorreu algum erro.')
            print('Erro:')
            print(e)
            return


janela = Tk()
janela.title('Assistente Virtual de Diego - Dev')

label2_l = Label(janela, text='Feito por Diego Rodrigues "Sawyer" | Estudante da C.E.S.A.R School', font='Calibri 10', )
label2_l.place(x=0, y=0)

label_l = Label(janela, text='Assistente Virtual', font='Arial 35', )
label_l.place(x=235, y=200)

botao_l = Button(janela, height=4, width=67, text='Clique aqui para iniciar!', command=iaon, background='orange')
botao_l.place(x=185, y=270)

janela.geometry('890x500+0+0')

janela.mainloop()