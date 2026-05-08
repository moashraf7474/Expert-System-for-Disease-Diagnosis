import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

# ==================================================
# LOAD PROLOG
# ==================================================
prolog = Prolog()
prolog.consult("expert_system.pl")

# ==================================================
# FIXED SYMPTOMS LIST (UPDATED)
# ==================================================
symptoms = [
    "blurred_vision",
    "body_aches",
    "chest_pain",
    "chest_tightness",
    "chills",
    "cold_hands",
    "congestion",
    "cough",
    "diarrhea",
    "difficulty_breathing",
    "dizziness",
    "dry_cough",
    "excessive_thirst",
    "fatigue",
    "fever",
    "frequent_urination",
    "headache",
    "high_fever",
    "loss_of_smell",
    "loss_of_taste",
    "mild_cough",
    "nausea",
    "nosebleed",
    "pale_skin",
    "runny_nose",
    "sensitivity_to_light",
    "sensitivity_to_sound",
    "severe_headache",
    "shortness_of_breath",
    "slow_healing",
    "sneezing",
    "sore_throat",
    "stomach_cramps",
    "sweating",
    "vomiting",
    "wheezing"
]

# ==================================================
# MAIN WINDOW
# ==================================================
root = tk.Tk()
root.title("Disease Diagnosis Expert System - AI406")
root.geometry("1050x720")
root.config(bg="#0f172a")

TITLE_FONT = ("Segoe UI", 24, "bold")
TEXT_FONT = ("Segoe UI", 11)
BTN_FONT = ("Segoe UI", 11, "bold")

# ==================================================
# HEADER
# ==================================================
header = tk.Frame(root, bg="#111827", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="Disease Diagnosis Expert System",
    font=TITLE_FONT,
    fg="white",
    bg="#111827"
).pack(side="left", padx=25, pady=20)

tk.Label(
    header,
    text="AI406 - Pharos University",
    font=("Segoe UI", 10),
    fg="#9ca3af",
    bg="#111827"
).pack(side="right", padx=20)

# ==================================================
# MAIN
# ==================================================
main = tk.Frame(root, bg="#0f172a")
main.pack(fill="both", expand=True, padx=15, pady=15)

# ==================================================
# LEFT PANEL
# ==================================================
left = tk.Frame(main, bg="#111827")
left.pack(side="left", fill="y", padx=(0, 10))

tk.Label(
    left,
    text="Select Symptoms",
    font=("Segoe UI", 16, "bold"),
    fg="white",
    bg="#111827"
).pack(pady=10)

canvas = tk.Canvas(left, bg="#111827", highlightthickness=0, width=360, height=500)
scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg="#111827")

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left")
scrollbar.pack(side="right", fill="y")

# ==================================================
# CHECKBOXES
# ==================================================
symptom_vars = {}

for s in symptoms:
    var = tk.BooleanVar()

    tk.Checkbutton(
        scroll_frame,
        text=s.replace("_", " ").title(),
        variable=var,
        bg="#111827",
        fg="white",
        activebackground="#111827",
        activeforeground="white",
        selectcolor="#1f2937",
        font=TEXT_FONT
    ).pack(anchor="w", padx=10, pady=2)

    symptom_vars[s] = var

# ==================================================
# RIGHT PANEL
# ==================================================
right = tk.Frame(main, bg="#111827")
right.pack(side="right", fill="both", expand=True)

tk.Label(
    right,
    text="Diagnosis Results",
    font=("Segoe UI", 16, "bold"),
    fg="white",
    bg="#111827"
).pack(pady=10)

result_box = tk.Text(
    right,
    wrap="word",
    font=("Consolas", 11),
    bg="#0b1220",
    fg="white",
    insertbackground="white",
    bd=0
)
result_box.pack(fill="both", expand=True, padx=15, pady=10)

# ==================================================
# FUNCTIONS
# ==================================================
def diagnose():
    selected = [s for s, v in symptom_vars.items() if v.get()]

    if not selected:
        messagebox.showwarning("No Symptoms", "Please select at least one symptom.")
        return

    result_box.delete("1.0", tk.END)

    query = f"diagnose({selected}, Disease, Score)"
    results = list(prolog.query(query))

    if not results:
        result_box.insert(tk.END, "No matching disease found.")
        return

    result_box.insert(tk.END, "Selected Symptoms:\n")
    result_box.insert(tk.END, ", ".join(s.replace("_", " ").title() for s in selected))
    result_box.insert(tk.END, "\n\n" + "=" * 50 + "\n\n")

    for r in results:
        disease = r["Disease"]
        score = r["Score"]

        treatment = list(prolog.query(f"get_treatment({disease}, T)"))[0]["T"]

        result_box.insert(tk.END, f"Disease: {disease.replace('_',' ').title()}\n")
        result_box.insert(tk.END, f"Score: {score}\n")
        result_box.insert(tk.END, f"Treatment: {treatment}\n")
        result_box.insert(tk.END, "-" * 50 + "\n")

def clear_all():
    for v in symptom_vars.values():
        v.set(False)
    result_box.delete("1.0", tk.END)

# ==================================================
# BUTTONS
# ==================================================
btn_frame = tk.Frame(left, bg="#111827")
btn_frame.pack(pady=10)

tk.Button(
    btn_frame,
    text="✓ Diagnose",
    command=diagnose,
    bg="#3b82f6",
    fg="white",
    font=BTN_FONT,
    width=24,
    relief="flat",
    pady=10
).pack(pady=5)

tk.Button(
    btn_frame,
    text="✕ Clear All",
    command=clear_all,
    bg="#ef4444",
    fg="white",
    font=BTN_FONT,
    width=24,
    relief="flat",
    pady=10
).pack(pady=5)

# ==================================================
# RUN
# ==================================================
root.mainloop()