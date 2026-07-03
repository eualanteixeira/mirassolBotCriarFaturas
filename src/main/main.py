import pyautogui
import re
import time
import pandas
import pyperclip
from datetime import datetime
from botcity.core import DesktopBot
import tkinter as tk
from tkinter import filedialog
from abrir_rodopar.rdp import main as abrir_vr

# Cria uma janela oculta (só para não mostrar a janela raiz)
root = tk.Tk()
root.withdraw()

# Abre o seletor de arquivos
caminho_arquivo = filedialog.askopenfilename(title="Selecione a Planilha: ")

class BotCriaFatura(DesktopBot):
    def __init__(self):
        super().__init__()
        self.abrir_rodopar = abrir_vr

    def main(self,):

        rodopar_aberto = self.find( "faturamento", matching=0.97, waiting_time=5000)
        if not rodopar_aberto:
            abrir_vr()

        if self.find( "faturamento", matching=0.97, waiting_time=20000):
            self.click()
            time.sleep(0.5)
            pyautogui.hotkey('alt','v')
            pyautogui.hotkey('alt','v')
            pyautogui.hotkey('alt','v')
            pyautogui.hotkey('alt','v')
            pyautogui.hotkey('alt','v')

        #Ler a lista de faturas a extrair
        listaCTes = pandas.read_excel(caminho_arquivo, dtype={'FATURA': str, 'SITUACAO': str, 'RESUMO': str})

        if self.find( "faturamento", matching=0.97, waiting_time=20000):
            for CTes in range(len(listaCTes)):

                numero_duplicata_principal = 0

                def pegar_valor(coluna):
                    try:
                        valor = listaCTes[coluna][CTes]
                        # se for NaN (célula vazia), devolve string vazia
                        if pandas.isna(valor):
                            return ""
                        return str(valor).strip() 
                    except Exception as e:
                        pyautogui.alert(f"Erro ao acessar a coluna '{coluna}'. Verifique se ela existe na planilha.")
                        raise e


                #Alimentando as variaveis
                filFat = pegar_valor('FILIAL')
                codPag = pegar_valor('PAGADOR')
                obs    = pegar_valor('OBSERVACAO')
                filCTe = pegar_valor('FILIAL')
                serCTe = pegar_valor('SERIE CTE')
                numCTe = pegar_valor('CTES')
                desc   = pegar_valor('DESCONTO')
                situac = pegar_valor('SITUACAO')
                # fatura = pegar_valor('FATURA')
                resumo = pegar_valor('RESUMO')

                if situac == "FATURAR" or situac == "":

                #Abrindo o ambiente da fatura
                    if self.find( "faturamento", matching=0.97, waiting_time=20000):
                        self.click()

                        if self.find( "Movimentacao", matching=0.97, waiting_time=5000):
                            self.click()

                            if self.find( "fatura_Duplicata", matching=0.97, waiting_time=5000):
                                self.click()

                                #Clicando na filial para inserir a filial da fatura
                                if self.find( "filialFatura", matching=0.97, waiting_time=5000):
                                    self.click_relative(55, 33)

                                    #Digitando o código da filial
                                    pyautogui.write(filFat)

                                    #Apertando o enter 2x
                                    pyautogui.press('enter')
                                    pyautogui.press('enter')

                                    #Confirmando se deu certo através da fatura inconsistente
                                    if self.find( "faturaInconsistente", matching=0.97, waiting_time=5000):

                                        #Clicar no codigo cliente (pagador)
                                        if self.find( "Cliente_pagador", matching=0.97, waiting_time=5000):
                                            self.click_relative(95, 37)

                                            #Digitar o código do cliente
                                            pyautogui.write(codPag)

                                            #Apertar o enter 1x
                                            pyautogui.press('enter')
                                            # pyautogui.press('tab') # A SER VALIDADO
                                            # pyautogui.write("19") # A SER VALIDADO

                                            #Confirmando se os dados entrou através da Tarefa
                                            if self.find( "tarefa", matching=0.97, waiting_time=5000):

                                                #Clicar em observação
                                                if self.find( "obsFatura", matching=0.97, waiting_time=5000):
                                                    self.click_relative(90, 72)

                                                    #Inserir a observação
                                                    pyautogui.write(obs)

                                                    #Clicar em salvar
                                                    if self.find( "salvar", matching=0.97, waiting_time=5000):
                                                        self.click()

                                                        if self.find( "numeroDuplicata", matching=0.97, waiting_time=5000):
                                                            self.double_click_relative(x=80, y=10) 
                                                            numero_duplicata_principal = pyautogui.hotkey('ctrl','c')
                                                            numero_duplicata_principal = pyperclip.paste()
                                                            print(numero_duplicata_principal)
                                                            duplicata = pyperclip.paste()

                                                        #Ir para aba documentos
                                                        if self.find( "abaDocumentos", matching=0.97, waiting_time=5000):
                                                            self.click()

                                                        #Clicar na pastinha
                                                            if ',' in numCTe:
                                                                lista_CTES =  numCTe.split(',')
                                                                
                                                                inconsistencia = 0

                                                                for numero_str in lista_CTES:

                                                                    quantidade_cte = len(lista_CTES)

                                                                    
                                                                    if self.find( "pastaNovoDoc", matching=0.97, waiting_time=5000) or self.find( "pastaNovoDoc1", matching=0.97, waiting_time=5000):
                                                                        self.click()
                                                                        #Apertar tab
                                                                        pyautogui.press('tab')

                                                                        #Digitar a filial do CTe
                                                                        pyautogui.write(filCTe)

                                                                        #Apertar enter
                                                                        pyautogui.press('enter')

                                                                        #Digitar a série
                                                                        numeroCTe, serieCTe = numero_str.split('-')

                                                                        pyautogui.write(serieCTe)

                                                                        #Apertar enter
                                                                        pyautogui.press('enter')
                                                                
                                                                        #Digitar o número do CTe
                                                                        pyautogui.write(numeroCTe)

                                                                        #Apertar enter 2x
                                                                        pyautogui.press('enter')
                                                                        pyautogui.press('enter')


                                                                        if self.find( "documentoJaFaturado", matching=0.97, waiting_time=5000):

                                                                            self.click()
                                                                            time.sleep(0.5)
                                                                            duplicata = pyautogui.hotkey('ctrl', 'c')
                                                                            time.sleep(0.5)
                                                                            duplicata = pyperclip.paste()

                                                                            linhas_uteis = [l.strip() for l in duplicata.splitlines() if l.strip() and not l.strip().startswith('---')]
                                                                            
                                                                            mensagem = linhas_uteis[1]
                                                                            match = re.search(r'\[(\d+)\]', mensagem)

                                                                            if match:
                                                                                numero_duplicata = match.group(1)

                                                                                print(f"Duplicata gerada: {numero_duplicata}")

                                                                            resumo = resumo + f"Documento: {numeroCTe} esta na Fatura: {numero_duplicata} \n"

                                                                            listaCTes.at[CTes, 'SITUACAO'] = "EM VALIDAÇÃO" 
                                                                            listaCTes.at[CTes, 'RESUMO'] = resumo
                                                                            listaCTes.to_excel(caminho_arquivo, index=False)

                                                                            pyautogui.press('enter')

                                                                            time.sleep(0.5)

                                                                            if self.find( "cancelarRegistroDocumento", matching=0.97, waiting_time=5000):
                                                                                self.click()
                                                                                time.sleep(0.5)

                                                                            inconsistencia += 1

                                                                            continue

                                                                        if self.find( "cteNaoAutorizado", matching=0.97, waiting_time=5000):
                                                                            self.click()
                                                                            time.sleep(0.5)
                                                                            
                                                                            if resumo == "":
                                                                                resumo = f"Documento: {numeroCTe} não autorizado. \n"
                                                                            else:
                                                                                resumo = resumo + f"Documento: {numeroCTe} não autorizado. \n"

                                                                            listaCTes.at[CTes, 'SITUACAO'] = "EM VALIDAÇÃO"
                                                                            listaCTes.at[CTes, 'RESUMO'] = resumo
                                                                            listaCTes.to_excel(caminho_arquivo, index=False)

                                                                            pyautogui.press('enter')

                                                                            time.sleep(0.5)

                                                                            if self.find( "cancelarRegistroDocumento", matching=0.97, waiting_time=5000):
                                                                                self.click()
                                                                                time.sleep(0.5)

                                                                            inconsistencia += 1

                                                                            continue
                                                                        
                                                                        if inconsistencia == 0: 
                                                                            situacao_fatura = "FATURADO"
                                                                        else:
                                                                            situacao_fatura = "FATURA INCONSISTENTE"

                                                                        listaCTes.at[CTes, 'SITUACAO'] = situacao_fatura 
                                                                        listaCTes.at[CTes, 'FATURA'] = numero_duplicata_principal
                                                                        listaCTes.to_excel(caminho_arquivo, index=False)    
                                                                            
                                                                        pyautogui.click(514,399)
                                                                        time.sleep(2)

                                                                if inconsistencia > 0:

                                                                    if inconsistencia == quantidade_cte:
                                                                        listaCTes.at[CTes, 'SITUACAO'] = "FATURA INCONSISTENTE" 
                                                                        listaCTes.to_excel(caminho_arquivo, index=False)

                                                                        if self.find( "excluir", matching=0.97, waiting_time=5000):
                                                                                    self.click()
                                                                                    time.sleep(0.5)
                                                                                    if self.find( "excluirRegistroPermanente", matching=0.97, waiting_time=5000):
                                                                                        if self.find( "Yes", matching=0.97, waiting_time=5000):
                                                                                            self.click()
                                                                                            time.sleep(0.5)
                                                                                            pyautogui.hotkey('alt','v')

                                                                    inconsistencia = 0
                                                                    pyautogui.hotkey('alt','v')

                                                                    continue

                                                                else:
                                                                        
                                                                    #Confirmar se entrou buscando o 1 de 1
                                                                    if self.find("confirmacao_Doc_Inserido2", matching=0.97, waiting_time=5000):

                                                                            #Estrutura de decisão para inserir o desconto somente se houver
                                                                            if desc != '0.0':
                                                                                #Clicando no campo para inserir o desconto
                                                                                if self.find( "desconto", matching=0.97, waiting_time=5000):
                                                                                    self.click_relative(153, 5)

                                                                                    #Digitando o valor do desconto
                                                                                    pyautogui.write(str(desc).replace('.',','))

                                                                                    #Apertar enter 1x
                                                                                    pyautogui.press('enter')

                                                                            #Efetuar a fatura através o atalho (F8)
                                                                            pyautogui.press('f8')
                                                                            
                                                                            #Estrutura de decisão para clicar no desconto somente se houver
                                                                            if desc != '0.0':
                                                                                #Clicar no yes (somente se tiver desconto)
                                                                                if self.find( "confirmacao_Desconto", matching=0.97, waiting_time=5000):
                                                                                    self.click_relative(200, 77)

                                                                            #Clicar no yes
                                                                            if self.find( "confirmacao_Efetuar_Fatura", matching=0.97, waiting_time=5000):
                                                                                self.click_relative(39, 66)

                                                                                if self.find( "jaFoiMovimentada", matching=0.97, waiting_time=5000):
                                                                                    self.click()
                                                                                    time.sleep(0.5)
                                                                                    duplicata = pyautogui.hotkey('ctrl', 'c')
                                                                                    time.sleep(0.5)
                                                                                    duplicata = pyperclip.paste()

                                                                                    linhas_uteis = [l.strip() for l in duplicata.splitlines() if l.strip() and not l.strip().startswith('---')]

                                                                                    mensagem = linhas_uteis[1]
                                                                                    match = re.search(r'Filial \[(\d+)\], N[ºo]\s*\[(\d+)\]', mensagem)

                                                                                    if match:
                                                                                        # filial = match.group(1)   # '102'
                                                                                        numero = match.group(2)   # '30757'

                                                                                        print(f"Duplicata já movimentada: {numero}")

                                                                                    listaCTes.at[CTes, 'SITUACAO'] = "EM VALIDAÇÃO"
                                                                                    listaCTes.at[CTes, 'FATURA'] = numero
                                                                                    listaCTes.at[CTes, 'RESUMO'] = f'Fatura {numero} já foi movimentada'
                                                                                    listaCTes.to_excel(caminho_arquivo, index=False)


                                                                                    continue

                                                                                else:

                                                                                    if self.find( "documentoJaFaturado", matching=0.97, waiting_time=5000):
                                                                                        self.click()
                                                                                        time.sleep(0.5)
                                                                                        duplicata = pyautogui.hotkey('ctrl', 'c')
                                                                                        time.sleep(0.5)
                                                                                        duplicata = pyperclip.paste()

                                                                                        linhas_uteis = [l.strip() for l in duplicata.splitlines() if l.strip() and not l.strip().startswith('---')]
                                                                                        
                                                                                        mensagem = linhas_uteis[1]
                                                                                        match = re.search(r'(\d+)/(\d+)', mensagem)

                                                                                        if match:
                                                                                            # codigo = match.group(0)   # '102/30736' (completo)
                                                                                            # filial = match.group(1)   # '102'
                                                                                            numero = match.group(2)   # '30736' 

                                                                                            print(f"Duplicata gerada: {numero}")

                                                                                        listaCTes.at[CTes, 'SITUACAO'] = "FATURADO" 
                                                                                        listaCTes.at[CTes, 'RESUMO'] = numero
                                                                                        listaCTes.to_excel(caminho_arquivo, index=False)
                                                                                    
                                                                                    #Clicar no ok
                                                                                    if self.find( "faturaEfetuada", matching=0.97, waiting_time=5000):
                                                                                        self.click()
                                                                                        #Fechando o ambiente de fatura
                                                                                        pyautogui.hotkey('alt','v')

                                                                    else:
                                                                        if self.find( "excluir", matching=0.97, waiting_time=5000):
                                                                                self.click()
                                                                                time.sleep(0.5)
                                                                                if self.find( "excluirRegistroPermanente", matching=0.97, waiting_time=5000):
                                                                                    if self.find( "Yes", matching=0.97, waiting_time=5000):
                                                                                        self.click()
                                                                                        time.sleep(0.5)
                                                                                        pyautogui.hotkey('alt','v')
                                                                        continue

                                                            else:
                                                                if self.find( "pastaNovoDoc", matching=0.97, waiting_time=5000):
                                                                    self.click()

                                                                    #Apertar tab
                                                                    pyautogui.press('tab')

                                                                    #Digitar a filial do CTe
                                                                    pyautogui.write(filCTe)

                                                                    #Apertar enter
                                                                    pyautogui.press('enter')

                                                                    #Digitar a série
                                                                    pyautogui.write(serCTe)

                                                                    #Apertar enter
                                                                    pyautogui.press('enter')
                                                                
                                                                    #Digitar o número do CTe
                                                                    pyautogui.write(numCTe)

                                                                    #Apertar enter 2x
                                                                    pyautogui.press('enter')
                                                                    pyautogui.press('enter')

                                                                    if self.find( "documentoJaFaturado", matching=0.97, waiting_time=5000):
                                                                        self.click()
                                                                        time.sleep(0.5)
                                                                        duplicata = pyautogui.hotkey('ctrl', 'c')
                                                                        time.sleep(0.5)
                                                                        duplicata = pyperclip.paste()

                                                                        linhas_uteis = [l.strip() for l in duplicata.splitlines() if l.strip() and not l.strip().startswith('---')]
                                                                        
                                                                        mensagem = linhas_uteis[1]
                                                                        match = re.search(r'\[(\d+)\]', mensagem)

                                                                        if match:
                                                                            numero_duplicata = match.group(1)

                                                                            print(f"Duplicata gerada: {numero_duplicata}")

                                                                        resumo = resumo + f"Documento: {numCTe} esta na Fatura: {numero_duplicata} \n"

                                                                        listaCTes.at[CTes, 'SITUACAO'] = "EM VALIDAÇÃO" 
                                                                        listaCTes.at[CTes, 'RESUMO'] = resumo
                                                                        listaCTes.to_excel(caminho_arquivo, index=False)

                                                                        pyautogui.press('enter')

                                                                        time.sleep(0.5)

                                                                        if self.find( "excluir", matching=0.97, waiting_time=5000):
                                                                            self.click()
                                                                            time.sleep(0.5)
                                                                            if self.find( "excluirRegistroPermanente", matching=0.97, waiting_time=5000):
                                                                                if self.find( "Yes", matching=0.97, waiting_time=5000):
                                                                                    self.click()
                                                                                    time.sleep(0.5)
                                                                                    pyautogui.hotkey('alt','v')

                                                                        continue

                                                                    if self.find( "cteNaoAutorizado", matching=0.97, waiting_time=5000):
                                                                        self.click()
                                                                        time.sleep(0.5)
                                                                        
                                                                        if resumo == "":
                                                                            resumo = f"Documento: {numCTe} não autorizado. \n"
                                                                        else:
                                                                            resumo = resumo + f"Documento: {numCTe} não autorizado. \n"

                                                                        listaCTes.at[CTes, 'SITUACAO'] = "EM VALIDAÇÃO"
                                                                        listaCTes.at[CTes, 'RESUMO'] = resumo
                                                                        listaCTes.to_excel(caminho_arquivo, index=False)

                                                                        pyautogui.press('enter')

                                                                        time.sleep(0.5)

                                                                        if self.find( "excluir", matching=0.97, waiting_time=5000):
                                                                            self.click()
                                                                            time.sleep(0.5)
                                                                            if self.find( "excluirRegistroPermanente", matching=0.97, waiting_time=5000):
                                                                                if self.find( "Yes", matching=0.97, waiting_time=5000):
                                                                                    self.click()
                                                                                    time.sleep(0.5)
                                                                                    pyautogui.hotkey('alt','v')


                                                                        continue

                                                                    #Confirmar se entrou buscando o 1 de 1
                                                                if self.find("confirmacao_Doc_Inserido2", matching=0.97, waiting_time=5000):

                                                                        #Estrutura de decisão para inserir o desconto somente se houver
                                                                        if desc != '0.0':
                                                                            #Clicando no campo para inserir o desconto
                                                                            if self.find( "desconto", matching=0.97, waiting_time=5000):
                                                                                self.click_relative(153, 5)

                                                                                #Digitando o valor do desconto
                                                                                pyautogui.write(str(desc).replace('.',','))

                                                                                #Apertar enter 1x
                                                                                pyautogui.press('enter')

                                                                        #Efetuar a fatura através o atalho (F8)
                                                                        pyautogui.press('f8')
                                                                        
                                                                        #Estrutura de decisão para clicar no desconto somente se houver
                                                                        if desc != '0.0':
                                                                            #Clicar no yes (somente se tiver desconto)
                                                                            if self.find( "confirmacao_Desconto", matching=0.97, waiting_time=5000):
                                                                                self.click_relative(200, 77)

                                                                        #Clicar no yes
                                                                        if self.find( "confirmacao_Efetuar_Fatura", matching=0.97, waiting_time=5000):
                                                                            self.click_relative(39, 66)

                                                                            if self.find( "jaFoiMovimentada", matching=0.97, waiting_time=5000):
                                                                                    self.click()
                                                                                    time.sleep(0.5)
                                                                                    duplicata = pyautogui.hotkey('ctrl', 'c')
                                                                                    time.sleep(0.5)
                                                                                    duplicata = pyperclip.paste()

                                                                                    linhas_uteis = [l.strip() for l in duplicata.splitlines() if l.strip() and not l.strip().startswith('---')]

                                                                                    mensagem = linhas_uteis[1]
                                                                                    match = re.search(r'Filial \[(\d+)\], N[ºo]\s*\[(\d+)\]', mensagem)

                                                                                    if match:
                                                                                        # filial = match.group(1)   # '102'
                                                                                        numero = match.group(2)   # '30757'

                                                                                        print(f"Duplicata já movimentada: {numero}")

                                                                                    listaCTes.at[CTes, 'SITUACAO'] = "EM VALIDAÇÃO"
                                                                                    listaCTes.at[CTes, 'FATURA'] = numero
                                                                                    listaCTes.at[CTes, 'RESUMO'] = f'Fatura {numero} já foi movimentada'
                                                                                    listaCTes.to_excel(caminho_arquivo, index=False)


                                                                                    continue
                                                                            else:

                                                                                if self.find( "documentoJaFaturado", matching=0.97, waiting_time=5000):
                                                                                    self.click()
                                                                                    time.sleep(0.5)
                                                                                    duplicata = pyautogui.hotkey('ctrl', 'c')
                                                                                    time.sleep(0.5)
                                                                                    duplicata = pyperclip.paste()

                                                                                    linhas_uteis = [l.strip() for l in duplicata.splitlines() if l.strip() and not l.strip().startswith('---')]
                                                                                    
                                                                                    mensagem = linhas_uteis[1]
                                                                                    match = re.search(r'(\d+)/(\d+)', mensagem)

                                                                                    if match:
                                                                                        # codigo = match.group(0)   # '102/30736' (completo)
                                                                                        # filial = match.group(1)   # '102'
                                                                                        numero = match.group(2)   # '30736' 

                                                                                        print(f"Duplicata gerada: {numero}")

                                                                                    listaCTes.at[CTes, 'SITUACAO'] = "FATURADO" 
                                                                                    listaCTes.at[CTes, 'FATURA'] = numero
                                                                                    listaCTes.to_excel(caminho_arquivo, index=False)
                                                                                
                                                                                #Clicar no ok
                                                                                if self.find( "faturaEfetuada", matching=0.97, waiting_time=5000):
                                                                                    self.click()
                                                                                    #Fechando o ambiente de fatura
                                                                                    pyautogui.hotkey('alt','v')
                                                                            
                                                                else:
                                                                    if self.find( "excluir", matching=0.97, waiting_time=5000):
                                                                            self.click()
                                                                            time.sleep(0.5)
                                                                            if self.find( "excluirRegistroPermanente", matching=0.97, waiting_time=5000):
                                                                                if self.find( "Yes", matching=0.97, waiting_time=5000):
                                                                                    self.click()
                                                                                    time.sleep(0.5)
                                                                                    pyautogui.hotkey('alt','v')
                                                                    continue                

    def not_found(self, label):
        print(f"Element not found: {label}")
        
if __name__ == '__main__':

    bot = BotCriaFatura()
    bot.main()


