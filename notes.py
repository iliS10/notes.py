import tkinter as tk
from tkinter import filedialog, Text, END
import os
from pygments import lex
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.styles import get_style_by_name

root = tk.Tk()
root.title("Bloc-Notes Personnalisé")

# Création de la marge
marge = tk.Listbox(root)
marge.grid(row=0, column=0, sticky="ns")

# Définition de la police et de la taille de la police
font_name = "CustomFont"
font_size = 16

# Création d'une zone de texte
text_area = tk.Text(root, font=(font_name, font_size), undo=True)
text_area.grid(row=0, column=1, sticky="nsew")
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Création d'une barre de menu
menu = tk.Menu(root)
root.config(menu=menu)

# Stocke le chemin du fichier actuel
file_path = ''
code_mode = False

def open_file(path=None):
    global file_path
    if path is None:
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    else:
        file_path = path
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text_area.delete('1.0', END)
            text_area.insert('1.0', file.read())
        update_marge()
        if code_mode:
            color_code()

def save_file(event=None):
    global file_path
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[("All Files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get('1.0', END))
        update_marge()

def save_file_as(event=None):
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[("All Files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get('1.0', END))
        update_marge()

def create_new():
    global file_path
    file_path = ''
    text_area.delete('1.0', END)
    update_marge()

def open_directory():
    global file_path
    directory = filedialog.askdirectory()
    if directory:
        file_path = os.path.join(directory, '')  # Add trailing slash
        update_marge()

def update_marge():
    marge.delete(0, tk.END)
    if file_path:
        directory = os.path.dirname(file_path)
        for file in os.listdir(directory):
            marge.insert(tk.END, file)

def on_file_select(event):
    file = marge.get(marge.curselection())
    if file_path:
        directory = os.path.dirname(file_path)
        file = os.path.join(directory, file)
        open_file(file)

marge.bind('<<ListboxSelect>>', on_file_select)

# Ajout de commandes à la barre de menu
file_menu = tk.Menu(menu)
menu.add_cascade(label="Fichier", menu=file_menu)
file_menu.add_command(label="Nouveau", command=create_new)
file_menu.add_command(label="Ouvrir...", command=open_file)
file_menu.add_command(label="Ouvrir un dossier...", command=open_directory)
file_menu.add_command(label="Sauvegarder", command=save_file, accelerator='Ctrl+S')
file_menu.add_command(label="Sauvegarder sous...", command=save_file_as, accelerator='Ctrl+Shift+S')
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=root.quit)

def toggle_marge():
    if marge.winfo_viewable():
        marge.grid()
    else:
        marge.grid_remove()

# Fonctions pour zoomer et dézoomer
def increase_font(event=None):
    global font_size
    font_size += 2
    text_area.config(font=(font_name, font_size))

def decrease_font(event=None):
    global font_size
    font_size -= 2
    text_area.config(font=(font_name, font_size))

root.bind("<Control-plus>", increase_font)
root.bind("<Control-minus>", decrease_font)
root.bind("<Control-s>", save_file)
root.bind("<Control-S>", save_file_as)

view_menu = tk.Menu(menu)
menu.add_cascade(label="Vue", menu=view_menu)
view_menu.add_command(label="Afficher/Enlever marge", command=toggle_marge)
view_menu.add_command(label="Zoom + (Ctrl+Plus)", command=increase_font)
view_menu.add_command(label="Zoom - (Ctrl+Minus)", command=decrease_font)

def toggle_code_mode():
    global code_mode
    code_mode = not code_mode
    if code_mode:
        color_code()
    else:
        text_area.config(fg="black")  # Réinitialise la couleur du texte en noir

view_menu.add_command(label="Mode code", command=toggle_code_mode)

# Fonction de coloration syntaxique
def color_code():
    text = text_area.get('1.0', 'end')
    lexer = guess_lexer(text)
    style = get_style_by_name('default')

    text_area.tag_configure("Token", foreground="black")
    for token, content in lex(text, lexer):
        start = '{}.{}'.format(*content[0])
        end = '{}.{}'.format(*content[1])
        color = "#000000"  # Couleur par défaut

        if token in style:
            prop = style[token]
            if prop['color']:
                color = '#' + prop['color']

        text_area.tag_configure(str(token), foreground=color)
        text_area.tag_add(str(token), start, end)

root.mainloop()
