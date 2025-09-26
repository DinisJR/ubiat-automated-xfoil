# [UBIAT](https://ubiat.aeroubi.pt/) - XFOIL Automation Script

Este projeto permite automatizar a execução do **XFOIL** para análise de perfis aerodinâmicos.  
O script em Python gera ficheiros de entrada para o XFOIL, executa simulações para diferentes números de Reynolds e agrega os resultados num único ficheiro `.txt`, pronto para análise.

## Funcionalidades

- Executa automaticamente até 10 testes de simulação com diferentes valores de Reynolds. (FUTURO: O user é que coloca o número de testes que quer fazer)
- Remove o cabeçalho padrão do XFOIL dos resultados.  
- Junta todos os testes num único ficheiro final (`resultados.txt`).  
- Inclui separadores no ficheiro final para identificar cada teste (`# Teste x - Nome do perfil - Re = ...`).  
- Resultados podem ser carregados diretamente no NumPy para pós-processamento.

## Requisitos

- Python 3.8+  
- [NumPy](https://numpy.org/)  
- XFOIL instalado e acessível pelo sistema (ex.: `xfoil.exe` no Windows ou `xfoil` no Linux/WSL).  

## Como usar

1. Coloque o ficheiro `.dat` do perfil aerodinâmico na mesma pasta do script.  
2. Configure o nome do perfil (`airfoil_name`) e outros parâmetros no script.  
3. Execute o script:  
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

Exemplo de perfil simples:

```bash
NACA 2412
1.000000 0.000000
0.950000 0.001260
0.900000 0.002510
...
0.000000 0.000000
```
