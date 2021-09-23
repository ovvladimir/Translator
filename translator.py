# https://www.deepl.com/translator

import translators as ts
from tkinter import Tk, Frame, Label, Text, Scrollbar, Button, PhotoImage, END, W, E
import os

import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
from textblob import TextBlob
# import pycld2 as cld2

icon = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(icon, 'icon.png')


def close(_):
    root.destroy()


def clipboard():
    try:
        clip_text = root.clipboard_get()
    except BaseException:
        clip_text = "Buffer empty"
    if len(clip_text) < 4:
        clip_text = "Enter text more than two characters"
    text1.delete(1.0, END)
    text1.insert(END, clip_text)
    translate(clip_text)


def window():
    win_text = text1.get(1.0, END)
    if len(win_text) < 4:
        win_text = "Enter text more than two characters"
        text1.delete(1.0, END)
        text1.insert(END, win_text)
    translate(win_text)


def translate(get_text):
    languages_text = TextBlob(get_text)
    indetect = languages_text.detect_language()
    # _, _, details = cld2.detect(get_text)
    # indetect = details[0][1]

    if indetect != 'ru':
        langout = 'ru'
    else:
        langout = 'en'
    lab0['text'] = f'Translate bing {indetect}\u2194{langout}'
    lab1['text'] = indetect
    lab2['text'] = langout

    if len(get_text) > 20:
        # translators
        output = ts.google(get_text, to_language=langout, if_use_cn_host=True)
        # output = ts.bing(get_text, to_language=langout, if_use_cn_host=False)
    else:
        try:
            # textblob
            output = languages_text.translate(from_lang=indetect, to=langout)
        except BaseException:
            output = languages_text
    text2.delete(1.0, END)
    text2.insert(END, output)


root = Tk()
root.title('Translate')
root.iconphoto(True, PhotoImage(file=path))

lab0 = Label(root, font='"times new roman" 14 bold', fg='white', bg='blue')
lab0.grid(row=0, column=0, columnspan=2, sticky=W + E, pady=2)

f1 = Frame(root)
f1.grid(row=1, column=0)
text1 = Text(
    f1, font='arial 12', wrap="word", width=50, height=12, padx=10, pady=10)
text1.pack(side='left')
scroll1 = Scrollbar(f1, command=text1.yview)
scroll1.pack(side='right', fill='y')
text1['yscroll'] = scroll1.set
# text1.pack_propagate(False)
root.update()
x, y = text1.winfo_width(), text1.winfo_height()
lab1 = Label(text1, fg='blue', bg='white')
# lab1.pack(side='right', anchor='s')
lab1.place(x=x - 35, y=y - 35)

f2 = Frame(root)
f2.grid(row=1, column=1)
text2 = Text(
    f2, font='arial 12', wrap="word", width=50, height=12, bg='gray95', padx=10, pady=10)
text2.pack(side='left')
scroll2 = Scrollbar(f2)
scroll2.pack(side='right', fill='y')
scroll2.config(command=text2.yview)
text2.config(yscrollcommand=scroll2.set)
# text2.pack_propagate(False)
lab2 = Label(text2, fg='blue', bg='gray95')
# lab2.pack(side='right', anchor='s')
lab2.place(x=x - 35, y=y - 35)

bt1 = Button(root, text='Translate window', font='arial 12', fg='blue', command=window)
bt1.grid(row=2, column=0, sticky=W + E)
bt2 = Button(root, text='Translate clipboard', font='arial 12', fg='blue', command=clipboard)
bt2.grid(row=2, column=1, sticky=W + E)

root.bind("<Escape>", close)
root.mainloop()
