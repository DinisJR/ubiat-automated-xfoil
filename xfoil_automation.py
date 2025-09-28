# ================================================================
#  Projeto:  Automação de Testes XFOIL
#  Autor:    Dinis Jacob Ramos
#  Equipa:   UBIAT - UBI Aeronautics Team
# ================================================================

import os
import subprocess
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
import getpass

downloads_folder = os.path.join("C:\\Users", getpass.getuser(), "Downloads")
temp_folder = "temp"

# Criar pasta temp se não existir
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

def run_xfoil(airfoil_file, alpha_i, alpha_f, alpha_step, n_iter, Re_list):
    airfoil_name = os.path.splitext(os.path.basename(airfoil_file))[0]
    final_polar_file = f"resultados_{airfoil_name}.txt"

    if not os.path.exists("xfoil.exe"):
        messagebox.showerror("Erro", "O ficheiro 'xfoil.exe' não foi encontrado na pasta atual.")
        return

    if os.path.exists(final_polar_file):
        os.remove(final_polar_file)

    for i, Re in enumerate(Re_list, start=1):
        input_filename = os.path.join(temp_folder, f"input_file_{i}.in")
        temp_polar_file = os.path.join(temp_folder, f"polar_test_{i}.txt")

        if os.path.exists(temp_polar_file):
            os.remove(temp_polar_file)

        with open(input_filename, 'w') as input_file:
            input_file.write(f"LOAD {airfoil_file}\n")
            input_file.write("PANE\n")
            input_file.write("OPER\n")
            input_file.write(f"Visc {Re}\n")
            input_file.write("PACC\n")
            input_file.write(temp_polar_file + "\n\n")
            input_file.write(f"ITER {n_iter}\n")
            input_file.write(f"ASeq {alpha_i} {alpha_f} {alpha_step}\n")
            input_file.write("\n\n")
            input_file.write("quit\n")

        subprocess.call(f"xfoil.exe < {input_filename}", shell=True)

        with open(final_polar_file, 'a') as fout:
            fout.write(f"# ================================================\n")
            fout.write(f"# Teste {i} - {airfoil_name} - Re = {Re}\n")
            fout.write(f"# ================================================\n")
            with open(temp_polar_file, 'r') as fin:
                lines = fin.readlines()[12:]
                fout.writelines(lines)
            fout.write("\n\n")

    try:
        polar_data = np.loadtxt(final_polar_file, comments="#")
        print(f"Todos os {len(Re_list)} testes concluídos e guardados em {final_polar_file}")
        print(f"Dimensão dos dados carregados:", polar_data.shape)
    except Exception as e:
        messagebox.showwarning("Aviso", f"Erro a carregar dados: {e}")

    shutil.move(final_polar_file, os.path.join(downloads_folder, final_polar_file))
    messagebox.showinfo("Sucesso", f"Resultados guardados em {downloads_folder}\\{final_polar_file}")

    for f in os.listdir(temp_folder):
        os.remove(os.path.join(temp_folder, f))

# ---------------- INTERFACE TKINTER ----------------
def start_gui():
    root = tk.Tk()
    root.title("UBIAT - Automação XFOIL")
    root.geometry("1080x700")
    root.configure(bg="#121212")

    # --------- ÍCONE DA JANELA ----------
    try:
        root.iconbitmap("img/LOGO UBIAT_black-02.ico")
    except Exception:
        icon_png = tk.PhotoImage(file="img/LOGO UBIAT_black-02.png")
        root.iconphoto(False, icon_png)

    # --------- LOGO NO CENTRO ----------
    bg_img = Image.open("img/LOGO-UBIAT_white-02.png")
    bg_img = bg_img.resize((250, 250), Image.LANCZOS)
    logo = ImageTk.PhotoImage(bg_img)

    logo_label = tk.Label(root, image=logo, bg="#121212")
    logo_label.image = logo
    logo_label.pack(pady=10)

    # --------- FRAME PRINCIPAL ----------
    card = tk.Frame(root, bg="#1E1E1E", bd=0, relief="flat")
    card.pack(pady=20, padx=20, fill="x")

    font_labels = ("Segoe UI", 11, "bold")
    font_entry = ("Consolas", 11)

    def choose_file():
        file_path = filedialog.askopenfilename(filetypes=[("Airfoil files", "*.dat")])
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

    def add_row(row, label, default="", width=20):
        tk.Label(card, text=label, bg="#1E1E1E", fg="white", font=font_labels, anchor="e", width=36)\
            .grid(row=row, column=0, sticky="e", padx=10, pady=6)
        entry = tk.Entry(card, font=font_entry, bg="#2C2C2C", fg="white",
                         insertbackground="white", width=width, relief="flat")
        entry.insert(0, default)
        entry.grid(row=row, column=1, sticky="w", padx=10, pady=6, ipadx=5, ipady=3)
        return entry

    # --------- CAMPOS ----------
    btn_file = tk.Button(card, text="📂 Escolher Perfil (.dat)", command=choose_file,
                         bg="#2C2C2C", fg="white", font=("Segoe UI", 10, "bold"),
                         relief="flat", activebackground="#3C3C3C", activeforeground="white")
    btn_file.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    entry_file = tk.Entry(card, width=50, font=font_entry, bg="#2C2C2C", fg="white", relief="flat")
    entry_file.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    entry_ai   = add_row(1, "Ângulo de ataque inicial (alpha_i)", "0")
    entry_af   = add_row(2, "Ângulo de ataque final (alpha_f)", "10")
    entry_step = add_row(3, "Incremento do ângulo (alpha_step)", "0.25")
    entry_iter = add_row(4, "Nº máximo de iterações (n_iter)", "100")
    entry_re   = add_row(5, "Números de Reynolds (separados por vírgula)", "1e5, 2e5, 3e5, 4e5, 5e5, 6e5, 7e5, 8e5, 9e5, 1e6", width=50)

    # --------- EXECUTAR ----------
    def execute():
        airfoil_file = entry_file.get()
        if not os.path.exists(airfoil_file):
            messagebox.showerror("Erro", "Escolha um ficheiro .dat válido.")
            return
        try:
            Re_list = [float(x.strip()) for x in entry_re.get().split(",") if x.strip()]
            run_xfoil(
                airfoil_file,
                float(entry_ai.get()),
                float(entry_af.get()),
                float(entry_step.get()),
                int(entry_iter.get()),
                Re_list
            )
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    btn_exec = tk.Button(root, text="🚀 Executar", command=execute,
                         bg="#28A745", fg="white", font=("Segoe UI", 13, "bold"),
                         relief="flat", activebackground="#34D058", activeforeground="black")
    btn_exec.pack(pady=20, ipadx=25, ipady=12)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
