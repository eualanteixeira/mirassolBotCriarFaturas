# Bot Criar Fatura

Bot de automação (RPA) desenvolvido em Python com [BotCity Core](https://github.com/botcity-dev/botcity-framework-core), que realiza a criação de faturas no sistema Visual Rodopar com base em uma planilha Excel. O bot conecta-se ao ambiente remoto via RDP (usando o pacote `abrir_rodopar`), localiza elementos na tela por reconhecimento de imagem (pasta `resources`) e preenche os campos automaticamente.

---

## 📁 Estrutura do projeto

```
botCriarFatura/
│
├── src/
│   └── main/
│       ├── main.py                 # Ponto de entrada do bot (classe BotCriaFatura)
│       └── controle_execucao.py    # Controle de pausar/continuar/parar via hotkeys
│
├── resources/                      # Imagens usadas pelo reconhecimento visual (BotCity)
├── logs/                           # Logs gerados a cada execução (um arquivo por dia)
├── .env                            # Credenciais e caminho do RDP (não versionar)
├── requirements.txt
└── readme.md
```

---

## 🔐 Configuração do ambiente (.env)

O bot depende de um arquivo `.env` na raiz do projeto com as credenciais de acesso ao RDP, usado pelo pacote `abrir_rodopar` para abrir o Visual Rodopar automaticamente quando a tela de faturamento não é encontrada:

```
PATH_RDP=<caminho do arquivo .rdp ou host>
USUARIO_RODOPAR=<usuário de acesso>
SENHA_RODOPAR=<senha de acesso>
```

> ⚠️ Esse arquivo contém credenciais sensíveis. Ele já está listado no `.gitignore` — nunca faça commit de um `.env` com dados reais.

---

## 🧠 Requisitos da Planilha

Para que o bot funcione corretamente, a planilha de entrada deve conter as **seguintes colunas**, com os **nomes exatamente como listados abaixo** (não diferencia maiúsculas de minúsculas):

| Coluna | Uso |
|---|---|
| `FILIAL` | Filial da fatura e do CTe |
| `PAGADOR` | Código do cliente pagador |
| `OBSERVACAO` | Texto inserido no campo de observação da fatura |
| `SERIE CTE` | Série do CTe (quando a linha tem um único CTe) |
| `CTES` | Número do CTe, ou vários separados por vírgula no formato `numero-serie,numero-serie,...` |
| `DESCONTO` | Valor do desconto (`0.0` = sem desconto) |
| `SITUACAO` | Controla se a linha deve ser processada (`FATURAR` ou vazia = processa); é **atualizada pelo próprio bot** ao final (`FATURADO`, `EM VALIDAÇÃO`, `FATURA INCONSISTENTE`) |
| `FATURA` | Preenchida pelo bot com o número da duplicata gerada |
| `RESUMO` | Preenchida pelo bot com observações sobre inconsistências/erros encontrados na linha |

O bot **salva a planilha automaticamente** (sobrescrevendo o arquivo original) a cada atualização de situação, então o progresso não é perdido caso a execução seja interrompida.

Essas colunas são lidas em `src/main/main.py` através da função `pegar_valor(coluna)`.

---

## ⌨️ Controles durante a execução (hotkeys)

Ao iniciar, o bot registra atalhos globais de teclado (funcionam mesmo com o foco em outra janela) para permitir intervenção manual sem precisar fechar o processo:

| Atalho | Ação |
|---|---|
| `Ctrl + Shift + Space` | Pausa/retoma a automação (a pausa entra em vigor no próximo checkpoint, entre um CTe e outro) |
| `Ctrl + Shift + Q` | Encerra a automação de forma segura |

Cada mudança de estado dispara também uma notificação do sistema (via `plyer`) avisando que a automação foi pausada, retomada ou encerrada. A lógica está em `src/main/controle_execucao.py` (classe `ControleExecucao`).

---

## 📝 Logging

Cada execução gera um arquivo de log em `logs/botCriarFatura_AAAA-MM-DD.log`, com:

- Nível **DEBUG** no arquivo: toda ação de teclado/mouse (`pyautogui.write`, `press`, `hotkey`, `click`), todo `find()` de imagem (com resultado e tempo de busca) e toda gravação da planilha.
- Nível **INFO** no console: progresso geral (planilha carregada, linha em processamento, planilha selecionada, atalhos registrados etc).

Isso permite auditar depois exatamente o que o bot fez em cada linha da planilha, mesmo sem estar acompanhando a execução ao vivo.

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

Dependências principais: `pyautogui`, `pandas`, `botcity-framework-core`, `openpyxl`, `pyperclip`, `keyboard` (hotkeys globais) e `plyer` (notificações do sistema).

5. **Instale o `auto-py-to-exe` dentro do ambiente virtual** (opcional, apenas para gerar o `.exe`):

```bash
pip install auto-py-to-exe
```

---

## 🛠 Gerando o executável (.exe)

### Opção 1: Linha de comando (PyInstaller)

```
pyinstaller --noconfirm --onefile --console --name "Bot Criar Fatura" 
--add-data "C:\Users\automacao\Documents\botCriarFatura\resources;resources/" 
--add-data "C:\Users\automacao\Documents\botCriarFatura\.venv\Lib\site-packages\abrir_rodopar\sources;sources/" 
--add-data "C:\Users\automacao\Documents\botCriarFatura\.venv\Lib\site-packages\abrir_rodopar\hosts.json;." 
--hidden-import "abrir_rodopar" 
--hidden-import "abrir_rodopar.rdp" 
--hidden-import "abrir_rodopar.controle" 
--hidden-import "plyer" 
--hidden-import "plyer.platforms" 
--hidden-import "plyer.platforms.win.notification"  
"C:\Users\automacao\Documents\botCriarFatura\src\main\main.py"
```

> Lembre-se de colocar o arquivo `.env` na mesma pasta do `.exe` gerado, já que ele não é empacotado junto pelo PyInstaller.

### Opção 2: Interface gráfica (auto-py-to-exe)

1. No terminal, execute:
   ```bash
   auto-py-to-exe
   ```
2. No painel que abrir:
   - **Script location**: selecione `src/main/main.py`
   - **Onefile**: marque para criar um único `.exe`
   - **Console Window**: marque conforme preferência
3. Em **"Additional Files"**, adicione a pasta `resources` inteira, garantindo que ela fique na raiz do `.exe`.
4. Clique em **"Convert .py to .exe"** e aguarde o processo finalizar.

O executável será gerado na pasta `output` (ou outra definida por você).

---

## ✅ Requisitos para executar o bot

1. Ter o arquivo `.exe` gerado (ou rodar via `python src/main/main.py` em modo desenvolvimento)
2. Ter o arquivo `.env` configurado na mesma pasta, com as credenciais de RDP
3. Ter a planilha Excel com as colunas corretas (veja seção acima)
4. Garantir que as imagens estejam na pasta `resources`, na mesma pasta do `.exe`
5. Executar o `.exe` (ou o script) e selecionar a planilha na janela de seleção de arquivo que abrirá automaticamente
6. Usar `Ctrl+Shift+Space` / `Ctrl+Shift+Q` conforme necessário para pausar ou encerrar a automação

---

## 📦 Testando em modo desenvolvimento

Se quiser testar o código antes de empacotar (lembrando de ativar o ambiente virtual antes, se estiver usando):

```bash
python src/main/main.py
```
