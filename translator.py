# https://www.deepl.com/translator
# https://habr.com/ru/post/517972/

import warnings
warnings.filterwarnings("ignore")
try:
    import os
    from textblob import TextBlob as detect
    import translators as ts
    # import apis as ts
    from tkinter import Tk, Label, Button, PhotoImage, END, W, E
    import tkinter.scrolledtext as scroll
except ImportError:
    pass

icon = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(icon, 'icon.png')


def clipboard():
    try:
        clip_text = root.clipboard_get()
    except BaseException:
        clip_text = "Buffer empty"
    lab1.delete(1.0, END)
    lab1.insert(END, clip_text)
    translate(clip_text)


def window():
    win_text = lab1.get(1.0, END)
    if len(win_text) < 4:
        win_text = "Enter text more than two characters"
        lab1.delete(1.0, END)
        lab1.insert(END, win_text)
    translate(win_text)


def translate(get_text):
    languages_text = detect(get_text)
    indetect = languages_text.detect_language()
    if indetect != 'ru':
        langout = 'ru'
    else:
        langout = 'en'
    lab0['text'] = f'Translate google {indetect}-{langout}'

    output = ts.google(get_text, to_language=langout, if_use_cn_host=True)
    lab2.delete(1.0, END)
    lab2.insert(END, output)


root = Tk()
root.title('Translate')
root.iconphoto(True, PhotoImage(file=path))
lab0 = Label(root, font='arial 11 bold', fg='white', bg='blue')
lab0.grid(row=0, column=0, columnspan=2, sticky=W + E, pady=4)
lab1 = scroll.ScrolledText(
    root, width=50, height=12, font='arial 12', padx=10, pady=10, wrap="word")
lab1.grid(row=1, column=0)
lab2 = scroll.ScrolledText(
    root, width=50, height=12, font='arial 12', padx=10, pady=10, bg='gray95', wrap="word")
lab2.grid(row=1, column=1)
bt1 = Button(root, text='Translate window', font='arial 12', fg='blue', command=window)
bt1.grid(row=2, column=0, sticky=W + E)
bt2 = Button(root, text='Translate clipboard', font='arial 12', fg='blue', command=clipboard)
bt2.grid(row=2, column=1, sticky=W + E)

root.mainloop()
