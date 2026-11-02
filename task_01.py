import tkinter as tk
from tkinter import ttk, messagebox
import ast
import operator

# ---------------- SAFE CALCULATOR ----------------

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def calculate_node(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in operators:
        left = calculate_node(node.left)
        right = calculate_node(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Power is too large")

        return operators[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
        return operators[type(node.op)](calculate_node(node.operand))

    raise ValueError("Invalid expression")


def calculate():
    try:
        expression = display.get()
        tree = ast.parse(expression, mode="eval")
        result = calculate_node(tree.body)

        display.delete(0, tk.END)
        display.insert(tk.END, str(result))

    except ZeroDivisionError:
        messagebox.showerror("Error", "Cannot divide by zero!")

    except Exception:
        messagebox.showerror("Error", "Please enter a valid calculation!")


def press(value):
    display.insert(tk.END, value)


def clear():
    display.delete(0, tk.END)


def backspace():
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])


# ---------------- UNIT CONVERTER ----------------

def convert_unit():
    try:
        value = float(amount_entry.get())
        category = category_box.get()
        from_unit = from_box.get()
        to_unit = to_box.get()

        units = {
            "Length": {
                "Millimeter": 0.001,
                "Centimeter": 0.01,
                "Meter": 1,
                "Kilometer": 1000
            },
            "Weight": {
                "Milligram": 0.001,
                "Gram": 1,
                "Kilogram": 1000,
                "Tonne": 1000000
            }
        }

        if category in units:
            result = value * units[category][from_unit]
            result = result / units[category][to_unit]

        elif category == "Temperature":
            if from_unit == "Celsius":
                celsius = value
            elif from_unit == "Fahrenheit":
                celsius = (value - 32) * 5 / 9
            else:
                celsius = value - 273.15

            if to_unit == "Celsius":
                result = celsius
            elif to_unit == "Fahrenheit":
                result = (celsius * 9 / 5) + 32
            else:
                result = celsius + 273.15

        result_label.config(
            text=f"Result: {result:.4f} {to_unit}"
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

    except Exception:
        messagebox.showerror("Error", "Please select valid units!")


def update_units(event=None):
    category = category_box.get()

    unit_options = {
        "Length": ["Millimeter", "Centimeter", "Meter", "Kilometer"],
        "Weight": ["Milligram", "Gram", "Kilogram", "Tonne"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
    }

    values = unit_options[category]

    from_box["values"] = values
    to_box["values"] = values

    from_box.current(0)
    to_box.current(1)


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Interactive Calculator & Unit Converter")
root.geometry("500x550")
root.resizable(False, False)
root.configure(bg="#eaf2f8")

title = tk.Label(
    root,
    text="CALCULATOR & UNIT CONVERTER",
    font=("Arial", 16, "bold"),
    bg="#eaf2f8",
    fg="#154360"
)
title.pack(pady=15)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=10)

# ---------------- CALCULATOR TAB ----------------

calc_frame = tk.Frame(notebook, bg="#d6eaf8")
notebook.add(calc_frame, text="Calculator")

display = tk.Entry(
    calc_frame,
    font=("Arial", 22),
    justify="right",
    bd=5
)
display.pack(fill="x", padx=15, pady=20, ipady=10)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "%", "+"]
]

for row in buttons:
    button_frame = tk.Frame(calc_frame, bg="#d6eaf8")
    button_frame.pack(fill="x", padx=10)

    for item in row:
        tk.Button(
            button_frame,
            text=item,
            font=("Arial", 16, "bold"),
            width=7,
            height=2,
            command=lambda x=item: press(x)
        ).pack(side="left", expand=True, padx=3, pady=3)

action_frame = tk.Frame(calc_frame, bg="#d6eaf8")
action_frame.pack(fill="x", padx=10, pady=10)

tk.Button(
    action_frame,
    text="CLEAR",
    bg="#e74c3c",
    fg="white",
    font=("Arial", 12, "bold"),
    command=clear
).pack(side="left", expand=True, padx=5, ipady=8)

tk.Button(
    action_frame,
    text="DELETE",
    bg="#f39c12",
    fg="white",
    font=("Arial", 12, "bold"),
    command=backspace
).pack(side="left", expand=True, padx=5, ipady=8)

tk.Button(
    action_frame,
    text="=",
    bg="#27ae60",
    fg="white",
    font=("Arial", 16, "bold"),
    command=calculate
).pack(side="left", expand=True, padx=5, ipady=5)


# ---------------- CONVERTER TAB ----------------

converter_frame = tk.Frame(notebook, bg="#d5f5e3")
notebook.add(converter_frame, text="Unit Converter")

tk.Label(
    converter_frame,
    text="UNIT CONVERTER",
    font=("Arial", 18, "bold"),
    bg="#d5f5e3",
    fg="#145a32"
).pack(pady=20)

tk.Label(
    converter_frame,
    text="Enter Value:",
    font=("Arial", 12),
    bg="#d5f5e3"
).pack(pady=5)

amount_entry = tk.Entry(
    converter_frame,
    font=("Arial", 14),
    justify="center"
)
amount_entry.pack(pady=5)

tk.Label(
    converter_frame,
    text="Select Category:",
    font=("Arial", 12),
    bg="#d5f5e3"
).pack(pady=8)

category_box = ttk.Combobox(
    converter_frame,
    values=["Length", "Weight", "Temperature"],
    state="readonly",
    font=("Arial", 12)
)
category_box.pack(pady=5)
category_box.current(0)

tk.Label(
    converter_frame,
    text="From Unit:",
    font=("Arial", 12),
    bg="#d5f5e3"
).pack(pady=8)

from_box = ttk.Combobox(
    converter_frame,
    state="readonly",
    font=("Arial", 12)
)
from_box.pack(pady=5)

tk.Label(
    converter_frame,
    text="To Unit:",
    font=("Arial", 12),
    bg="#d5f5e3"
).pack(pady=8)

to_box = ttk.Combobox(
    converter_frame,
    state="readonly",
    font=("Arial", 12)
)
to_box.pack(pady=5)

category_box.bind("<<ComboboxSelected>>", update_units)
update_units()

tk.Button(
    converter_frame,
    text="CONVERT",
    bg="#229954",
    fg="white",
    font=("Arial", 13, "bold"),
    command=convert_unit,
    width=18
).pack(pady=20)

result_label = tk.Label(
    converter_frame,
    text="Result: ",
    font=("Arial", 16, "bold"),
    bg="#d5f5e3",
    fg="#154360"
)
result_label.pack(pady=10)

# ---------------- RUN APPLICATION ----------------

root.mainloop()