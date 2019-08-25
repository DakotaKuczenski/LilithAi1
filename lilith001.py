from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser 
import smtplib 
import requests
import sys
from os import rename
from glob import iglob
from os.path import join, expanduser, isfile, basename, splitext


def talkToMe(audio):
    
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)


def myCommand():

    k = sr.Recognizer()
    with sr.Microphone() as source:
        print('Ready...')
        k.pause_threshold = 1
        k.adjust_for_ambient_noise(source, duration=1)
        audio = k.listen(source)
    try:
        command = k.recognize_google(audio).lower()
        print('I heard: ' + command + '\n')

    #loop back to continue to listen for commands
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command


def initializer_Command(command):
    pass


def assistant(command):

    # this was a poor choice for a name, as you may soon to find out. 
    if 'lilith' in command:

        if 'open reddit' in command:
            regex = re.search('open reddit (.*)', command) # looks for a sub command
            url = 'https://www.reddit.com/'
            if regex:
                sub = regex.group(1)
                url = url + 'r/' + sub
            webbrowser.open(url)

        elif 'search google for' in command:
            regex = re.search('search google for (.*)', command)
            if regex:
                search = regex.group(1)
                url = "https://www.google.com.tr/search?q={}".format(search)
                webbrowser.open_new_tab(url)


        #may add spotify. 


        elif 'email' in command:
            talkToMe('Who is the this to?')
            email = myCommand()

            talkToMe('What is the subject')
            subject = myCommand()

            talkToMe('What should I say?')
            content = myCommand()

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

                smtp.login('dkuczenski12@gmail.com', 'xvikcxcslizxfsla')
                msg = f'Subject: {subject}\n\n{content}'
                smtp.sendmail('dkuczenski12@gmail.com', {email} , msg)
                smtp.close()

                talkToMe('Email sent.')


        elif 'open the website' in command:
            regex = re.search('open the website (.+)', command)
            if regex:
                domain = regex.group(1)
                url = 'https://www.' + domain
                webbrowser.open(url)
            else:
                pass


        elif 'sort my downloads' in command:

            #dictionary for the types of files. 
            file_types = {
                'Pictures': ['.gif', '.jpeg', '.jpg', '.png'],

                'Videos': ['.m4v', '.mov', '.mp4', '.mpg', '.mpeg'],

                'Documents': ['.doc', '.docx', '.odt', '.pdf', '.rtf', '.tex', '.txt','.wks', '.wps', '.wpd', '.ods', '.key','.csv', '.dat', '.db', '.dbf', '.log', '.mdb','.sav', '.sql', '.xml'],

                'programs': ['.apk', '.bat', '.bin', '.cgi', '.pl', '.com', '.exe', '.jar', '.py', '.wsf']
            }
            for f in iglob(join(expanduser('~/Downloads'), '*.*')):  #grab the files in downloads
                for key in file_types:
                    if splitext(f)[1] in file_types[key]:
                        rename(f, join(expanduser('~'), key, basename(f)))
                        print(f'{basename(f)} was moved to {key}.')
                if isfile(f): # if not moved print
                    print(f'Unknown where to move: {basename(f)}')


        elif 'turn off' in command:
            sys.exit()


talkToMe('Active')

while True:
    assistant(myCommand())
