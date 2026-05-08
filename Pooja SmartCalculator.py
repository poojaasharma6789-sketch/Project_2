import customtkinter as ctk
import math
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PoojaSmartCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pooja's Design")
        self.geometry("480x850") # Thoda height adjust kiya
        self.resizable(False, False)

        self.data_input = ""
        self.vaani = ctk.StringVar()
        self.mode = "DEG" 

        self.setup_ui()
        self.bind("<Key>", self.keyboard_logic)
        self.focus_set()

    def setup_ui(self):
        # 1. Clock & Mode Indicator
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=25, pady=(10, 0))
        
        self.mode_label = ctk.CTkLabel(self.top_frame, text="MODE: DEG", font=("Arial", 12, "bold"), text_color="#00f2fe")
        self.mode_label.pack(side="left")
        
        self.clock_label = ctk.CTkLabel(self.top_frame, text="", font=("Arial", 12), text_color="#aaaaaa")
        self.clock_label.pack(side="right")
        self.update_clock()

        # 2. Main Display
        self.display = ctk.CTkEntry(self, textvariable=self.vaani, font=("Arial", 36, "bold"),
                                   height=100, corner_radius=15, fg_color="#1a1a1a", 
                                   text_color="#ffffff", border_color="#333333", justify="right")
        self.display.pack(pady=20, padx=25, fill="x")

        # 3. DEG/RAD Toggle
        self.toggle_switch = ctk.CTkSegmentedButton(self, values=["DEG", "RAD"], 
                                                    command=self.change_mode,
                                                    selected_color="#00adb5")
        self.toggle_switch.set("DEG")
        self.toggle_switch.pack(pady=10)

        # 4. Tabs
        self.tabs = ctk.CTkTabview(self, corner_radius=20, border_width=1, border_color="#2a2a2a")
        self.tabs.pack(padx=15, pady=5, fill="both", expand=True)
        self.tab_std = self.tabs.add("Standard")
        self.tab_sci = self.tabs.add("Scientific")

        # 5. Buttons Layout
        std_btns = [
            ['C', '⌫', '%', '÷'], 
            ['7', '8', '9', '*'], 
            ['4', '5', '6', '-'], 
            ['1', '2', '3', '+'], 
            ['.', '0', '=', '']
        ]
        
        sci_btns = [
            ['sin', 'cos', 'tan', '√'],
            ['log', 'fact', 'π', 'e'],
            ['x²', 'x³', 'x^y', '÷'], 
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['(', ')', '0', '='],
            ['C', '⌫', '.', '+']
        ]
        
        self.create_grid(self.tab_std, std_btns, True)
        self.create_grid(self.tab_sci, sci_btns, False)

    def create_grid(self, parent, btns, is_std):
        for r, row in enumerate(btns):
            for c, b in enumerate(row):
                if b == '': continue
                color = "#2b2b2b"
                if b == '=': color = "#00adb5"
                elif b in ['C', '⌫']: color = "#ff2e63"
                elif b in ['x²', 'x³', 'x^y']: color = "#3d3d3d"
                
                btn = ctk.CTkButton(parent, text=b, width=90, height=65 if is_std else 50, corner_radius=12,
                                   fg_color=color, font=("Arial", 18 if is_std else 14, "bold"),
                                   command=lambda x=b: self.handle_click(x))
                btn.grid(row=r, column=c, padx=5, pady=5)

    def change_mode(self, value):
        self.mode = value
        self.mode_label.configure(text=f"MODE: {value}")

    def update_clock(self):
        self.clock_label.configure(text=time.strftime("%H:%M:%S"))
        self.after(1000, self.update_clock)

    def handle_click(self, btn):
        if btn == "=":
            try:
                # Proper replacements for evaluation
                exp = self.data_input.replace("÷", "/").replace("π", str(math.pi)).replace("e", str(math.e)).replace("%", "/100")
                
                # Trigonometry wrapper
                def tr(func, x):
                    val = math.radians(x) if self.mode == "DEG" else x
                    if func == "tan" and round(math.cos(val), 10) == 0: return "Undefined"
                    return getattr(math, func)(val)

                # Safe environment for eval
                safe_dict = {
                    "sin": lambda x: tr("sin", x),
                    "cos": lambda x: tr("cos", x),
                    "tan": lambda x: tr("tan", x),
                    "log": lambda x: math.log10(x) if x > 0 else "Log Error",
                    "fact": lambda x: math.factorial(int(x)),
                    "sqrt": math.sqrt
                }

                res = eval(exp, {"__builtins__": None}, safe_dict)
                
                if isinstance(res, float):
                    res = round(res, 8)
                
                self.vaani.set(res)
                self.data_input = str(res)
            except Exception:
                self.vaani.set("Math Error")
                self.data_input = ""
        
        elif btn == "C": 
            self.data_input = ""
            self.vaani.set("")
        elif btn == "⌫": 
            self.data_input = self.data_input[:-1]
            self.vaani.set(self.data_input)
        elif btn == "x²": 
            self.data_input += "**2"
            self.vaani.set(self.data_input)
        elif btn == "x³": 
            self.data_input += "**3"
            self.vaani.set(self.data_input)
        elif btn == "x^y": 
            self.data_input += "**"
            self.vaani.set(self.data_input)
        elif btn in ['sin', 'cos', 'tan', 'log', 'fact', '√']:
            cmd = "sqrt(" if btn == "√" else btn + "("
            self.data_input += cmd
            self.vaani.set(self.data_input)
        else:
            self.data_input += str(btn)
            self.vaani.set(self.data_input)

    def keyboard_logic(self, event):
        key = event.char
        if event.keysym == "Return": self.handle_click("=")
        elif event.keysym == "BackSpace": self.handle_click("⌫")
        elif key in "0123456789.+-*/()%": 
            # Translate keyboard keys to match calculator symbols
            k = key.replace("/", "÷")
            self.handle_click(k)

if __name__ == "__main__":
    app = PoojaSmartCalculator()
    app.mainloop()
    
