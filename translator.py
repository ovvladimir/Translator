# https://www.deepl.com/translator

import warnings
warnings.filterwarnings("ignore")
try:
    import os
    from textblob import TextBlob as detect
    # import translators as ts
    import apis as ts
    from tkinter import Tk, Label, LEFT, RIGHT, BOTTOM, TOP, Button, PhotoImage, END
    import tkinter.scrolledtext as scroll
except ImportError:
    pass

icon = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(icon, 'icon.png')

err = "Buffer empty!"


def clipboard():
    try:
        clip = root.clipboard_get()
    except BaseException:
        clip = err
    lab1.delete(1.0, END)
    lab1.insert(END, clip)
    return clip


def definition():
    languages_text = detect(clipboard())
    indetect = languages_text.detect_language()
    if indetect != 'ru':
        langout = 'ru'
    else:
        langout = 'en'
    lab0['text'] = f'Translate google {indetect}-{langout}'
    return langout


def translate():
    output = []
    output = ts.google(clipboard(), to_language=definition(), if_use_cn_host=True)
    lab2.delete(1.0, END)
    lab2.insert(END, output)


root = Tk()
root.title('Translate')
root.iconphoto(True, PhotoImage(file=path))
lab0 = Label(root, font='arial 11 bold', fg='white', bg='blue')
lab0.pack(side=TOP, fill='both', pady=4)
bt = Button(root, text='Translate', font='arial 12', fg='blue', bd=1, command=translate)
bt.pack(side=BOTTOM, fill='both')
lab1 = scroll.ScrolledText(
    root, width=50, height=12, font='arial 12', padx=10, pady=10, wrap="word")
lab1.pack(side=LEFT)
lab2 = scroll.ScrolledText(
    root, width=50, height=12, font='arial 12', padx=10, pady=10, bg='gray95', wrap="word")
lab2.pack(side=RIGHT)

root.mainloop()
