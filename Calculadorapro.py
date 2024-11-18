import tkinter as tk
from tkinter import ttk
import math

class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Calculadora Pro")
        self.dark_mode = False
        
        # Estilos por defecto (modo claro)
        self.light_colors = {
            'bg': '#f0f0f0',
            'fg': '#000000',
            'button_bg': '#ffffff',
            'screen_bg': '#ffffff'
        }
        
        # Estilos modo oscuro
        self.dark_colors = {
            'bg': '#2c2c2c',
            'fg': '#ffffff',
            'button_bg': '#404040',
            'screen_bg': '#1c1c1c'
        }
        
        self.current_colors = self.light_colors
        self.configure(bg=self.current_colors['bg'])
        self.resizable(True, True)
        
        # Variables
        self.current = ''
        self.resultado = tk.StringVar(value='0')
        self.memoria = 0
        self.historial = []
        
        self.crear_widgets()
        self.configurar_atajos_teclado()
        
    def crear_widgets(self):
        # Estilo personalizado
        style = ttk.Style()
        style.configure('Custom.TButton', padding=5)
        
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Frame para historial
        self.historial_frame = ttk.Frame(self.main_frame)
        self.historial_frame.grid(row=0, column=4, rowspan=6, padx=5, sticky="nsew")
        
        # Label de historial
        self.historial_label = ttk.Label(self.historial_frame, text="Historial", anchor="center")
        self.historial_label.pack(fill="x", pady=5)
        
        # Listbox para historial
        self.historial_list = tk.Listbox(self.historial_frame, height=10)
        self.historial_list.pack(fill="both", expand=True)
        
        # Pantalla
        self.pantalla = ttk.Entry(
            self.main_frame, 
            textvariable=self.resultado, 
            justify='right',
            font=('Arial', 24)
        )
        self.pantalla.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        
        # Botones científicos
        botones_cientificos = [
            'sin', 'cos', 'tan', 'M+',
            'log', 'ln', 'π', 'M-',
            '(', ')', 'MR', 'MC'
        ]
        
        row = 1
        col = 0
        for boton in botones_cientificos:
            cmd = lambda x=boton: self.click_cientifico(x)
            btn = ttk.Button(
                self.main_frame,
                text=boton,
                command=cmd,
                style='Custom.TButton'
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Botones básicos
        botones = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            '%', 'C', '√', '^2'
        ]
        
        for boton in botones:
            cmd = lambda x=boton: self.click(x)
            btn = ttk.Button(
                self.main_frame,
                text=boton,
                command=cmd,
                style='Custom.TButton'
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Botón de modo oscuro
        self.dark_mode_btn = ttk.Button(
            self.main_frame,
            text="🌙 Modo Oscuro",
            command=self.toggle_dark_mode,
            style='Custom.TButton'
        )
        self.dark_mode_btn.grid(row=row, column=0, columnspan=4, sticky="nsew", pady=5)
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        for i in range(5):
            self.main_frame.grid_columnconfigure(i, weight=1)
        for i in range(8):
            self.main_frame.grid_rowconfigure(i, weight=1)
            
    def configurar_atajos_teclado(self):
        self.bind('<Return>', lambda e: self.click('='))
        self.bind('<Escape>', lambda e: self.click('C'))
        for num in range(10):
            self.bind(str(num), lambda e, num=num: self.click(str(num)))
        self.bind('+', lambda e: self.click('+'))
        self.bind('-', lambda e: self.click('-'))
        self.bind('*', lambda e: self.click('*'))
        self.bind('/', lambda e: self.click('/'))
            
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.current_colors = self.dark_colors if self.dark_mode else self.light_colors
        
        # Actualizar colores
        self.configure(bg=self.current_colors['bg'])
        self.dark_mode_btn.configure(text="☀️ Modo Claro" if self.dark_mode else "🌙 Modo Oscuro")
        
        # Actualizar estilos de widgets
        style = ttk.Style()
        style.configure('TFrame', background=self.current_colors['bg'])
        style.configure('TLabel', background=self.current_colors['bg'], foreground=self.current_colors['fg'])
        style.configure('TButton', background=self.current_colors['button_bg'])
        self.pantalla.configure(style='Custom.TEntry')
        
    def click_cientifico(self, operacion):
        if operacion == 'sin':
            try:
                resultado = math.sin(float(self.current))
                self.resultado.set(resultado)
                self.current = str(resultado)
                self.agregar_historial(f'sin({self.current}) = {resultado}')
            except:
                self.resultado.set('Error')
        elif operacion == 'cos':
            try:
                resultado = math.cos(float(self.current))
                self.resultado.set(resultado)
                self.current = str(resultado)
                self.agregar_historial(f'cos({self.current}) = {resultado}')
            except:
                self.resultado.set('Error')
        elif operacion == 'tan':
            try:
                resultado = math.tan(float(self.current))
                self.resultado.set(resultado)
                self.current = str(resultado)
                self.agregar_historial(f'tan({self.current}) = {resultado}')
            except:
                self.resultado.set('Error')
        elif operacion == 'log':
            try:
                resultado = math.log10(float(self.current))
                self.resultado.set(resultado)
                self.current = str(resultado)
                self.agregar_historial(f'log({self.current}) = {resultado}')
            except:
                self.resultado.set('Error')
        elif operacion == 'ln':
            try:
                resultado = math.log(float(self.current))
                self.resultado.set(resultado)
                self.current = str(resultado)
                self.agregar_historial(f'ln({self.current}) = {resultado}')
            except:
                self.resultado.set('Error')
        elif operacion == 'π':
            self.current = str(math.pi)
            self.resultado.set(self.current)
        elif operacion in ['M+', 'M-', 'MR', 'MC']:
            self.operacion_memoria(operacion)
            
    def operacion_memoria(self, operacion):
        if operacion == 'M+':
            try:
                self.memoria += float(self.current)
                self.agregar_historial(f'M+ ({self.current})')
            except:
                pass
        elif operacion == 'M-':
            try:
                self.memoria -= float(self.current)
                self.agregar_historial(f'M- ({self.current})')
            except:
                pass
        elif operacion == 'MR':
            self.current = str(self.memoria)
            self.resultado.set(self.current)
            self.agregar_historial(f'MR = {self.memoria}')
        elif operacion == 'MC':
            self.memoria = 0
            self.agregar_historial('MC')
            
    def click(self, tecla):
        if tecla == '=':
            try:
                resultado = eval(self.current)
                self.resultado.set(resultado)
                self.agregar_historial(f'{self.current} = {resultado}')
                self.current = str(resultado)
            except:
                self.resultado.set('Error')
                self.current = ''
        elif tecla == 'C':
            self.current = ''
            self.resultado.set('0')
        else:
            self.current += tecla
            self.resultado.set(self.current)
            
    def agregar_historial(self, operacion):
        self.historial.append(operacion)
        self.historial_list.insert(0, operacion)
        if len(self.historial) > 10:
            self.historial.pop(0)
            self.historial_list.delete(10)

if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
