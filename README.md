<div align="center">
  <img src="img/LOGO-UBIAT_white-02.png" width="300">
</div>

# [UBIAT](https://ubiat.aeroubi.pt/) - XFOIL Automation Script

Este projeto permite automatizar a execução do **XFOIL** para análise de perfis aerodinâmicos.  
O script em Python gera ficheiros de entrada para o XFOIL, executa simulações para diferentes números de Reynolds e agrega os resultados num único ficheiro `.txt`, pronto para análise.

## Funcionalidades

- Interface gráfica para seleção do ficheiro `.dat` do perfil.  
- Definição dos parâmetros de análise:
  - Ângulo inicial, final e passo (alpha_i, alpha_f, alpha_step).  
  - Número máximo de iterações (n_iter).  
  - Lista de valores de Reynolds definida pelo utilizador.  
- Geração automática de ficheiros temporários na pasta `/temp`.  
- Consolidação de todos os resultados num único ficheiro `resultados_<perfil>.txt`.  
- Exportação automática do ficheiro final para a pasta **Transferências** do Windows.  
- Cabeçalhos do XFOIL removidos para facilitar o pós-processamento.  

### Futuras Funcionalidades

- Calcular o valor de Reynolds com os parâmetros do user.

## Requisitos

- [Python 3.8+](https://www.python.org/downloads/)  
- [NumPy](https://numpy.org/)  
- [Pillow (PIL)](https://pypi.org/project/pillow/)  
- **Tkinter** (vem incluído por defeito no Python para Windows).  
- **XFOIL** instalado e acessível (ex.: `xfoil.exe` na mesma pasta do programa).  

## Como usar

1. Instalar as dependências
2. Executar o script:  
   ```bash
   python xfoil_automation.py

## Formato dos Ficheiros de Perfil

Os perfis aerodinâmicos devem estar em ficheiros `.dat` com o seguinte formato: 

```bash
NOME_DO_PERFIL
x1 y1
x2 y2
x3 y3
...
xn yn
```

- A primeira linha contém apenas o nome do perfil.  
- As linhas seguintes contêm as coordenadas normalizadas do bordo de ataque até ao bordo de fuga (x, y).  
- O formato mais comum é o disponibilizado pela **UIUC Airfoil Database**.  
- Certifique-se de que o ficheiro não contém colunas extra, cabeçalhos ou separadores diferentes de espaço/tabulação.  

Exemplo de um perfil:

```bash
NACA 2412
1.000000 0.000000
0.950000 0.001260
0.900000 0.002510
...
0.000000 0.000000
```
