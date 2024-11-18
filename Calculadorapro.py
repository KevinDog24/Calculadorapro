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
        
        # Diccionarios de conversión
        self.conversiones = {
            'Longitud': {
                'm → km': lambda x: x/1000,
                'km → m': lambda x: x*1000,
                'm → cm': lambda x: x*100,
                'cm → m': lambda x: x/100,
                'pies → metros': lambda x: x*0.3048,
                'metros → pies': lambda x: x/0.3048
            },
            'Temperatura': {
                'C → F': lambda x: (x * 9/5) + 32,
                'F → C': lambda x: (x - 32) * 5/9,
                'C → K': lambda x: x + 273.15,
                'K → C': lambda x: x - 273.15
            },
            'Peso': {
                'kg → lb': lambda x: x*2.20462,
                'lb → kg': lambda x: x/2.20462,
                'g → kg': lambda x: x/1000,
                'kg → g': lambda x: x*1000
            }
        }
        
        self.crear_widgets()
        self.configurar_atajos_teclado()
        
    def crear_widgets(self):
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Pestaña Calculadora
        self.calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calc_frame, text='Calculadora')
        
        # Pestaña Conversiones
        self.conv_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.conv_frame, text='Conversiones')
        
        # Frame principal calculadora
        self.main_frame = ttk.Frame(self.calc_frame)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Crear interfaz de calculadora básica
        self.crear_calculadora()
        
        # Crear interfaz de conversiones
        self.crear_conversiones()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def crear_calculadora(self):
        # Frame para historial
        self.historial_frame = ttk.Frame(self.main_frame)
        self.historial_frame.grid(row=0, column=4, rowspan=6, padx=5, sticky="nsew")
        
        # Label de historial
        self.historial_label = ttk.Label(self.historial_frame, text="Historial")
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
        
        # Botones porcentaje avanzado
        botones_porcentaje = [
            'Aumento %', 'Descuento %', 
            'Diferencia %', '% del total'
        ]
        
        row = 1
        col = 0
        for boton in botones_porcentaje:
            cmd = lambda x=boton: self.calcular_porcentaje(x)
            btn = ttk.Button(
                self.main_frame,
                text=boton,
                command=cmd
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
        
        # Botones científicos
        botones_cientificos = [
            'sin', 'cos', 'tan', 'M+',
            'log', 'ln', 'π', 'M-',
            '(', ')', 'MR', 'MC'
        ]
        
        row = 2
        col = 0
        for boton in botones_cientificos:
            cmd = lambda x=boton: self.click_cientifico(x)
            btn = ttk.Button(
                self.main_frame,
                text=boton,
                command=cmd
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
                command=cmd
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
                
        # Botón modo oscuro
        self.dark_mode_btn = ttk.Button(
            self.main_frame,
            text="🌙 Modo Oscuro",
            command=self.toggle_dark_mode
        )
        self.dark_mode_btn.grid(row=row, column=0, columnspan=4, sticky="nsew", pady=5)
    
    def crear_conversiones(self):
        # Variables para conversiones
        self.valor_conversion = tk.StringVar(value='0')
        self.tipo_conversion = tk.StringVar(value='Longitud')
        self.conversion_especifica = tk.StringVar()
        
        # Frame para conversiones
        conv_container = ttk.Frame(self.conv_frame)
        conv_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Selector de tipo de conversión
        ttk.Label(conv_container, text="Tipo de conversión:").pack(fill="x", pady=5)
        tipo_cb = ttk.Combobox(
            conv_container, 
            textvariable=self.tipo_conversion,
            values=list(self.conversiones.keys())
        )
        tipo_cb.pack(fill="x", pady=5)
        tipo_cb.bind('<<ComboboxSelected>>', self.actualizar_conversiones)
        
        # Selector de conversión específica
        ttk.Label(conv_container, text="Conversión:").pack(fill="x", pady=5)
        self.conv_especifica_cb = ttk.Combobox(
            conv_container, 
            textvariable=self.conversion_especifica
        )
        self.conv_especifica_cb.pack(fill="x", pady=5)
        
        # Entrada de valor
        ttk.Label(conv_container, text="Valor:").pack(fill="x", pady=5)
        self.entrada_conversion = ttk.Entry(
            conv_container,
            textvariable=self.valor_conversion
        )
        self.entrada_conversion.pack(fill="x", pady=5)
        
        # Botón convertir
        ttk.Button(
            conv_container,
            text="Convertir",
            command=self.realizar_conversion
        ).pack(fill="x", pady=10)
        
        # Resultado
        self.resultado_conversion = ttk.Label(
            conv_container,
            text="Resultado: "
        )
        self.resultado_conversion.pack(fill="x", pady=5)
        
        # Inicializar lista de conversiones
        self.actualizar_conversiones()
        
    def actualizar_conversiones(self, event=None):
        tipo = self.tipo_conversion.get()
        self.conv_especifica_cb['values'] = list(self.conversiones[tipo].keys())
        if self.conv_especifica_cb['values']:
            self.conv_especifica_cb.set(self.conv_especifica_cb['values'][0])
            
    def realizar_conversion(self):
        try:
            tipo = self.tipo_conversion.get()
            conv = self.conversion_especifica.get()
            valor = float(self.valor_conversion.get())
            
            resultado = self.conversiones[tipo][conv](valor)
            
            # Formatear resultado según el tipo
            if tipo == 'Temperatura':
                resultado_str = f"{resultado:.1f}°"
            elif tipo == 'Peso':
                resultado_str = f"{resultado:.3f}"
            else:
                resultado_str = f"{resultado:.2f}"
                
            self.resultado_conversion.config(
                text=f"Resultado: {valor} {conv.split('→')[0].strip()} = {resultado_str} {conv.split('→')[1].strip()}"
            )
            
            # Agregar al historial
            self.agregar_historial(f"Conversión: {valor} {conv} = {resultado_str}")
            
        except ValueError:
            self.resultado_conversion.config(text="Error: Ingrese un número válido")
        except Exception as e:
            self.resultado_conversion.config(text=f"Error: {str(e)}")
            
    def calcular_porcentaje(self, tipo):
        try:
            if tipo == 'Aumento %':
                valor = float(self.current)
                porcentaje = float(self.mostrar_dialogo("Ingrese el porcentaje de aumento:"))
                resultado = valor * (1 + porcentaje/100)
                self.agregar_historial(f"{valor} + {porcentaje}% = {resultado}")
                
            elif tipo == 'Descuento %':
                valor = float(self.current)
                porcentaje = float(self.mostrar_dialogo("Ingrese el porcentaje de descuento:"))
                resultado = valor * (1 - porcentaje/100)
                self.agregar_historial(f"{valor} - {porcentaje}% = {resultado}")
                
            elif tipo == 'Diferencia %':
                valor1 = float(self.current)
                valor2 = float(self.mostrar_dialogo("Ingrese el segundo valor:"))
                diferencia = ((valor2 - valor1) / valor1) * 100
                self.agregar_historial(f"Diferencia entre {valor1} y {valor2} = {diferencia}%")
                resultado = diferencia
                
            elif tipo == '% del total':
                parte = float(self.current)
                total = float(self.mostrar_dialogo("Ingrese el total:"))
                porcentaje = (parte / total) * 100
                self.agregar_historial(f"{parte} es {porcentaje}% de {total}")
                resultado = porcentaje
                
            self.resultado.set(str(resultado))
            self.current = str(resultado)
            
        except ValueError:
            self.resultado.set('Error')
            self.current = ''
            
    def mostrar_dialogo(self, mensaje):
        # Crear una ventana de diálogo simple
        dialogo = tk.Toplevel(self)
        dialogo.title("Entrada")
        
        ttk.Label(dialogo, text=mensaje).pack(pady=5)
        entrada = ttk.Entry(dialogo)
        entrada.pack(pady=5)
        
        valor = tk.StringVar()
        
        def aceptar():
            valor.set(entrada.get())
            dialogo.destroy()
            
        ttk.Button(dialogo, text="Aceptar", command=aceptar).pack(pady=5)
        
        # Hacer la ventana modal
        dialogo.transient(self)
        dialogo.grab_set()
        self.wait_window(dialogo)
        
        return valor.get()
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.current_colors = self.dark_colors if self.dark_mode else self.light_colors
        
        # Actualizar colores
        self.configure(bg=self.current_colors['bg'])
        
        # Actualizar texto del botón
        self.dark_mode_btn.configure(
            text="☀️ Modo Claro" if self.dark_mode else "🌙 Modo Oscuro"
        )
        
        # Actualizar colores de widgets
        style = ttk.Style()
        style.configure('TFrame', background=self.current_colors['bg'])
        style.configure('TLabel', foreground=self.current_colors['fg'])
        style.configure('TButton', background=self.current_colors['button_bg'])
        
        # Actualizar color de la pantalla y el historial
        self.pantalla.configure(style='Custom.TEntry')
        self.historial_list.configure(
            bg=self.current_colors['screen_bg'],
            fg=self.current_colors['fg']
        )

    def configurar_atajos_teclado(self):
        # Teclas numéricas y operadores básicos
        for key in '0123456789+-*/':
            self.bind(key, lambda e, key=key: self.click(key))
        
        # Teclas especiales
        self.bind('<Return>', lambda e: self.click('='))
        self.bind('<BackSpace>', lambda e: self.click('C'))
        self.bind('.', lambda e: self.click('.'))
        self.bind('(', lambda e: self.click('('))
        self.bind(')', lambda e: self.click(')'))
        
        # Teclas de función
        self.bind('<Escape>', lambda e: self.click('C'))
        
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
