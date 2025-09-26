import os
import subprocess
import numpy as np

# Inputs base
airfoil_name = "ag53"
alpha_i = 0
alpha_f = 10
alpha_step = 0.25
n_iter = 100

# Lista de Reynolds para 10 testes
Re_list = [1e5, 2e5, 3e5, 4e5, 5e5, 6e5, 7e5, 8e5, 9e5, 1e6]

# Nome do ficheiro final
final_polar_file = "resultados.txt"

# Apagar o ficheiro final se já existir
if os.path.exists(final_polar_file):
    os.remove(final_polar_file)

# Loop para os 10 testes
for i, Re in enumerate(Re_list, start=1):
    input_filename = f"input_file_{i}.in"
    temp_polar_file = f"polar_test_{i}.txt"

    # Apagar polar temporário se já existir
    if os.path.exists(temp_polar_file):
        os.remove(temp_polar_file)

    # Criar script para o XFOIL
    with open(input_filename, 'w') as input_file:
        input_file.write(f"LOAD {airfoil_name}.dat\n")
        input_file.write("PANE\n")
        input_file.write("OPER\n")
        input_file.write(f"Visc {Re}\n")
        input_file.write("PACC\n")
        input_file.write(temp_polar_file + "\n\n")  # cada teste escreve no seu ficheiro
        input_file.write(f"ITER {n_iter}\n")
        input_file.write(f"ASeq {alpha_i} {alpha_f} {alpha_step}\n")
        input_file.write("\n\n")
        input_file.write("quit\n")

    # Correr XFOIL
    subprocess.call(f"xfoil.exe < {input_filename}", shell=True)

    # Escrever no ficheiro final com separador e sem cabeçalho do XFOIL
    with open(final_polar_file, 'a') as fout:
        fout.write(f"# ================================================\n")
        fout.write(f"# Teste {i} - {airfoil_name} - Re = {Re}\n")
        fout.write(f"# ================================================\n")
        with open(temp_polar_file, 'r') as fin:
            lines = fin.readlines()[12:]  # ignora cabeçalho do XFOIL
            fout.writelines(lines)
        fout.write("\n\n")

# Agora podes carregar diretamente no NumPy (vai ignorar as linhas que começam com '#')
try:
    polar_data = np.loadtxt(final_polar_file, comments="#")
    print("Todos os 10 testes concluídos e guardados em", final_polar_file)
    print("Dimensão dos dados carregados:", polar_data.shape)
except Exception as e:
    print("Erro a carregar dados:", e)

for i in range(1, 11):
    os.remove(f"polar_test_{i}.txt")
    os.remove(f"input_file_{i}.in")
