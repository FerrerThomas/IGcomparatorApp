import json
import webbrowser
import tkinter as tk
import os
from bs4 import BeautifulSoup
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.title("Comparador de Seguidores en Instagram")
root.geometry("600x600")

# Hacer que la ventana esté centrada
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

from PIL import Image, ImageTk
import tkinter as tk
import os
# Obtén la ruta absoluta del archivo logo.png
logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
# Luego carga la imagen
image = Image.open(logo_path)
image_resized = image.resize((80, 80))  # Ajusta el tamaño según prefieras
logo = ImageTk.PhotoImage(image_resized)

# Crear el label del logo y colocarlo a la izquierda del botón "Comparar Listas"
label_logo = tk.Label(root, image=logo, bg="#F0F0F0")
label_logo.grid(row=2, column=1, padx=10, pady=10, sticky="e")

# Variables para almacenar los datos
seguidores = []
seguidos = []

# Función para cargar la lista de seguidores en HTML
def cargar_seguidores_html():
    global seguidores
    archivo_seguidores = filedialog.askopenfilename(title="Selecciona el archivo de seguidores (HTML)")
    if archivo_seguidores:
        try:
            with open(archivo_seguidores, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                seguidores = [a['href'].split('/')[-1] for a in soup.find_all('a', href=True)]
            messagebox.showinfo("Archivo de Seguidores", f"{len(seguidores)} seguidores cargados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

# Función para cargar la lista de seguidos en HTML
def cargar_seguidos_html():
    global seguidos
    archivo_seguidos = filedialog.askopenfilename(title="Selecciona el archivo de seguidos (HTML)")
    if archivo_seguidos:
        try:
            with open(archivo_seguidos, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                seguidos = [a['href'].split('/')[-1] for a in soup.find_all('a', href=True)]
            messagebox.showinfo("Archivo de Seguidos", f"{len(seguidos)} seguidos cargados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            
def cargar_seguidores_json():
    global seguidores
    archivo_seguidores = filedialog.askopenfilename(title="Selecciona el archivo de seguidores (JSON)")
    if archivo_seguidores:
        try:
            with open(archivo_seguidores, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Aquí usamos una lista para iterar sobre cada elemento del JSON
                seguidores = [
                    item['string_list_data'][0]['value']  # Extraemos el valor del nombre de usuario
                    for item in data if 'string_list_data' in item and item['string_list_data']
                ]
            messagebox.showinfo("Archivo de Seguidores", f"{len(seguidores)} seguidores cargados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")



# Función para cargar la lista de seguidos en JSON
def cargar_seguidos_json():
    global seguidos
    archivo_seguidos = filedialog.askopenfilename(title="Selecciona el archivo de seguidos (JSON)")
    if archivo_seguidos:
        try:
            with open(archivo_seguidos, 'r', encoding='utf-8') as file:
                data = json.load(file)
                seguidos = [
                    item['string_list_data'][0]['value'] 
                    for item in data.get("relationships_following", [])
                ]
            messagebox.showinfo("Archivo de Seguidos", f"{len(seguidos)} seguidos cargados.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

# Función de comparación
def comparar_listas():
    if not seguidores or not seguidos:
        messagebox.showwarning("Advertencia", "Por favor, carga ambas listas antes de comparar.")
        return
    no_te_siguen = sorted([usuario for usuario in seguidos if usuario not in seguidores])
    # Limpiar el área de texto
    resultado_texto.delete("1.0", tk.END)
    if no_te_siguen:
        resultado_texto.insert(tk.END, "Usuarios que sigues y no te siguen de vuelta:\n", "header")  
        # Añadir cada usuario con enlace
        for usuario in no_te_siguen:
            enlace = f"https://www.instagram.com/{usuario}"
            resultado_texto.insert(tk.END, f"{usuario} | ({enlace})\n", usuario)
            # Añadir un enlace clicable usando el tag
            resultado_texto.tag_config(usuario, foreground="blue", underline=True)
            resultado_texto.tag_bind(usuario, "<Button-1>", lambda e, url=enlace: webbrowser.open(url))
    else:
        resultado_texto.insert(tk.END, "¡Todos los usuarios te siguen de vuelta!")


# Reemplazar los botones estándar por botones de ttk para una apariencia más moderna
boton_cargar_seguidores_html = ttk.Button(root, text="Cargar Seguidores (HTML)", command=cargar_seguidores_html)
boton_cargar_seguidores_html.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

boton_cargar_seguidos_html = ttk.Button(root, text="Cargar Seguidos (HTML)", command=cargar_seguidos_html)
boton_cargar_seguidos_html.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

boton_cargar_seguidores_json = ttk.Button(root, text="Cargar Seguidores (JSON)", command=cargar_seguidores_json)
boton_cargar_seguidores_json.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

boton_cargar_seguidos_json = ttk.Button(root, text="Cargar Seguidos (JSON)", command=cargar_seguidos_json)
boton_cargar_seguidos_json.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

boton_comparar = ttk.Button(root, text="Comparar Listas", command=comparar_listas)
boton_comparar.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew", padx=100)

# Cambiar el estilo de ttk
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))

# Área de texto para mostrar resultados
resultado_texto = tk.Text(root, height=20, width=30)
resultado_texto.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew", padx=20)
resultado_texto.configure(bg="#EDEDED", bd=1, relief="sunken")

# Ejecutar el bucle principal de la ventana
root.mainloop()
