import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
import os
from functools import partial

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("500x700")
        
        # Initialize memory
        self.memory = 0
        self.history = []
        self.variables = {}
        self.current_theme = "light"
        
        # Create UI
        self.create_ui()
        self.load_settings()
        
    def create_ui(self):
        # Result display
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.result_display = ttk.Label(
            self.root, 
            textvariable=self.result_var,
            font=('Arial', 24),
            anchor="e",
            background="white"
        )
        self.result_display.pack(fill=tk.X, padx=10, pady=10)
        
        # History display
        self.history_display = tk.Listbox(
            self.root,
            height=5,
            font=('Arial', 10)
        )
        self.history_display.pack(fill=tk.X, padx=10, pady=5)
        
        # Create notebook for different modes
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Standard calculator tab
        self.standard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.standard_frame, text="Standard")
        self.create_standard_calculator()
        
        # Scientific calculator tab
        self.scientific_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scientific_frame, text="Scientific")
        self.create_scientific_calculator()
        
        # Programmer calculator tab
        self.programmer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.programmer_frame, text="Programmer")
        self.create_programmer_calculator()
        
        # Unit converter tab
        self.converter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.converter_frame, text="Converter")
        self.create_converter()
        
        # Memory buttons
        self.create_memory_buttons()
        
        # Menu bar
        self.create_menu()
        
    def create_standard_calculator(self):
        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', '⌫',
            '1', '2', '3', '-', '=',
            '0', '.', '(', ')', '+'
        ]
        
        self.create_button_grid(self.standard_frame, buttons)
    
    def create_scientific_calculator(self):
        buttons = [
            'sin', 'cos', 'tan', '√', '^',
            'asin', 'acos', 'atan', 'log', 'ln',
            'π', 'e', '(', ')', '=',
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', '⌫',
            '1', '2', '3', '-', 'M+',
            '0', '.', '(', ')', '+'
        ]
        
        self.create_button_grid(self.scientific_frame, buttons)
    
    def create_programmer_calculator(self):
        buttons = [
            'HEX', 'DEC', 'OCT', 'BIN', 'C',
            'AND', 'OR', 'XOR', 'NOT', '⌫',
            '<<', '>>', 'MOD', '^', '=',
            '7', '8', '9', '/', 'M+',
            '4', '5', '6', '*', 'M-',
            '1', '2', '3', '-', 'MR',
            '0', '.', '(', ')', '+'
        ]
        
        self.create_button_grid(self.programmer_frame, buttons)
    
    def create_converter(self):
        # Conversion types
        conversion_types = [
            "Length", "Weight", "Temperature", "Area", "Volume"
        ]
        
        self.conversion_type = tk.StringVar()
        self.conversion_type.set(conversion_types[0])
        
        type_menu = ttk.OptionMenu(
            self.converter_frame,
            self.conversion_type,
            *conversion_types
        )
        type_menu.pack(fill=tk.X, padx=10, pady=5)
        
        # From unit
        self.from_unit = tk.StringVar()
        self.from_unit.set("meters")
        
        # To unit
        self.to_unit = tk.StringVar()
        self.to_unit.set("feet")
        
        # Create unit dropdowns
        self.update_unit_dropdowns()
        
        # Value entry
        ttk.Label(self.converter_frame, text="Value:").pack(pady=5)
        self.convert_value = ttk.Entry(self.converter_frame)
        self.convert_value.pack(fill=tk.X, padx=10, pady=5)
        
        # Convert button
        convert_btn = ttk.Button(
            self.converter_frame,
            text="Convert",
            command=self.perform_conversion
        )
        convert_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Result display
        self.convert_result = ttk.Label(self.converter_frame, text="")
        self.convert_result.pack(fill=tk.X, padx=10, pady=5)
        
        # Bind conversion type change
        self.conversion_type.trace_add("write", self.update_unit_dropdowns)
    
    def update_unit_dropdowns(self, *args):
        # Clear existing dropdowns
        for widget in self.converter_frame.winfo_children():
            if isinstance(widget, ttk.OptionMenu) and widget not in [self.conversion_type]:
                widget.destroy()
        
        # Get current conversion type
        conv_type = self.conversion_type.get()
        
        # Define units for each type
        units = {
            "Length": ["meters", "feet", "inches", "centimeters", "miles", "kilometers"],
            "Weight": ["kilograms", "pounds", "ounces", "grams", "tons"],
            "Temperature": ["celsius", "fahrenheit", "kelvin"],
            "Area": ["square meters", "square feet", "acres", "hectares"],
            "Volume": ["liters", "gallons", "cubic meters", "cubic feet"]
        }
        
        # Create from unit dropdown
        ttk.Label(self.converter_frame, text="From:").pack(pady=5)
        from_menu = ttk.OptionMenu(
            self.converter_frame,
            self.from_unit,
            units[conv_type][0],
            *units[conv_type]
        )
        from_menu.pack(fill=tk.X, padx=10, pady=5)
        
        # Create to unit dropdown
        ttk.Label(self.converter_frame, text="To:").pack(pady=5)
        to_menu = ttk.OptionMenu(
            self.converter_frame,
            self.to_unit,
            units[conv_type][1],
            *units[conv_type]
        )
        to_menu.pack(fill=tk.X, padx=10, pady=5)
    
    def perform_conversion(self):
        try:
            value = float(self.convert_value.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            conv_type = self.conversion_type.get()
            
            # Length conversions
            if conv_type == "Length":
                # Convert to meters first
                if from_unit == "meters":
                    meters = value
                elif from_unit == "feet":
                    meters = value * 0.3048
                elif from_unit == "inches":
                    meters = value * 0.0254
                elif from_unit == "centimeters":
                    meters = value * 0.01
                elif from_unit == "miles":
                    meters = value * 1609.34
                elif from_unit == "kilometers":
                    meters = value * 1000
                
                # Convert from meters to target unit
                if to_unit == "meters":
                    result = meters
                elif to_unit == "feet":
                    result = meters / 0.3048
                elif to_unit == "inches":
                    result = meters / 0.0254
                elif to_unit == "centimeters":
                    result = meters / 0.01
                elif to_unit == "miles":
                    result = meters / 1609.34
                elif to_unit == "kilometers":
                    result = meters / 1000
            
            # Weight conversions
            elif conv_type == "Weight":
                # Convert to kilograms first
                if from_unit == "kilograms":
                    kg = value
                elif from_unit == "pounds":
                    kg = value * 0.453592
                elif from_unit == "ounces":
                    kg = value * 0.0283495
                elif from_unit == "grams":
                    kg = value * 0.001
                elif from_unit == "tons":
                    kg = value * 907.185
                
                # Convert from kg to target unit
                if to_unit == "kilograms":
                    result = kg
                elif to_unit == "pounds":
                    result = kg / 0.453592
                elif to_unit == "ounces":
                    result = kg / 0.0283495
                elif to_unit == "grams":
                    result = kg / 0.001
                elif to_unit == "tons":
                    result = kg / 907.185
            
            # Temperature conversions
            elif conv_type == "Temperature":
                # Convert to Celsius first
                if from_unit == "celsius":
                    celsius = value
                elif from_unit == "fahrenheit":
                    celsius = (value - 32) * 5/9
                elif from_unit == "kelvin":
                    celsius = value - 273.15
                
                # Convert from Celsius to target unit
                if to_unit == "celsius":
                    result = celsius
                elif to_unit == "fahrenheit":
                    result = (celsius * 9/5) + 32
                elif to_unit == "kelvin":
                    result = celsius + 273.15
            
            # Add other conversion types here...
            
            self.convert_result.config(text=f"{value} {from_unit} = {result:.4f} {to_unit}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def create_memory_buttons(self):
        memory_frame = ttk.Frame(self.root)
        memory_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("MS", self.memory_store)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(
                memory_frame,
                text=text,
                command=command
            )
            btn.pack(side=tk.LEFT, expand=True, padx=2)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save History", command=self.save_history)
        file_menu.add_command(label="Load History", command=self.load_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Clear History", command=self.clear_history)
        edit_menu.add_command(label="Variables", command=self.show_variables)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Light Theme", command=lambda: self.set_theme("light"))
        view_menu.add_command(label="Dark Theme", command=lambda: self.set_theme("dark"))
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_button_grid(self, parent, buttons):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        
        rows = 5
        cols = 5
        
        for i, text in enumerate(buttons):
            row = i // cols
            col = i % cols
            
            if text == "=":
                btn = ttk.Button(
                    frame,
                    text=text,
                    command=self.calculate,
                    style='Accent.TButton'
                )
            else:
                btn = ttk.Button(
                    frame,
                    text=text,
                    command=partial(self.button_click, text)
                )
            
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            frame.grid_columnconfigure(col, weight=1)
            frame.grid_rowconfigure(row, weight=1)
    
    def button_click(self, text):
        current = self.result_var.get()
        
        if text == "C":
            self.result_var.set("0")
        elif text == "⌫":
            if len(current) > 1:
                self.result_var.set(current[:-1])
            else:
                self.result_var.set("0")
        elif text in ["sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "√"]:
            try:
                value = float(current)
                if text == "sin":
                    result = math.sin(math.radians(value))
                elif text == "cos":
                    result = math.cos(math.radians(value))
                elif text == "tan":
                    result = math.tan(math.radians(value))
                elif text == "asin":
                    result = math.degrees(math.asin(value))
                elif text == "acos":
                    result = math.degrees(math.acos(value))
                elif text == "atan":
                    result = math.degrees(math.atan(value))
                elif text == "log":
                    result = math.log10(value)
                elif text == "ln":
                    result = math.log(value)
                elif text == "√":
                    result = math.sqrt(value)
                
                self.result_var.set(str(result))
                self.add_to_history(f"{text}({current}) = {result}")
            except ValueError:
                messagebox.showerror("Error", "Invalid input for function")
        elif text == "π":
            self.result_var.set(str(math.pi))
        elif text == "e":
            self.result_var.set(str(math.e))
        elif text == "^":
            self.result_var.set(current + "**")
        else:
            if current == "0":
                self.result_var.set(text)
            else:
                self.result_var.set(current + text)
    
    def calculate(self):
        try:
            expression = self.result_var.get()
            # Replace special constants
            expression = expression.replace("π", str(math.pi))
            expression = expression.replace("e", str(math.e))
            
            result = eval(expression, {"__builtins__": None}, {**math.__dict__, **self.variables})
            self.result_var.set(str(result))
            self.add_to_history(f"{expression} = {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {e}")
    
    def add_to_history(self, entry):
        self.history.append(entry)
        self.history_display.insert(tk.END, entry)
        if len(self.history) > 10:  # Limit history to 10 entries
            self.history.pop(0)
            self.history_display.delete(0)
    
    def clear_history(self):
        self.history = []
        self.history_display.delete(0, tk.END)
    
    def save_history(self):
        try:
            with open("calculator_history.json", "w") as f:
                json.dump({
                    "history": self.history,
                    "memory": self.memory,
                    "variables": self.variables
                }, f)
            messagebox.showinfo("Success", "History saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save history: {e}")
    
    def load_history(self):
        try:
            if os.path.exists("calculator_history.json"):
                with open("calculator_history.json", "r") as f:
                    data = json.load(f)
                self.history = data.get("history", [])
                self.memory = data.get("memory", 0)
                self.variables = data.get("variables", {})
                
                self.history_display.delete(0, tk.END)
                for entry in self.history:
                    self.history_display.insert(tk.END, entry)
                
                messagebox.showinfo("Success", "History loaded successfully")
            else:
                messagebox.showinfo("Info", "No history file found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load history: {e}")
    
    def memory_clear(self):
        self.memory = 0
    
    def memory_recall(self):
        self.result_var.set(str(self.memory))
    
    def memory_add(self):
        try:
            value = float(self.result_var.get())
            self.memory += value
        except ValueError:
            messagebox.showerror("Error", "Invalid value in display")
    
    def memory_subtract(self):
        try:
            value = float(self.result_var.get())
            self.memory -= value
        except ValueError:
            messagebox.showerror("Error", "Invalid value in display")
    
    def memory_store(self):
        try:
            self.memory = float(self.result_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid value in display")
    
    def show_variables(self):
        var_window = tk.Toplevel(self.root)
        var_window.title("Variables")
        
        # List variables
        ttk.Label(var_window, text="Current Variables:").pack(pady=5)
        var_list = tk.Listbox(var_window)
        for name, value in self.variables.items():
            var_list.insert(tk.END, f"{name} = {value}")
        var_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add new variable
        ttk.Label(var_window, text="Add/Update Variable:").pack(pady=5)
        
        var_frame = ttk.Frame(var_window)
        var_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(var_frame, text="Name:").pack(side=tk.LEFT)
        var_name = ttk.Entry(var_frame)
        var_name.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        ttk.Label(var_frame, text="Value:").pack(side=tk.LEFT)
        var_value = ttk.Entry(var_frame)
        var_value.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        def add_variable():
            name = var_name.get()
            try:
                value = float(var_value.get())
                self.variables[name] = value
                var_list.insert(tk.END, f"{name} = {value}")
                var_name.delete(0, tk.END)
                var_value.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Value must be a number")
        
        ttk.Button(
            var_window,
            text="Add/Update",
            command=add_variable
        ).pack(pady=5)
    
    def set_theme(self, theme):
        self.current_theme = theme
        self.save_settings()
        
        if theme == "dark":
            self.root.tk_setPalette(
                background="#2d2d2d",
                foreground="#ffffff",
                activeBackground="#3d3d3d",
                activeForeground="#ffffff"
            )
            self.result_display.config(background="#2d2d2d", foreground="#ffffff")
        else:
            self.root.tk_setPalette(
                background="#f0f0f0",
                foreground="#000000",
                activeBackground="#e0e0e0",
                activeForeground="#000000"
            )
            self.result_display.config(background="white", foreground="black")
    
    def save_settings(self):
        try:
            with open("calculator_settings.json", "w") as f:
                json.dump({
                    "theme": self.current_theme,
                    "memory": self.memory
                }, f)
        except:
            pass
    
    def load_settings(self):
        try:
            if os.path.exists("calculator_settings.json"):
                with open("calculator_settings.json", "r") as f:
                    settings = json.load(f)
                self.current_theme = settings.get("theme", "light")
                self.memory = settings.get("memory", 0)
                self.set_theme(self.current_theme)
        except:
            pass
    
    def show_about(self):
        messagebox.showinfo(
            "About Advanced Calculator",
            "Advanced Calculator\n\n"
            "Features:\n"
            "- Standard and scientific calculations\n"
            "- Memory functions\n"
            "- Unit conversion\n"
            "- History tracking\n"
            "- Variable support\n"
            "- Themes\n\n"
            "Created with Python and Tkinter"
        )

if __name__ == "__main__":
    root = tk.Tk()
    
    # Create a custom style
    style = ttk.Style()
    style.configure('Accent.TButton', foreground='white', background='#0078d7')
    
    app = AdvancedCalculator(root)
    root.mainloop()