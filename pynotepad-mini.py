#!/usr/bin/python3

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from re import search
import os
import webbrowser
"""__________________________________________________"""
scheme_colors = {
    "dark": {
        'text_bg': '#282c34',
        'text_fg': '#abb2df',
        'cursor': '#528bff',
        'select_bg': '#7e8491'
    },

    "light": {
        'text_bg': '#fff',
        'text_fg': '#000',
        'cursor': '#8000ff',
        'select_bg': '#3399ff'
    }
}

CURRENT_FILE = False


def _clear_work_space():
    text.delete('1.0', END)
    root.title('New File')

def _open_file():
    file_path = filedialog.askopenfilename(title='Open File', filetypes=(
        ('Text documents (*.txt)', '*.txt'), ('All documents', '*.*')))
    if file_path:
        global CURRENT_FILE
        CURRENT_FILE = file_path
        FILE = open(file_path, encoding='utf-8', mode='r')
        text.delete('1.0', END)
        text.insert('1.0', FILE.read())
        FILE.close()
        root.title(os.path.basename(file_path))

def _save_changes(next_step):
    answer = messagebox.askyesnocancel('Save Changes', 'Unsaved changes will be lost!\n\nSave file?')
    if answer:
        save_as_file()
        next_step()
    elif answer == False:
        next_step()
    else:
        return


def exit_program():
    answer_exit = messagebox.askokcancel(title='Closing', message='Close Program?')
    if answer_exit:
        root.destroy()


def open_file():
    if text.get('1.0', END).strip():
        _save_changes(_open_file)
    else:
        _open_file()


def save_as_file():
    file_path = filedialog.asksaveasfilename(title='Save As File', filetypes=(('Text documents (*.txt)', '*.txt'), (
        'All documents', '*.*')))
    if file_path:
        if not re.search('.txt+$', file_path, flags=re.IGNORECASE):
            file_path += '.txt'
        global CURRENT_FILE
        CURRENT_FILE = file_path
        FILE = open(file_path, encoding='utf-8', mode="w")
        TEXT = text.get('1.0', END)
        FILE.write(TEXT)
        FILE.close()
        root.title(os.path.basename(file_path))


def save_file():
    global CURRENT_FILE
    if CURRENT_FILE:
        FILE = open(CURRENT_FILE, encoding='utf-8', mode='w')
        TEXT = text.get('1.0', END)
        FILE.write(TEXT)
        FILE.close()
    else:
        save_as_file()


def close_file():
    _save_changes(_clear_work_space)


def on_closing():
    if messagebox.askyesno("Quit", "Do you want to quit?"):
        root.destroy()

def switch_scheme(schm, txt):
    txt['bg'] = scheme_colors[schm]['text_bg']
    txt['fg'] = scheme_colors[schm]['text_fg']
    txt['insertbackground'] = scheme_colors[schm]['cursor']
    txt['selectbackground'] = scheme_colors[schm]['select_bg']

# open web-browser whith url
def callback(url):
    webbrowser.open_new(url)

def show_modal_about():
    top = Toplevel(root)

    if os.name == 'nt':
        ico_path = 'resources' + os.sep + os.sep + 'py.ico'
        if os.path.isfile(ico_path):
            top.iconbitmap(ico_path)

    top.title("About")
    top.geometry('+250+250')
    top.resizable(False, False)

    frm_top = Frame(top)
    frm_top.pack(padx=5, pady=10)
    frm_btm = Frame(top)
    frm_btm.pack(padx=5)

    Label(frm_top, font="10", text="Created by:", fg="black").grid(row=0, column=0, sticky=W)
    Label(frm_top, font="10", text="Denis Pirogov (EPluribusNEO)", fg="black").grid(row=0, column=1, sticky=W)

    Label(frm_top, font="10", text="Get source code:", fg="black").grid(row=1, column=0, sticky=W)
    link1 = Label(frm_top, font="10", text="GitHub", fg="blue", cursor="hand2")
    link1.grid(row=1, column=1, sticky=W)
    link1.bind("<Button-1>", lambda e: callback("https://github.com/EpluribusNEO/py-notepad-mini"))

    Label(frm_top, font="10", text="License:", fg="black").grid(row=2, column=0, sticky=W)
    link_license = Label(frm_top, font="10", text="Apache Version 2.0", fg="blue", cursor="hand2")
    link_license.grid(row=2, column=1, sticky=W)
    link_license.bind("<Button-1>", lambda e: callback("https://apache.org/licenses/LICENSE-2.0.html"))

    Label(frm_top, font="10", text="Personal web page:", fg="black").grid(row=3, column=0, sticky=W)
    link2 = Label(frm_top, font="10", text="Visit web page", fg="blue", cursor="hand2")
    link2.grid(row=3, column=1, sticky=W)
    link2.bind("<Button-1>", lambda e: callback("https://ds-portfolio.netlify.app/"))


    btn_cloce = ttk.Button(frm_btm, text='Close', command=lambda: top.destroy())
    btn_cloce.pack(side=BOTTOM)

    top.transient(root)
    top.grab_set()
    top.focus_set()
    top.wait_window()


root = Tk()
root.title('PyNotepad-mini')
root.geometry('840x620+50+50')
root.resizable(True, True)

if os.name == 'nt':
    ico_path = 'resources' + os.sep + os.sep + 'py.ico'
    if os.path.isfile(ico_path):
        root.iconbitmap(ico_path)

main_menu = Menu(root)
root.config(menu=main_menu)

""". . . . . . . . . .FILE. . . . . . . . . ."""
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label='Save As', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label='Close File', command=close_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exit_program)
main_menu.add_cascade(label='File', menu=file_menu)
""". . . . . . . . . ./FILE. . . . . . . . . ."""

""". . . . . . . . . .View. . . . . . . . . ."""
view_menu = Menu(main_menu, tearoff=0)
view_menu_scheme = Menu(view_menu, tearoff=False)
view_menu_scheme.add_command(label='Dark', command=lambda: switch_scheme('dark', text))
view_menu_scheme.add_separator()
view_menu_scheme.add_command(label='Light', command=lambda: switch_scheme('light', text))
view_menu.add_cascade(label='Scheme', menu=view_menu_scheme)
main_menu.add_cascade(label='View', menu=view_menu)
""". . . . . . . . . ./View. . . . . . . . . ."""

""". . . . . . . . . .Info. . . . . . . . . ."""
info_menu = Menu(main_menu, tearoff=0)
info_menu_sub = Menu(info_menu, tearoff=0)
info_menu.add_command(label='About', command=lambda: show_modal_about())
main_menu.add_cascade(label='Info', menu=info_menu)
""". . . . . . . . . ./Info. . . . . . . . . ."""

f_text = Frame(root)
f_text.pack(fill=BOTH, expand=True)

text = Text(f_text, bg=scheme_colors['dark']['text_bg'], fg=scheme_colors['dark']['text_fg'], padx=0, pady=0,
            wrap=WORD, insertbackground=scheme_colors['dark']['cursor'],
            selectbackground=scheme_colors['dark']['select_bg'],
            width=30, spacing3=1,
            font=('Courier New', 14))
text.pack(fill=BOTH, expand=True, side=LEFT)

scroll = Scrollbar(f_text, command=text.yview)
scroll.pack(fill=Y, side=LEFT)
text.config(yscrollcommand=scroll.set)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()