import pandas as pd
from openpyxl import load_workbook
import os
import numpy as np
import pyautogui
import ctypes
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys          
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
import shutil
from datetime import datetime, timedelta


time = 0.5
caminho = os.getcwd() 
caminho_sistema = caminho.replace("C", "T", 1)
multi = False

def click_selenium(selector, value):
    try:
        print("Clicando no botão...")
        elemento = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((selector, value)))
        elemento.click()
    except Exception as e:
        print(f"Erro ao clicar: {e}")

def click_(image_path, confidence=0.9):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = caminho + r'\IMAGENS'
    image_path = os.path.join(current_dir, caminho_imagem, image_path) 
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if position:
            center_x = position.left + position.width // 2
            center_y = position.top + position.height // 2
            pyautogui.click(center_x, center_y)
            print("Imagem foi encontrada na tela.")
    except Exception as e:
        print("Imagem não encontrada na tela. Aguardando...")

#enquanto o campo de data nota nao estiver vazio apertar os botoes
def finalizar_baixa(image_path, confidence=0.9):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = caminho + r'\IMAGENS'
    image_path = os.path.join(current_dir, caminho_imagem, image_path) 
    while True:
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if position:
                print("Imagem foi encontrada na tela.")
                break
        except Exception as e:
            click_('yes.png')
            click_('yes_marcado.png')
            click_('ok.png')
            click_('cancelar.png')
            print("Imagem não encontrada na tela. Aguardando...")
        pyautogui.sleep(0.5)

def remover_hora(data_str):
    if pd.notna(data_str) and isinstance(data_str, str):
        return data_str[:-5]
    return None

def click_image(image_path, confidence=0.9):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = caminho + r'\IMAGENS'
    image_path = os.path.join(current_dir, caminho_imagem, image_path) 
    while True:
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if position:
                center_x = position.left + position.width // 2
                center_y = position.top + position.height // 2
                pyautogui.click(center_x, center_y)
                print("Imagem foi encontrada na tela.")
                break
        except Exception as e:
            print("Imagem não encontrada na tela. Aguardando...")
        pyautogui.sleep(1)

def confirmacao_preenchido(image_path, image_path2, image_path3, confidence=0.9):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = caminho + r'\IMAGENS'
    image_path = os.path.join(current_dir, caminho_imagem, image_path)
    image_path2 = os.path.join(current_dir, caminho_imagem, image_path2)
    image_path3 = os.path.join(current_dir, caminho_imagem, image_path3)
    a, b, c = 0, 0, 0
    while True:
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if position:
                print("Imagem 1 foi encontrada na tela.")
                a = 0  # Redefine 'a' se a imagem 1 for encontrada
                click_image('referencia.png')
                for i in range(10):
                    pyautogui.press("backspace")
                pyautogui.write(str(referencia))
            else:
                a = 1  # Define 'a' como 1 se a imagem 1 não for encontrada
        except Exception as e:
            print("Erro ao procurar imagem 1:", e)
            a = 1
        try:
            position2 = pyautogui.locateOnScreen(image_path2, confidence=confidence)
            if position2:
                print("Imagem 2 foi encontrada na tela.")
                b = 0  # Redefine 'b' se a imagem 2 for encontrada
                click_image('digitar_data.png')
                for i in range(10):
                    pyautogui.press("backspace")
                pyautogui.write(str(data_nota_fiscal))
                pyautogui.sleep(time)  
            else:
                b = 1  # Define 'b' como 1 se a imagem 2 não for encontrada
        except Exception as e:
            print("Erro ao procurar imagem 2:", e)
            b = 1
        try:
            position3 = pyautogui.locateOnScreen(image_path3, confidence=confidence)
            if position3:
                print("Imagem 3 foi encontrada na tela.")
                c = 0  # Redefine 'c' se a imagem 3 for encontrada
                click_nota('digitar_nota.png')
                pyautogui.sleep(time)
                if multi == True:
                    pyautogui.write('00')
                    pyautogui.sleep(0.2)
                pyautogui.write(str(nf))
                pyautogui.sleep(time)
            else:
                c = 1  # Define 'c' como 1 se a imagem 3 não for encontrada
        except Exception as e:
            print("Erro ao procurar imagem 3:", e)
            c = 1
        # Se todas as três imagens não forem encontradas, sai do loop
        if a == 1 and b == 1 and c == 1:
            print("Nenhuma das três imagens foi encontrada. Saindo do loop.")
            click_image('atualizar.png')
            pyautogui.sleep(time)
            for i in range(2):
                pyautogui.press('tab')
            break
        
def baixada_ou_nao(yes, ok, confidence=0.9):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = caminho + r'\IMAGENS'
    yes_path = os.path.join(current_dir, caminho_imagem, yes) 
    ok_path = os.path.join(current_dir, caminho_imagem, ok) 
    while True:
        try:
            position = pyautogui.locateOnScreen(yes_path, confidence=confidence)
            if position:
                center_x = position.left + position.width // 2
                center_y = position.top + position.height // 2
                pyautogui.click(center_x, center_y)
                print("Nota sera baixada.")
                break
        except Exception as e:
            print("Imagem 'yes' não encontrada na tela. Aguardando...")
        
        try:
            position = pyautogui.locateOnScreen(ok_path, confidence=confidence)
            if position:
                center_x = position.left + position.width // 2
                center_y = position.top + position.height // 2
                pyautogui.click(center_x, center_y)
                print("Nota ja baixada.")
                return True
        except Exception as e:
            print("Imagem 'ok' não encontrada na tela. Aguardando...")
        pyautogui.sleep(1)
    return False

def imagem_encontrada(image_path, confidence=0.9, max_attempts=5):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = os.path.join(current_dir, 'IMAGENS')
    image_path = os.path.join(caminho_imagem, image_path)
    for attempt in range(max_attempts):
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if position:
                print("Nota encontrada na tela.")
                return True
        except Exception as e:
            print("Nota não encontrada na tela. Aguardando...")
        pyautogui.sleep(1)

    click_image('CTRC.png')
    for i in range(2):
        pyautogui.press("down")
    pyautogui.sleep(0.5)
    pyautogui.press("enter")   
    for attempt in range(max_attempts):
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if position:
                print("Nota encontrada na tela é uma OST.")
                return True
        except Exception as e:
            print("Nota não encontrada na tela. Aguardando...")
        pyautogui.sleep(1)  

    multi = True
    click_image('cancelar.png')
    click_image('referencia.png')
    for i in range(10):
        pyautogui.press("backspace")
    pyautogui.write(str(referencia))
    click_image('digitar_data.png')
    for i in range(15):
        pyautogui.press("backspace")
    pyautogui.write(str(data_nota_fiscal))
    pyautogui.sleep(1)  
    click_nota('digitar_nota.png')
    pyautogui.sleep(1)
    pyautogui.write('00')
    pyautogui.sleep(0.2)
    pyautogui.write(str(nf))
    pyautogui.sleep(1)
    confirmacao_preenchido('referencia.png','digitar_data.png','digitar_nota.png')
    # for i in range(15):
    #     pyautogui.press("left")
    pyautogui.sleep(1)
    click_image('atualizar.png')
    pyautogui.sleep(1)
    for i in range(2):
        pyautogui.press('tab')
    for attempt in range(max_attempts):
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if position:
                print("Nota encontrada na tela.")
                confirmacao_preenchido('referencia.png','digitar_data.png','digitar_nota.png')
                return True
        except Exception as e:
            print("Nota não encontrada na tela. Aguardando...")
        pyautogui.sleep(1)
    print("Número máximo de tentativas atingido. Nota não encontrada.")
    return False
 
def verificar_campo(image_name, confidence=0.9):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = os.path.join(current_dir, 'IMAGENS')
    image_path = os.path.join(caminho_imagem, image_name)    
    while True:
        found = False
        for i in range(5): 
            try:
                position = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if position:
                    print("Campo preenchido.")
                    found = True
                    break
            except Exception as e:
                print(f"Erro ao procurar o campo: {e}")
            print("Campo não preenchido. Aguardando...")
            pyautogui.sleep(1)       
        if found:
            break
        else:
            click_image('salvar_filial.png')
            for i in range(5):
                pyautogui.press("backspace")
            pyautogui.write("1")
            pyautogui.sleep(1)   
            pyautogui.press("tab")
            for i in range(5):
                pyautogui.press("backspace")
            pyautogui.write("1")
            pyautogui.sleep(1)   
            pyautogui.press("tab")
            for i in range(5):
                pyautogui.press("backspace")            
            pyautogui.write("1")
            pyautogui.sleep(1)   
            pyautogui.press("tab")

def click_nota(image_path, confidence=0.9):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = caminho + r'\IMAGENS'
    image_path = os.path.join(current_dir, caminho_imagem, image_path) 
    while True:
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if position:
                center_x = position.left + position.width // 2
                center_y = position.top + position.height // 2
                center_x += 90  # Adicionar deslocamento para a direita
                pyautogui.click(center_x, center_y)
                print("Imagem foi encontrada na tela.")
                break
        except Exception as e:
            print("Imagem não encontrada na tela. Aguardando...")
        pyautogui.sleep(1)

def image_erro(image_name,image_name2,image_name3,image_name4,confidence=0.9):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = os.path.join(current_dir, 'IMAGENS')
    image_path = os.path.join(caminho_imagem, image_name)
    image_path2 = os.path.join(caminho_imagem, image_name2)
    image_path3 = os.path.join(caminho_imagem, image_name3)
    image_path4 = os.path.join(caminho_imagem, image_name4)
    while True:
        try:
            position = pyautogui.locateOnScreen(image_path, confidence=confidence)         
            if position:
                click_image('ok_aviso.png')
                try:
                    position3 = pyautogui.locateOnScreen(image_path3, confidence=confidence)
                    if position:
                        center_x = position3.left + position3.width // 2
                        center_y = position3.top + position3.height // 2
                        pyautogui.moveTo(center_x, center_y)  # Movendo o cursor para a posição da imagem               
                        pyautogui.moveRel(-80, 0)  # Movendo o cursor para cima
                        pyautogui.click()  # Clicando no local da imagem
                        for i in range(2): 
                            pyautogui.press("tab")
                        click_image('efetuar_baixa.png')
                        print("Imagem de erro encontrada na tela.")
                        break
                except Exception as e:
                    print("Imagem não encontrada na tela. Aguardando...")
            position2 = pyautogui.locateOnScreen(image_path2, confidence=confidence)
            if position2:
                 break
        except Exception as e:
            print("Imagem de erro não encontrada na tela.")
        try:
            position2 = pyautogui.locateOnScreen(image_path2, confidence=confidence)
            if position2:
                print("Imagem de Baixa efetuada")
                break
        except Exception as e:
            print("Imagem de Baixa não encontrada na tela.")
        try:
            position4 = pyautogui.locateOnScreen(image_path4, confidence=confidence)
            if position4:
                print("Imagem de Baixa efetuada")
                break
        except Exception as e:
            print("Imagem de Baixa não encontrada na tela.")       
        pyautogui.sleep(1)

def erro_efetuar(image_path, confidence=0.9, max_attempts=5):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = os.path.join(current_dir, r'IMAGENS', image_path)
    attempts = 0
    while attempts < max_attempts:
        try:
            position = pyautogui.locateOnScreen(caminho_imagem, confidence=confidence)
            if position:
                click_image('OK.png')
                pyautogui.sleep(2)
                click_image('OK.png')
                click_image('efetuar_baixa.png')
                break
        except Exception as e:
            print(f"Imagem não encontrada na tela. Tentativa {attempts + 1} de {max_attempts}. Aguardando...")
        attempts += 1
        pyautogui.sleep(1)

def atualizar_ocorrencia(image_path, confidence=0.9, max_attempts=5):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = os.path.join(current_dir, r'IMAGENS', image_path)
    attempts = 0
    while attempts < max_attempts:
        try:
            position = pyautogui.locateOnScreen(caminho_imagem, confidence=confidence)
            if position:
                center_x = position.left + position.width // 2
                center_y = position.top + position.height // 2
                pyautogui.click(center_x, center_y)
                print("Baixa de ocorrencia feita com sucesso.")
                break
        except Exception as e:
            print(f"Imagem da baixa nao encontrada. Tentativa {attempts + 1} de {max_attempts}. Aguardando...")
        attempts += 1
        pyautogui.sleep(1)

def verificar_ok_final(image_path, confidence=0.9, max_attempts=5):
    current_dir = os.path.dirname(__file__)  # Diretório atual do script
    caminho_imagem = os.path.join(current_dir, r'IMAGENS', image_path)
    attempts = 0
    while attempts < max_attempts:
        try:
            position = pyautogui.locateOnScreen(caminho_imagem, confidence=confidence)
            if position:
                center_x = position.left + position.width // 2
                center_y = position.top + position.height // 2
                pyautogui.click(center_x, center_y)
                print("Ok final encontrado com sucesso.")
                break
        except Exception as e:
            print(f"Imagem do ok nao encontrada. Tentativa {attempts + 1} de {max_attempts}. Aguardando...")
        attempts += 1
        pyautogui.sleep(1)

def check_caps_lock():
    return ctypes.windll.user32.GetKeyState(0x14) & 0xffff != 0

def alt_press(key):
    pyautogui.keyDown('alt')
    pyautogui.press(key)
    pyautogui.keyUp('alt')

def processar_coluna_data(df, coluna):
    df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
    df[coluna] = df[coluna].dt.date
    df[coluna] = df[coluna].astype(str).str.strip()  # Converter para string e remover espaços em branco
    df[coluna] = pd.to_datetime(df[coluna], format='%Y-%m-%d', errors='coerce')  # Converter para datetime
    df[coluna] = df[coluna] + pd.Timedelta(hours=22)  # Adicionar o horário '22:00'
    df[coluna] = df[coluna].dt.strftime('%d/%m/%Y %H:%M')  # Formatar no formato desejado

def processar_coluna_chegada(df, coluna):
    df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
    df[coluna] = df[coluna] + pd.Timedelta(hours=22)
    df[coluna] = df[coluna].dt.strftime('%d/%m/%Y%H:%M')

def processar_datas(df, colunas):
    for coluna in colunas:
        if 'Data Entrega' in coluna:
            df[coluna] = pd.to_datetime(df[coluna], dayfirst=True, errors='coerce') + pd.Timedelta(minutes=1)
        elif 'Fim Descarreg.' in coluna:
            df[coluna] = pd.to_datetime(df[coluna], dayfirst=True, errors='coerce') + pd.Timedelta(minutes=2)
        df[coluna] = df[coluna].dt.strftime('%d/%m/%Y%H:%M')
        
def formatar_datas(df, colunas):
    for coluna in colunas:
        df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
        df[coluna] = df[coluna].dt.strftime('%d/%m/%Y%H:%M')
    

Planilha_CC19 = pd.read_excel("planilhaderotascc19.xlsx")
colunas_para_remover = ['Série', 'Cnpj cliente', 'Status da baixa','Cliente','Cidade','Ct-e/OST','Peso','Qtde','Vlr Merc.','Entrega Canhoto Físico','NF com problema','Imagem Salva - Com Erro']
Planilha_CC19.drop(columns=colunas_para_remover, inplace=True)
Planilha_CC19['N° NF'] = pd.to_numeric(Planilha_CC19['N° NF'], errors='coerce')
Planilha_CC19.dropna(subset=['N° NF'], inplace=True)
Planilha_CC19['N° NF'] = Planilha_CC19['N° NF'].astype(int)
Planilha_CC19 = Planilha_CC19.rename(columns={'N° NF': 'NF', 'Data NF': 'DATA NOTA FISCAL', 'Data': 'Data Chegada', 'Status da entrega': 'STATUS'})
Planilha_CC19['Data Entrega'] = Planilha_CC19['Data Chegada']
Planilha_CC19['Fim Descarreg.'] = Planilha_CC19['Data Chegada']
Planilha_CC19['DATA NOTA FISCAL'] = pd.to_datetime(Planilha_CC19['DATA NOTA FISCAL'])
Planilha_CC19['DATA NOTA FISCAL'] = Planilha_CC19['DATA NOTA FISCAL'].dt.strftime('%d/%m/%Y')
colunas_de_data = ['Data Entrega', 'Fim Descarreg.']
for coluna in colunas_de_data:
    processar_coluna_data(Planilha_CC19, coluna)
processar_datas(Planilha_CC19, colunas_de_data)
processar_coluna_chegada(Planilha_CC19,'Data Chegada')
Planilha_CC19 = Planilha_CC19.dropna(axis=1, how='all')
Planilha_CC19 = Planilha_CC19[Planilha_CC19['STATUS'] == 'Entregue']

for i, linha in enumerate(Planilha_CC19.index):
    nf = Planilha_CC19.loc[linha, "NF"]
    status = Planilha_CC19.loc[linha, "STATUS"]
    print(f'nf:{nf} status:{status}')