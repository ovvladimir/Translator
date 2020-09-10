# https://www.deepl.com/translator
# https://habr.com/ru/post/517972/

import warnings
warnings.filterwarnings("ignore")
try:
    import os
    from textblob import TextBlob as detect
    import translators as ts
    # import apis as ts
    from tkinter import Tk, Label, Text, Button, PhotoImage, END, W, E, S, RIGHT, Scrollbar
except ImportError:
    pass

icon = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(icon, 'icon.png')


def clipboard():
    try:
        clip_text = root.clipboard_get()
    except BaseException:
        clip_text = "Buffer empty"
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
    languages_text = detect(get_text)
    indetect = languages_text.detect_language()
    if indetect != 'ru':
        langout = 'ru'
    else:
        langout = 'en'
    lab0['text'] = f'Translate google {indetect}-{langout}'
    lab1['text'] = indetect
    lab2['text'] = langout

    output = ts.google(get_text, to_language=langout, if_use_cn_host=True)
    text2.delete(1.0, END)
    text2.insert(END, output)


root = Tk()
root.title('Translate')
root.iconphoto(True, PhotoImage(file=path))

lab0 = Label(root, font='arial 11 bold', fg='white', bg='blue')
lab0.grid(row=0, column=0, columnspan=2, sticky=W + E)

text1 = Text(
    root, width=50, height=12, font='arial 12', wrap="word")
text1.grid(row=1, column=0)
scroll1 = Scrollbar(text1, command=text1.yview)
scroll1.pack(side='right', fill='y')
text1['yscroll'] = scroll1.set

text2 = Text(
    root, width=50, height=12, font='arial 12', bg='gray95', wrap='word')
text2.grid(row=1, column=1)
scroll2 = Scrollbar(text2)
scroll2.pack(side='right', fill='y')
scroll2.config(command=text2.yview)
text2.config(yscrollcommand=scroll2.set)

bt1 = Button(root, text='Translate window', font='arial 12', fg='blue', command=window)
bt1.grid(row=2, column=0, sticky=W + E)
bt2 = Button(root, text='Translate clipboard', font='arial 12', fg='blue', command=clipboard)
bt2.grid(row=2, column=1, sticky=W + E)

text1.pack_propagate(False)
text2.pack_propagate(False)
lab1 = Label(text1, fg='blue', bg='white')
lab1.pack(side=RIGHT, anchor=S)
lab2 = Label(text2, fg='blue', bg='gray95')
lab2.pack(side=RIGHT, anchor=S)

root.mainloop()
