# Guia de Execução do Projeto REPADEL

Este documento descreve o procedimento necessário para executar o projeto de treinamento do modelo REPADEL utilizando PyCaret em ambiente local. O processo envolve a criação de um ambiente virtual (venv), instalação das dependências do projeto e uso da extensão Jupyter no Visual Studio Code para execução dos notebooks ou scripts interativos.

---

## 📌 Pré-requisitos

Antes de iniciar a execução, certificar-se de ter instalado:

* **Python 3.10.11**
* **Visual Studio Code**
* **Extensão Jupyter para VS Code** (`ms-toolsai.jupyter`)
* **Extensão Python para VS Code** (`ms-python.python`)

---

## 📁 Estrutura Relevante do Projeto

```
PyCaret/
├── Treinamento com dados brutos/
└── Treinamento com dados tratados/

requirements.txt
```

As pastas contêm os arquivos utilizados durante o treinamento do modelo no PyCaret.

---

## 🧱 1. Criar o Ambiente Virtual (venv)

Dentro da pasta do projeto, executar no terminal:

```
py -3.10 -m venv venv
```

---

## ▶️ 2. Ativar o Ambiente Virtual

### Windows (PowerShell ou Git Bash)

```
source venv/Scripts/activate
```

### Windows (CMD)

```
venv\Scripts\activate
```

Verificar a versão ativa:

```
python --version
```

Deve retornar uma versão **3.10.11**.

---

## 📦 3. Instalar as Dependências

Com a venv ativada, executar:

```
pip install -r requirements.txt
```

Esse arquivo contém todas as bibliotecas necessárias, incluindo:

* PyCaret
* Pandas
* Numpy
* Scikit-learn
* Bibliotecas auxiliares para o PyCaret
* Jupyter / IPykernel

---

## 📓 4. Usar o Jupyter pelo VS Code ou Optar por inserir os arquivos no Google Colab

Para execução dos arquivos de treinamento (notebooks ou scripts interativos), é necessário:

* Abrir o **VS Code**
* Garantir que a extensão **Jupyter** está instalada
* Abrir o notebook ou script do PyCaret
* No canto superior direito, selecionar o **Kernel**
* Escolher o kernel correspondente ao ambiente virtual:

```
Python 3.10 (venv)
```

O VS Code utilizará essa venv para executar o código.

---

## ▶️ 5. Executar o Treinamento

A partir desse ponto, basta:

* Navegar até a pasta desejada:

  * *Treinamento com dados brutos*
  * *Treinamento com dados tratados*
* Abrir o notebook ou script Python
* Executar célula por célula (Shift+Enter)

O PyCaret iniciará o processo de análise, preparação de dados e treinamento do modelo conforme definido no projeto.

---
