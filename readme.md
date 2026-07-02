# Gerar .exe via auto-py-to-exe

```
pyinstaller --noconfirm --onefile --console --name "Criar Fatura" --add-data "C:\Users\automacao\Documents\botCriarFatura\resources;resources/" --hidden-import "abrir_rodopar" --hidden-import "abrir_rodopar.rdp" --hidden-import "abrir_rodopar.controle" --add-data "C:\Users\automacao\Documents\botCriarFatura\.venv\Lib\site-packages\abrir_rodopar\sources;sources/" --add-data "C:\Users\automacao\Documents\botCriarFatura\.venv\Lib\site-packages\abrir_rodopar\hosts.json;." --hidden-import "plyer" --hidden-import "plyer.platforms" --hidden-import "plyer.platforms.win.notification"  "C:\Users\automacao\Documents\botCriarFatura\bot.py"
```




# Bot de Automação com BotCity

Este projeto é um bot desenvolvido em Python usando a biblioteca [BotCity Core](https://github.com/botcity-dev/botcity-framework-core), que realiza ações automatizadas com base nos dados de uma planilha Excel. A automação depende de imagens contidas na pasta `resources`.

---

## 📁 Estrutura esperada do projeto
```
seu-projeto/
│
├── bot.py
├── requirements.txt
├── README.md
└── resources/
    ├── abaDocumentos.png
    ├── desconto.png
    └── ...
```

---

## 🧠 Requisitos da Planilha

Para que o bot funcione corretamente, a planilha de entrada deve conter as **seguintes colunas**, com os **nomes exatamente como listados abaixo** (não diferencia maiúsculas de minúsculas):

- `Filial`
- `PAGADOR`
- `OBSERVACAO`
- `SERIE CTE`
- `CTES`
- `DESCONTO`

Essas colunas são usadas nas seguintes variáveis do código:

```python
filFat = pegar_valor('Filial')
codPag = pegar_valor('PAGADOR')
obs    = pegar_valor('OBSERVACAO')
filCTe = pegar_valor('Filial')
serCTe = pegar_valor('SERIE CTE')
numCTe = pegar_valor('CTES')
desc   = pegar_valor('DESCONTO')
```
Por isso, os nomes das colunas precisam estar exatamente iguais aos nomes no código.

---

## 🐍 Criando um Ambiente Virtual Python (Recomendado)

Para manter seu projeto organizado e evitar conflitos com outros pacotes do sistema, é **recomendado criar um ambiente virtual** Python antes de instalar as dependências.

### Passo a passo:

1. **Abra o terminal na pasta do projeto**

2. **Crie o ambiente virtual** (apenas uma vez):

```bash
python -m venv NomeDoVenv
```

3. **Ative o ambiente virtual**:

- No **Windows**:
  ```bash
  NomeDoVenv\Scripts\activate
  ```

- No **Linux/macOS**:
  ```bash
  source NomeDoVenv/bin/activate
  ```

> Você saberá que está ativado porque o nome `(venv)` aparecerá antes do cursor no terminal.

4. **Instale as dependências do projeto**:

```bash
pip install -r requirements.txt
```

5. **Instale o `auto-py-to-exe` dentro do ambiente virtual**:

```bash
pip install auto-py-to-exe
```

---

## 🛠 Como transformar em executável com auto-py-to-exe

### 1. Execute o `auto-py-to-exe`

No terminal:

```bash
auto-py-to-exe
```

### 2. Configure a interface

No painel que abrir:

- **Script location**: selecione o arquivo `bot.py`
- **Onefile**: marque para criar um único `.exe`
- **Console Window**:
  - Marque Window Based se estiver marcado.

### 3. Adicione a pasta `resources`

1. Clique em **"Add Files"** ou **"Add Folder"** no painel "Additional Files"
2. Adicione a **pasta `resources` inteira**
3. Certifique-se de que ela será incluída na raiz do `.exe`, mantendo a estrutura correta

### 4. Converter

Clique em **"Convert .py to .exe"** e aguarde o processo finalizar.

O executável será gerado na pasta `output` (ou outra definida por você).

---

## ✅ Requisitos para executar o bot

1. Ter o arquivo `bot.exe` gerado
2. Ter a planilha Excel com as colunas corretas (veja seção acima)
3. Garantir que as imagens estejam na pasta `resources`, na mesma pasta do `.exe`
4. Executar o `.exe` com duplo clique ou pelo terminal

---

## 📦 Dica para ambiente Python antes da conversão

Se quiser testar o código em modo desenvolvimento antes de empacotar:

```bash
python bot.py
```

(lembrando de ativar o ambiente virtual antes, se estiver usando)


