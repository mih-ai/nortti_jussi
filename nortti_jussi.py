import tkinter
from tkinter import *
import openai
import pyperclip
import pygame
from charset_normalizer import md__mypyc
import PIL.Image, PIL.ImageTk
from PIL import ImageDraw
from PIL import ImageFont
import os
import numpy as np
import time
import threading

# Author: @experience-in-ai (https://stackoverflow.com/users/15519629/experience-in-ai)
# Email: manneha@oamk.fi
# Copyright 2023
#
# Tämä on vapaaseen käyttöön ja jatkojalostukseen tarkoitettu ohjelmanpätkä "nörtti-jussi", 
# liittyen OpenAI-tekoälyjärjestelmän sujuvaan käyttöön. Ohjelma on erityisesti tarkoitettu opiskelijoilleni. 
# 
# Käyttöehdot: ennen omalle tietokoneellennesi lataamista hymyile jollekulle lähellä olevalle.
# Tämän myötä saatte vapaan käyttöoikeuden ohjelmaan. Tietysti ohjelmaa saa käyttää vain asiallisiin hommiin. 
# Jos jatkojalostat koodia, on fiksua viitata alkuperäiseen koodiin sopivalla tavalla.
#
# Jos kohtaat ongelmia, kysymykset ovat tervetulleita stackoverflown kautta, jolloin vastaukset ovat 
# myös muiden helposti hyödynnettävissä, tai sähköpostitse.
#
# Toimiakseen ohjelma tarvitsee OpenAI:n API_KEY:n. Voit luoda sellaisen helposti itsellesi, ohjeet löydät googlettamalla. 
#
# -- ja sama kansainvälisesti:
#
# This piece of code is for free use everywhere; especially for my students. 
# Use it, have fun, develp further, and so on! 
# 
# Terms of use: before downloading that, smile once to someone near to you.
# This will grant you for-ever-type free usage of the code. The software is for 
# responsible use only, be fair and kind when using that.  
#
# If you modify or develop further the code, please refer to the author somehow in your code.  
#
# If you have probems in using or in installation - feel free to ask the 
# author for help (https://stackoverflow.com/users/15519629/experience-in-ai)
#
# To use this software you need own OpenAI API_KEY. You can easily generate one for you, google helps you how to do that. 
#
# OWN PERSONAL API-KEY HERE (below just an example somehow what it looks like...)
#
API_KEY='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'
#
# Mutta, säännöksistä johtuen pyydetään käyttäjältä aina API käyttöliittymän kautta. 
# Oma API kannattaa "kovakoodata" tänne, katso vihjeet asiasta koodin seasta

#Initialisointia...
pygame.mixer.init()

#Maaritellaan aanet...
kysymys_aani=pygame.mixer.Sound("manne_klik.wav")
vastaus_aani=pygame.mixer.Sound("manne_bling.wav")
tiedostotalletus_aani=pygame.mixer.Sound("manne_blong.wav")
leikepoyta_aani=pygame.mixer.Sound("manne_kamerasuljin.wav")
leikepoyta_aani.set_volume(0.5)

ikkuna=tkinter.Tk()
ikoni=PhotoImage(file='d.png')
ikkuna.iconphoto(True,ikoni)
ikkuna.title('Nörtti-Jussi Suomesta - - - (write a question on left, press "Öööh?" and wait for the anwer...all languages are welcome!)')

def paivita_kuva(kuvan_polku):
    opiskelijan_kuva=PIL.Image.open(kuvan_polku).resize([200,230],resample=0)
    temp_kuva=PIL.ImageTk.PhotoImage(opiskelijan_kuva)
    animaatio_label.configure(image=temp_kuva)
    animaatio_label.image=temp_kuva
    ikkuna.update()

def kysy():
    global API_KEY
    API_KEY2=apikoodi_kahva.get('1.0','end-1c')
    pygame.mixer.Sound.play(kysymys_aani)
    painike['bg']='gray80'
    painike['text']='...hmmm...krmh...'

    if np.random.randn()>0:
        paivita_kuva("pohdi4.png")
    else:
        paivita_kuva("pohdi5.png")
    
    openai.api_key=API_KEY
    model="text-davinci-003"
    prompt=kysymysteksti_kahva.get('1.0','end')
    print("Kysymyksen pituus oli: ",len(prompt))
    print("Valittu lämpötila on: ",liukukytkin.get())

    #Jatkokehittäjä: huomaa että alla olevia parametereja säätämällä voit tehdä edistyksellisempiä asioita...
    try:
        response= openai.Completion.create(
            prompt=prompt,
            model=model,
            max_tokens=2000,
            temperature=liukukytkin.get(),
        )
        vastaus=response.choices[0].text
        paivita_kuva("pohdi_vastaus.png")
    except:
        vastaus='Ei vastausta - Ernesti on kiireinen eli\nkahvitauolla,\nyritä parjäillä itseksesi! \n\nOn myös mahdollista että API-koodisi on väärä tai puuttuu, tarkista se!\n\n(If you did not understood, \nplease see translation for\nthis e.g. from google)'
        paivita_kuva("pohdi_kahvi.png")

    vastausteksti_kahva.delete(1.0,'end')
    vastausteksti_kahva.insert(1.0,vastaus)  
    pygame.mixer.Sound.play(kysymys_aani)
    painike['bg']='SeaGreen2'
    painike['text']='Öööh?'
    return vastaus

def kopioi_leikepoydalle():
    pyperclip.copy(vastausteksti_kahva.get('1.0','end'))
    pygame.mixer.Sound.play(leikepoyta_aani)
    print("Vastaus kopioitu leikepoydalle!")

def tallenna_py_tiedostona():
    global tiedostotalletus_aani
    try:
        with open('apukoodi.py', 'w') as file:
            file.write(vastausteksti_kahva.get('1.0','end'))
        print("Tallennettu!")
        pygame.mixer.Sound.play(tiedostotalletus_aani)
    except:
        print("Jokin virhe tapahtui!")
                   
kysymysteksti_kahva=tkinter.Text(ikkuna,height=14,width=40)
kysymysteksti_kahva.grid(row=0,column=0,pady=2,columnspan=1)

opiskelijan_kuva=PIL.Image.open("pohdi_valmiina.png").resize([200,230],resample=0)
temp_kuva=PIL.ImageTk.PhotoImage(opiskelijan_kuva)
animaatio_label=Label(ikkuna,image=temp_kuva)
animaatio_label.grid(row=0,column=1,padx=10)

painike=tkinter.Button(ikkuna,text='Öööh?',command=kysy)
painike.grid(row=1,column=0,pady=1,columnspan=1)
painike['bg']='SeaGreen2'

liukukytkin=tkinter.Scale(ikkuna,from_=0,to=1,resolution=0.1,orient=HORIZONTAL)
liukukytkin.set(0.5)
liukukytkin.grid(row=1,column=1,padx=10)

vasen_teksti=Label(ikkuna,text="Viileä...")
vasen_teksti.grid(row=1,column=1,sticky='W',padx=10)
oikea_teksti=Label(ikkuna,text="...Kuuma")
oikea_teksti.grid(row=1,column=1,sticky='E',padx=10)

vastausteksti_kahva=tkinter.Text(ikkuna,height=14,width=40)
vastausteksti_kahva.grid(row=0,column=2,pady=2,columnspan=1)

apikoodi_kahva=tkinter.Text(ikkuna,height=1,width=5)
apikoodi_kahva.grid(row=2,column=1,pady=2,columnspan=1)

api_ohje_teksti=Label(ikkuna,text="API:")
api_ohje_teksti.grid(row=2,column=1,sticky='W',padx=5)

kopioi_leikepoydalle_painike=tkinter.Button(ikkuna,text='Leikepöydälle',command=kopioi_leikepoydalle)
kopioi_leikepoydalle_painike.grid(row=1,column=2,pady=2,sticky='W',padx=10)

tallenna_tiedostona_painike=tkinter.Button(ikkuna,text='.py -tiedostoksi',command=tallenna_py_tiedostona)
tallenna_tiedostona_painike.grid(row=1,column=2,pady=2,sticky='E',padx=10)

ikkuna.mainloop()