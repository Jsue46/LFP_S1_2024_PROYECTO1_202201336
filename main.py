from analizador import analizador_lexico, analizar_texto, imprimir_tokens_y_errores
from tkinter import scrolledtext
import tkinter as tk
from tkinter import filedialog
from tkinter import Menu
import re


def convertir_color_a_hexadecimal(color):
    colores = {
        'rojo': '#FF0000',
        'amarillo': '#FFFF00',
        'azul': '#0000FF',
        'cyan': '#00FFFF'
        
    }
    # Pasar color a hexadecimal
    if color.lower() in colores:
        return colores[color.lower()]
    elif color.startswith('#') and len(color) == 7 and all(c in '0123456789ABCDEFabcdef' for c in color[1:]):
        return color
    else:
        return '#000000' 
    
def traducir_a_html(tokens):
    html = "<!DOCTYPE html>\n<html>\n<head>\n<title>"
    titulo_pagina = ""
    cuerpo = ""
    fondo_estilo = "" 
    saltos = 0  

    
    tamanos_a_encabezados = {
        't1': 'h1',
        't2': 'h2',
        't3': 'h3',
        't4': 'h4',
        't5': 'h5',
        't6': 'h6'
    }

    for token, valor in tokens:
        print(f"Token: {token}, Valor: {valor}")  # Imprimir el token y su valor

        if token == 'TITULOPAGINA':
            titulo_pagina = valor
        elif token == 'FONDO':
            fondo_estilo = f"background-color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))};"
        elif token == 'TITULO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            alineacion = 'center' if alineacion == 'centro' else alineacion
            alineacion = 'right' if alineacion == 'derecha' else alineacion  
            # Pasar el tamaño del título a la etiqueta HTML 
            tamaño = extraer_valor(valor, 'tamaño', 't1')
            etiqueta_encabezado = tamanos_a_encabezados.get(tamaño, 'h1')
            cuerpo += f"<{etiqueta_encabezado} style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</{etiqueta_encabezado}>\n"
        elif token == 'PARRAFO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            alineacion = 'center' if alineacion == 'centro' else alineacion
            alineacion = 'right' if alineacion == 'derecha' else alineacion  
            cuerpo += f"<p style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</p>\n"
        elif token == 'TEXTO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            alineacion = 'center' if alineacion == 'centro' else alineacion
            alineacion = 'right' if alineacion == 'derecha' else alineacion  
            cuerpo += f"<span style='font-family:{extraer_valor(valor, 'fuente')}; color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; font-size:{extraer_valor(valor, 'tamaño')}px; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</span>\n"
        elif token == 'CODIGO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            alineacion = 'center' if alineacion == 'centro' else alineacion
            alineacion = 'right' if alineacion == 'derecha' else alineacion  
            cuerpo += f"<code style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</code>\n"
        elif token == 'NEGRITA':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<b style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</b>\n"
        elif token == 'SUBRAYADO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<u style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</u>\n"
        elif token == 'TACHADO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<strike style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</strike>\n"
        elif token == 'CURSIVA':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<i style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</i>\n"
        elif token == 'TABLA':
            filas = int(extraer_valor(valor, 'filas', '0'))
            columnas = int(extraer_valor(valor, 'columnas', '0'))
            tabla_html = "<table border='1'>\n"
            elementos_tabla = extraerElementosTabla(valor)
            for fila in range(filas):
                tabla_html += "<tr>\n"
                for columna in range(columnas):
                    texto_elemento = ""
                    for elemento in elementos_tabla:
                        if int(elemento['fila']) == fila + 1 and int(elemento['columna']) == columna + 1:
                            texto_elemento = elemento['texto']
                            break
                    tabla_html += f"<td>{texto_elemento}</td>\n"
                tabla_html += "</tr>\n"
            tabla_html += "</table>\n"
            cuerpo += tabla_html
        elif token == 'SALTO':
            cantidad_saltos = int(extraer_valor(valor, 'cantidad', '1'))
            print(f"SALTOS DE LÍNEA: {cantidad_saltos}")  # verificar la cantidad de saltos de línea
            cuerpo += "<br>" * cantidad_saltos 
            print(f"CUERPO DESPUÉS DEL SALTO: {cuerpo}")  # verificar después de agregar los saltos de línea
    
    html += f"{titulo_pagina}</title>\n</head>\n<body style='{fondo_estilo}'>\n{cuerpo}</body>\n</html>"
    return html

def extraerElementosTabla(token_str):
    # Patrón para encontrar todos los elementos de la tabla
    elemento_pattern = r'elemento:{"fila":"(\d+)","columna":"(\d+)","([^"]*)"}'
    matches = re.findall(elemento_pattern, token_str)
    elementos = []
    for match in matches:
        elemento = {
            'fila': match[0],
            'columna': match[1],
            'texto': match[2]
        }
        elementos.append(elemento)
    return elementos

def extraer_valor(token_str, atributo, valor_predeterminado=""):
    # RE para buscar el valor del atributo en la cadena del token
    patron = rf'{atributo}:\s*"([^"]*)"'
    matches = re.findall(patron, token_str)
    if matches:
        return matches[0]
    return valor_predeterminado if atributo != "posicion" else "left"
# Ventana principal
class VentanaPrincipal:
    def on_enter(self, event):
        event.widget.config(bg="grey")

    def on_leave(self, event):
        event.widget.config(bg="#142157")
    
    def __init__(self, root):
        # Variables que se analizan
        # Ventana principal
        self.root = root
        self.root.title("Proyecto 1 - 202201336")
        self.root.geometry("1200x650")
        self.root.configure(bg="white")
        self.root.resizable(0   ,0)
        # Frame principal
        titulo_frame = tk.Frame(root, bg="#142157")
        # Titulo label
        label_titulo = tk.Label(titulo_frame, text="Proyecto 1 Lenguajes Formales")
        label_titulo.config(font=("Arial", 16), bg="#142157", fg="white")
        label_titulo.pack(fill='both', expand= True)
        # Configuración del frame
        titulo_frame.place(x=0, y=0,)
        titulo_frame.config(width=1200, height=50)
        titulo_frame.pack_propagate(0)
        # Frame de botones
        opciones_frame = tk.Frame(root, bg="#4A6EB0")
        # Botones
        boton_archivo = tk.Menubutton(opciones_frame, text="Archivo", bg="#142157", font=("Arial", 12), bd=0, fg="white", activeforeground='black')
        boton_archivo.place(x=50, y=10, width=150, height=30)
        # Opciones del boton archivo
        opciones=Menu(boton_archivo, tearoff=0)
        boton_archivo["menu"]=opciones
        opciones.add_command(label="Abrir", font=("Arial", 12), activeforeground='black', command=self.abrir_archivo)
        opciones.add_command(label="salir", font=("Arial", 12), activeforeground='black', command=self.salir)
        # Boton traducir
        boton_traducir = tk.Menubutton(opciones_frame, text="Traducir", bg="#142157", font=("Arial", 12), bd=0, fg="white", activeforeground='black')
        boton_traducir.place(x=650, y=10, width=150, height=30)
        # Opciones del boton traducir
        opciones=Menu(boton_traducir, tearoff=0)
        boton_traducir["menu"]=opciones
        opciones.add_command(label="Traducir", font=("Arial", 12), activeforeground='black', command=self.traducir_archivo)

        
        # Configuración del frame
        opciones_frame.place(x=0, y=50)
        opciones_frame.pack_propagate()
        opciones_frame.config(width=1200, height=50)

        # Frame del cuadro de texto
        cuadrotexto_frame = tk.Frame(root, bg="#0799B6")
        # Cuadro de texto
        self.areatexto = scrolledtext.ScrolledText(cuadrotexto_frame, font=("Arial", 12), bg="white",  width=60, height=28)
        self.areatexto.place(x=30, y=30)
        self.consola = scrolledtext.ScrolledText(cuadrotexto_frame, font=("Arial", 12), bg="white", width=60, height=28)
        self.consola.place(x=600, y=30)
        self.label_consola = tk.Label(cuadrotexto_frame, text="Traduccion:", font=("Arial", 12), fg="white", bg="#0799B6")
        self.label_consola.place(x=600, y=5)
        self.label_consola = tk.Label(cuadrotexto_frame, text="Texto de Entrada: ", font=("Arial", 12), fg="white", bg="#0799B6")   
        self.label_consola.place(x=30, y=5)
        # Configuración del frame
        cuadrotexto_frame.place(x=0, y=100)
        cuadrotexto_frame.pack_propagate()
        cuadrotexto_frame.config(width=1200, height=600)





    def abrir_archivo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.areatexto.delete('1.0', tk.END)
                self.areatexto.insert(tk.END, content)


    def salir(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def traducir_archivo(self):
   
        content = self.areatexto.get("1.0", tk.END)

        self.consola.delete("1.0", tk.END)

        tokens = analizar_texto(content)
        html = traducir_a_html(tokens)

        self.consola.insert(tk.END, html)

        with open("salida.html", "w") as file:
            file.write(html)
            
        tokens, errores_lexicos = analizador_lexico(self.areatexto, self.consola)
        imprimir_tokens_y_errores(tokens, errores_lexicos)



if __name__ == "__main__":
    root = tk.Tk()
    ventana_principal = VentanaPrincipal(root)
    root.mainloop()
