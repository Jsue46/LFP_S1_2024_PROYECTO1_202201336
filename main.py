import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext



class ventana_principal:
    def on_enter(self, event):
        event.widget.config(bg="grey")

    def on_leave(self, event):
        event.widget.config(bg="#142157")
    
    def __init__(self, root):
        #variables que se analizan
        #ventana principal
        self.root = root
        self.root.title("Proyecto 1 - Estuardo Josué Vaquiax Reyes")
        self.root.geometry("1200x650")
        self.root.configure(bg="white")
        self.root.resizable(0   ,0)
        #frame principal
        titulo_frame = tk.Frame(root, bg="#142157")
        #titulo label
        label_titulo = tk.Label(titulo_frame, text="Proyecto 1 Lenguajes Formales")
        label_titulo.config(font=("Arial", 16), bg="#142157", fg="white")
        label_titulo.pack(fill='both', expand= True)
        #confuración del frame
        titulo_frame.place(x=0, y=0,)
        titulo_frame.config(width=1200, height=50)
        titulo_frame.pack_propagate(0)
        #frame de botones
        opciones_frame = tk.Frame(root, bg="#4A6EB0")
        #botones
        boton_archivo = tk.Menubutton(opciones_frame, text="Archivo", bg="#142157", font=("Arial", 12), bd=0, fg="white", activeforeground='black')
        boton_archivo.place(x=50, y=10, width=150, height=30)
        #opciones del boton archivo
        opciones=Menu(boton_archivo, tearoff=0)
        boton_archivo["menu"]=opciones
        opciones.add_command(label="Abrir", font=("Arial", 12), activeforeground='black', command=self.abrir_archivo)
        opciones.add_command(label="salir", font=("Arial", 12), activeforeground='black', command=self.salir)
        #boton traducir
        boton_traducir = tk.Menubutton(opciones_frame, text="Traducir", bg="#142157", font=("Arial", 12), bd=0, fg="white", activeforeground='black')
        boton_traducir.place(x=650, y=10, width=150, height=30)
        #opciones del boton traducir
        opciones=Menu(boton_traducir, tearoff=0)
        boton_traducir["menu"]=opciones
        opciones.add_command(label="Traducir", font=("Arial", 12), activeforeground='black', command=self.traducir_archivo)

        
        #confuración del frame
        opciones_frame.place(x=0, y=50)
        opciones_frame.pack_propagate()
        opciones_frame.config(width=1200, height=50)

        #frame del cuadro de texto
        cuadrotexto_frame = tk.Frame(root, bg="#0799B6")
        #cuadro de texto
        self.areatexto = scrolledtext.ScrolledText(cuadrotexto_frame, font=("Arial", 12), bg="white",  width=60, height=28)
        self.areatexto.place(x=30, y=30)
        self.consola = scrolledtext.ScrolledText(cuadrotexto_frame, font=("Arial", 12), bg="white", width=60, height=28)
        self.consola.place(x=600, y=30)
        self.label_consola = tk.Label(cuadrotexto_frame, text="Traduccion:", font=("Arial", 12), fg="white", bg="#0799B6")
        self.label_consola.place(x=600, y=5)
        self.label_consola = tk.Label(cuadrotexto_frame, text="Texto de Entrada: ", font=("Arial", 12), fg="white", bg="#0799B6")   
        self.label_consola.place(x=30, y=5)
        #confuración del frame
        cuadrotexto_frame.place(x=0, y=100)
        cuadrotexto_frame.pack_propagate()
        cuadrotexto_frame.config(width=1200, height=600)





    def abrir_archivo(self):
        file_path = filedialog.askopenfilename()
        print(file_path)


    def salir(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def traducir_archivo(self):
        print("traducir")

if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = ventana_principal(ventana)
    ventana.mainloop()