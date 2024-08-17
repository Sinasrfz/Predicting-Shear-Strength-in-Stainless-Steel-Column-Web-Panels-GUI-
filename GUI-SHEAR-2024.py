

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
from joblib import load
from sklearn.preprocessing import MinMaxScaler

# Scaler initialization
min_values = np.array([6.0, 88.7, 140.0, 45.0, 40.0, 0.0, 0.0, 16.0, 8377892.333, 7984488.333])
max_values = np.array([30.0, 300.0, 426.4, 200.0, 165.0, 100.0, 100.0, 24, 262295552, 218764745.5])
scaler = MinMaxScaler(feature_range=(-1, 1))
scaler.fit(np.array([min_values, max_values]))

# Model loading
def load_model(label_name):
    model_path = f"saved_models/ExtraTrees_best_model({label_name}).joblib"
    try:
        model = load(model_path)
    except FileNotFoundError:
        print(f"Model file {model_path} not found.")
        return None
    return model

# Load model for 'Vpz' label
label = "Vpz"
model = load_model(label)

if model:
    print(f"Model for {label} loaded successfully.")
else:
    print(f"Failed to load model for {label}.")

# Prediction function
def predict(features):
    features_array = np.array([features]).astype(np.float64)
    scaled_features = scaler.transform(features_array)
    if model:
        result = model.predict(scaled_features)[0]
        return result
    else:
        return 'Model not loaded'

# UI Setup
root = tk.Tk()
root.title("Shear Strength of Stainless Steel Column Web Panels")
root.configure(bg='#2E4053')  

main_title = ttk.Label(root, text="Shear Strength of Stainless Steel Column Web Panels", font=('Times New Roman', 24, 'bold'), background='#2E4053', foreground='#ECF0F1')
main_title.grid(row=0, column=0, columnspan=2, pady=(20, 10))

feature_frame = ttk.LabelFrame(root, text="Feature Inputs", padding=20, style="Custom.TLabelframe")
output_frame = ttk.LabelFrame(root, text="Model Outputs", padding=20, style="Custom.TLabelframe")
info_frame = ttk.LabelFrame(root, text="Information", padding=20, style="Custom.TLabelframe")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

feature_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
output_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
info_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

# Information text area
info_text = tk.Text(info_frame, height=4, width=50, bg='#2E4053', fg='#ECF0F1', font=('Times New Roman', 14), wrap="word")
info_content = """This GUI is developed by SINA SARFARAZI
Department of Science and Technology, University of Naples “Parthenope”, ITALY
Email: sina.srfz@gmail.com"""
info_text.insert(tk.END, info_content)
info_text.config(state=tk.DISABLED)
info_text.pack(expand=True, fill=tk.BOTH)

# Entry fields for input features
labels = ["End-plate thickness, tep(mm):", "End-plate width, bep(mm):", "End-plate height, hep(mm):",
          "Horizontal distance between bolts, gi(mm):","Spacing between bolts in tension and compression, Pi(mm):",
          "Spacing between the tension bolts, Pt(mm):", "Spacing between the compression bolts, Pc(mm):",
          "Bolt diameter, Db(mm):", "Column second moment of inertia, Ixxc(mm4):",
          "Beam second moment of inertia, Ixxb(mm4):"]
entries = [ttk.Entry(feature_frame, width=10, font=('Times New Roman', 14)) for _ in labels]

for i, (label, entry) in enumerate(zip(labels, entries)):
    col = i % 2
    row = i // 2
    ttk.Label(feature_frame, text=label, background='#2E4053', foreground='#ECF0F1', font=('Times New Roman', 14)).grid(row=row, column=col * 2, padx=10, pady=5, sticky='w')
    entry.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky='w')

# Output label for Vpz
output_label = "Vpz (kN): "
output_widget = ttk.Label(output_frame, text="", font=('Times New Roman', 14), background='#2E4053', foreground='#ECF0F1')
ttk.Label(output_frame, text=output_label, background='#2E4053', foreground='#ECF0F1', font=('Times New Roman', 14)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
output_widget.grid(row=0, column=1, padx=10, pady=5, sticky='w')

# Function to handle button click events
def submit():
    try:
        # Collect inputs
        feature_values = [float(entry.get()) for entry in entries]
        # Prediction
        result = predict(feature_values)
        # Update the output label in the GUI
        output_result = f"{result:.2f}"
        output_widget.config(text=output_result)
    except ValueError:
        messagebox.showerror("Input error", "Please check your inputs. All fields must be filled with numeric values.")

# Function to clear input and output fields
def clear_fields():
    for entry in entries:
        entry.delete(0, tk.END)
    output_widget.config(text="")

# Buttons for predictions and clearing fields
predict_button = ttk.Button(output_frame, text="Predict", command=submit, style="Custom.TButton")
predict_button.grid(row=1, column=0, padx=10, pady=5, sticky='w')

clear_button = ttk.Button(output_frame, text="Clear", command=clear_fields, style="Custom.TButton")
clear_button.grid(row=1, column=1, padx=10, pady=5, sticky='w')

# Style customization
style = ttk.Style()
style.configure("Custom.TLabelframe", background='#2E4053', foreground='#ECF0F1', bordercolor='#ECF0F1', font=('Times New Roman', 22))
style.configure("Custom.TFrame", background='#2E4053', bordercolor='#ECF0F1')
style.configure("TLabel", background='#2E4053', foreground='#ECF0F1', font=('Times New Roman', 18))
style.configure("TLabelFrame.Label", background='#2E4053', foreground='#ECF0F1', font=('Times New Roman', 18))
style.configure("Custom.TButton", background='#ECF0F1', foreground='black', font=('Times New Roman', 18))

# Main application loop
root.mainloop()





