from Biblioteca_Protheus import * 
from Biblioteca_Protheus.tabelas.tabelas_protheus import * 
from verificar_horarios import dados_horarios
from listas import descricoes_de_grupos_a_ignorar

def verifica_fim_da_lista(driver):
    funcao_tres_e_demais(driver, "wa-button", "A")
    esperar_existir(driver,"wa-button","Confirmar")
    funcao_tres_e_demais(driver, "wa-button", "Fechar")
    time.sleep(2)

def selecao_grupo(driver): 

    esperar_existir(driver,"wa-button","A")
    time.sleep(5)
    grupos = linhas_de_tabela(driver,"COMP6013" )
    print(len(grupos))

    colunas=colunas_da_tabela(driver,grupos)
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ESCAPE)
    time.sleep(1)
    body.send_keys(Keys.ESCAPE)
    time.sleep(1)
    grupos[0].click()
    
    # for indice, coluna in enumerate(colunas): 
    #      print(coluna)
    indice = 0
    id_tabela_horarios = "COMP6013"
    fim = False
    while True: 
        time.sleep(1)
        grupos = linhas_de_tabela(driver,"COMP6013" )
        colunas=colunas_da_tabela(driver,grupos)

        try:
            print("Try 1")
            print("Indice: ", indice)
            print("TESTE 0: ", colunas[0])
            print("TESTE: ", colunas[indice])
            print("TESTE: ", colunas[indice+1])
            if colunas[indice + 1]: 
                None
            if any(grupo.lower() in colunas[indice][2].lower() for grupo in descricoes_de_grupos_a_ignorar):
                indice = indice + 1 
                descer_para_proxima_na_tabela(driver,id_tabela_horarios)

                continue
        except:
            if indice == 14: 
                verifica_fim_da_lista(driver)
                indice = 0
                continue
            else:
                print("EXCEPT!!!!")
                descricao_linha = colunas[indice][2].lower()
                if any(descricao.lower() in descricao_linha
                        for descricao in descricoes_de_grupos_a_ignorar):

                    driver.execute_script("document.getElementById('COMP6014').click();")
                    break
                else: 
                    fim = True
        print("Linha: ", colunas[indice][2])


        funcao_tres_e_demais(driver, "wa-button", "A")
        esperar_existir(driver,"wa-button","Confirmar")
        Scriptfind(driver,"wa-tab-button",retorno=True,tipo="caption")
        driver.find_element(By.ID, "BUTTON-COMP7520").click()
        
        
        dados_horarios(driver)
        print("INDICE ATUAL: ", indice)
        time.sleep(2)
        indice = 1
        descer_para_proxima_na_tabela(driver,id_tabela_horarios)

        grupos = linhas_de_tabela(driver,"COMP6013" )
        colunas=colunas_da_tabela(driver,grupos)
        if fim: 
            driver.execute_script("document.getElementById('COMP6014').click();")
            time.sleep(5)
            break
        else:
            continue
        
