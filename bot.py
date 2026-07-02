import pyautogui
import time
import pandas
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

        abrir_vr()
        
        #Ler a lista de faturas a extrair
        listaCTes = pandas.read_excel(caminho_arquivo)

        if self.find( "faturamento", matching=0.97, waiting_time=20000):
            for CTes in range(len(listaCTes)):
                def pegar_valor(coluna):
                    try:
                        return str(listaCTes[coluna][CTes])
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

                #Abrindo o ambiente da fatura
                if self.find( "faturamento", matching=0.97, waiting_time=20000):
                    self.click()

                    if self.find( "Movimentacao", matching=0.97, waiting_time=10000):
                        self.click()

                        if self.find( "fatura_Duplicata", matching=0.97, waiting_time=10000):
                            self.click()

                            #Clicando na filial para inserir a filial da fatura
                            if self.find( "filialFatura", matching=0.97, waiting_time=10000):
                                self.click_relative(55, 33)

                                #Digitando o código da filial
                                pyautogui.write(filFat)

                                #Apertando o enter 2x
                                pyautogui.press('enter')
                                pyautogui.press('enter')

                                #Confirmando se deu certo através da fatura inconsistente
                                if self.find( "faturaInconsistente", matching=0.97, waiting_time=10000):

                                    #Clicar no codigo cliente (pagador)
                                    if self.find( "Cliente_pagador", matching=0.97, waiting_time=10000):
                                        self.click_relative(95, 37)

                                        #Digitar o código do cliente
                                        pyautogui.write(codPag)

                                        #Apertar o enter 1x
                                        pyautogui.press('enter')
                                        # pyautogui.press('tab') # A SER VALIDADO
                                        # pyautogui.write("19") # A SER VALIDADO

                                        #Confirmando se os dados entrou através da Tarefa
                                        if self.find( "tarefa", matching=0.97, waiting_time=10000):

                                            #Clicar em observação
                                            if self.find( "obsFatura", matching=0.97, waiting_time=10000):
                                                self.click_relative(90, 72)

                                                #Inserir a observação
                                                pyautogui.write(obs)

                                                #Clicar em salvar
                                                if self.find( "salvar", matching=0.97, waiting_time=10000):
                                                    self.click()

                                                    #Ir para aba documentos
                                                    if self.find( "abaDocumentos", matching=0.97, waiting_time=10000):
                                                        self.click()

                                                    #Clicar na pastinha
                                                        if ',' in numCTe:
                                                            lista_CTES =  numCTe.split(',')
                                                            for numero_str in lista_CTES:
                                                                if self.find( "pastaNovoDoc", matching=0.97, waiting_time=50000):
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
                                                                    pyautogui.click(514,399)
                                                                    time.sleep(2)
                                                        else:
                                                            if self.find( "pastaNovoDoc", matching=0.97, waiting_time=10000):
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

                                                            #Confirmar se entrou buscando o 1 de 1
                                                        if self.find("confirmacao_Doc_Inserido2", matching=0.97, waiting_time=10000):

                                                                #Estrutura de decisão para inserir o desconto somente se houver
                                                                if desc != '0.0':
                                                                    #Clicando no campo para inserir o desconto
                                                                    if self.find( "desconto", matching=0.97, waiting_time=10000):
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
                                                                    if self.find( "confirmacao_Desconto", matching=0.97, waiting_time=10000):
                                                                        self.click_relative(200, 77)

                                                                #Clicar no yes
                                                                if self.find( "confirmacao_Efetuar_Fatura", matching=0.97, waiting_time=10000):
                                                                    self.click_relative(39, 66)
                                                                    
                                                                    #Clicar no ok
                                                                    if self.find( "faturaEfetuada", matching=0.97, waiting_time=10000):
                                                                        self.click()

                                                                        #Fechando o ambiente de fatura
                                                                        pyautogui.hotkey('alt','v')
    def not_found(self, label):
        print(f"Element not found: {label}")
        
if __name__ == '__main__':

    bot = BotCriaFatura()
    bot.main()


