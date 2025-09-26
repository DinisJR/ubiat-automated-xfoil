import os
import subprocess
import numpy as np
import sys

# Inputs base
airfoil_name = "ag53"
alpha_i = 0
alpha_f = 10
alpha_step = 0.25
n_iter = 100

# Lista de Reynolds para 10 testes
Re_list = [1e5, 2e5, 3e5, 4e5, 5e5, 6e5, 7e5, 8e5, 9e5, 1e6]

final_polar_file = "resultados.txt"

airfoil_file = f"{airfoil_name}.dat"
if not os.path.exists(airfoil_file):
    print(f"Erro: o ficheiro '{airfoil_file}' não foi encontrado na pasta atual.")
    sys.exit(1)

if not os.path.exists("xfoil.exe"):
    print("Erro: o ficheiro 'xfoil.exe' não foi encontrado na pasta atual.")
    sys.exit(1)

if os.path.exists(final_polar_file):
    os.remove(final_polar_file)

for i, Re in enumerate(Re_list, start=1):
    input_filename = f"input_file_{i}.in"
    temp_polar_file = f"polar_test_{i}.txt"

    if os.path.exists(temp_polar_file):
        os.remove(temp_polar_file)

    # Cria o script para o XFOIL
    with open(input_filename, 'w') as input_file:
        input_file.write(f"LOAD {airfoil_name}.dat\n")
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
    print("Todos os 10 testes concluídos e guardados em", final_polar_file)
    print("Dimensão dos dados carregados:", polar_data.shape)
except Exception as e:
    print("Erro a carregar dados:", e)

for i in range(1, 11):
    if os.path.exists(f"polar_test_{i}.txt"):
        os.remove(f"polar_test_{i}.txt")
    if os.path.exists(f"input_file_{i}.in"):
        os.remove(f"input_file_{i}.in")
