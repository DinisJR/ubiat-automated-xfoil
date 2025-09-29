# ================================================================
#  Projeto:  Automação de Testes XFOIL
#  Autor:    Dinis Jacob Ramos
#  Equipa:   UBIAT - UBI Aeronautics Team
# ================================================================

import os
import subprocess
import numpy as np
import tkinter as tk
import shutil
import getpass
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime

downloads_folder = os.path.join("C:\\Users", getpass.getuser(), "Downloads")
temp_folder = "temp"

if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

def run_xfoil(airfoil_file, alpha_i, alpha_f, alpha_step, n_iter, Re_list):
    airfoil_name = os.path.splitext(os.path.basename(airfoil_file))[0]
    final_polar_file = f"resultados_{airfoil_name}_{datetime.now().strftime('%Y-%m__%H-%M-%S')}.txt"

    if not os.path.exists("xfoil.exe"):
        messagebox.showerror("Erro", "O ficheiro 'xfoil.exe' não foi encontrado na pasta atual.")
        return

    if os.path.exists(final_polar_file):
        os.remove(final_polar_file)

    try:
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

            ret = subprocess.call(f"xfoil.exe < {input_filename}", shell=True)
            if ret != 0:
                messagebox.showerror("Erro", f"Falha ao executar XFOIL (código {ret}).")
                return
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

        destino = os.path.join(downloads_folder, final_polar_file)
        shutil.move(final_polar_file, destino)
        messagebox.showinfo("Sucesso", f"Resultados guardados em {destino}")

        try:
            os.startfile(downloads_folder)
        except:
            pass

    finally:
        for f in os.listdir(temp_folder):
            os.remove(os.path.join(temp_folder, f))


# ------------------ INTERFACE ------------------
def start_gui():
    root = tk.Tk()
    root.title("UBIAT - Automação XFOIL")
    root.geometry("1060x820")
    root.configure(bg="#0D1117")  

    try:
        root.iconbitmap("img/LOGO UBIAT_black-02.ico")
    except Exception:
        try:
            icon_png = tk.PhotoImage(file="img/LOGO UBIAT_black-02.png")
            root.iconphoto(False, icon_png)
        except:
            pass

    # --------- LOGO + TÍTULO ----------
    bg_img = Image.open("img/LOGO-UBIAT_white-02.png").resize((200, 200), Image.LANCZOS)
    logo = ImageTk.PhotoImage(bg_img)
    logo_label = tk.Label(root, image=logo, bg="#0D1117")
    logo_label.image = logo
    logo_label.pack(pady=(30, 10))

    title = tk.Label(root, text="Automação de Testes XFOIL",
                     bg="#0D1117", fg="white",
                     font=("Segoe UI", 20, "bold"))
    title.pack()

    subtitle = tk.Label(root, text="UBI Aeronautics Team",
                        bg="#0D1117", fg="#AAAAAA",
                        font=("Segoe UI", 12))
    subtitle.pack(pady=(0, 20))

    # --------- CARD PRINCIPAL ----------
    card = tk.Frame(root, bg="#161B22", bd=0, relief="flat", highlightthickness=1, highlightbackground="#30363D")
    card.pack(padx=40, pady=10, fill="x")

    font_labels = ("Segoe UI", 11, "bold")
    font_entry = ("Consolas", 11)

    def choose_file():
        file_path = filedialog.askopenfilename(filetypes=[("Airfoil files", "*.dat")])
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

    def add_row(row, label, default="", width=20):
        tk.Label(card, text=label, bg="#161B22", fg="white", font=font_labels, anchor="e", width=36)\
            .grid(row=row, column=0, sticky="e", padx=10, pady=8)
        entry = tk.Entry(card, font=font_entry, bg="#0D1117", fg="white",
                         insertbackground="white", width=width, relief="flat",
                         highlightthickness=1, highlightbackground="#30363D")
        entry.insert(0, default)
        entry.grid(row=row, column=1, sticky="w", padx=10, pady=8, ipadx=6, ipady=4)
        return entry

    # --------- CAMPOS ----------
    btn_file = tk.Button(card, text="📂 Escolher Perfil (.dat)", command=choose_file,
                         bg="#238636", fg="white", font=("Segoe UI", 10, "bold"),
                         relief="flat", activebackground="#2EA043", activeforeground="white",
                         padx=10, pady=6, cursor="hand2")
    btn_file.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    entry_file = tk.Entry(card, width=50, font=font_entry, bg="#0D1117", fg="white",
                          relief="flat", highlightthickness=1, highlightbackground="#30363D")
    entry_file.grid(row=0, column=1, padx=10, pady=10, sticky="w", ipadx=6, ipady=4)

    entry_ai   = add_row(1, "Ângulo de ataque inicial (alpha_i)", "0")
    entry_af   = add_row(2, "Ângulo de ataque final (alpha_f)", "10")
    entry_step = add_row(3, "Incremento do ângulo (alpha_step)", "0.25")
    entry_iter = add_row(4, "Nº máximo de iterações (n_iter)", "100")
    entry_re   = add_row(5, "Números de Reynolds (separados por vírgula)",
                         "1e5, 2e5, 3e5, 4e5, 5e5, 6e5, 7e5, 8e5, 9e5, 1e6", width=50)

    # --------- BOTÃO EXECUTAR ----------
    def execute():
        airfoil_file = entry_file.get()
        if not os.path.exists(airfoil_file) or not airfoil_file.endswith(".dat"):
            messagebox.showerror("Erro", "Escolha um ficheiro .dat válido.")
            return

        try:
            ai = float(entry_ai.get())
            af = float(entry_af.get())
            step = float(entry_step.get())
            n_iter = int(entry_iter.get())
        except ValueError:
            messagebox.showerror("Erro", "Os campos de ângulos e iterações devem ser numéricos.")
            return

        if step <= 0:
            messagebox.showerror("Erro", "O incremento do ângulo (alpha_step) deve ser positivo.")
            return
        if af <= ai:
            messagebox.showerror("Erro", "O ângulo final deve ser maior que o inicial.")
            return
        if n_iter <= 0:
            messagebox.showerror("Erro", "O número de iterações deve ser positivo.")
            return

        try:
            Re_list = [float(x.strip()) for x in entry_re.get().split(",") if x.strip()]
        except ValueError:
            messagebox.showerror("Erro", "A lista de Reynolds deve conter apenas números separados por vírgulas.")
            return

        run_xfoil(airfoil_file, ai, af, step, n_iter, Re_list)

    btn_exec = tk.Button(root, text="🚀 Executar", command=execute,
                         bg="#238636", fg="white", font=("Segoe UI", 14, "bold"),
                         relief="flat", activebackground="#2EA043", activeforeground="black",
                         padx=25, pady=12, cursor="hand2")
    btn_exec.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
