from biblioteca_protheus.tabelas.tabelas_protheus import *
from listas import horario_base_aceito, horario_base_block
from datetime import datetime

def atualizar_horario(driver, id_tabela, coluna, valor, indice):
    
    for tentativa in range(10):

        print("Tentativa:", tentativa + 1)

        inserir_na_tabela_shadow(driver,id_tabela,coluna,valor,indice)

        time.sleep(2)

        tabela_horas = linhas_de_tabela(driver, id_tabela)
        horas = colunas_da_tabela(driver, tabela_horas)

        valor_atual = horas[indice][coluna]
        print("Horas: ", horas[indice])
        print("Linha:", indice)
        print("Valor atual:", valor_atual)

        if valor_atual == valor:
            print("Atualizado com sucesso")
            return True

        print(f"Falha ao atualizar linha {indice}")

    return False

from datetime import datetime

def dados_horarios(driver,dados_json):
    print("dados json: ", dados_json)
    print("____________________________________________________")

    id_tabela_horarios = "COMP7660"

    tabela_horas = linhas_de_tabela(driver, id_tabela_horarios)
    horas = colunas_da_tabela(driver, tabela_horas)

    total_linhas = len(horas)
    alterado = False

    inicio = datetime.strptime("06:00", "%H:%M").time()
    fim = datetime.strptime("19:00", "%H:%M").time()
    # loop para ler tabela de horarios  
    for indice in range(total_linhas):
        print("Horas: ", horas[indice])
        dia = horas[indice][0]
        print("Dia", dia)
        horario_inicio_alterado = False
        horario_final_alterado = False
        if dia in dados_json:
            hora1 = datetime.strptime(dados_json[dia][0], "%H:%M").time()
            hora2 = datetime.strptime(dados_json[dia][1], "%H:%M").time()
            if dia not in ["Sábado", "Domingo"]: 
                     
                if hora1 > inicio: 
                    hora1 = inicio
                    horario_inicio_alterado = True
                if hora2 < fim: 
                    hora2 = fim
                    horario_final_alterado = True
    
            if hora1 > hora2:     
                continue
            
            if horario_inicio_alterado:
                hora_inicio = hora1.strftime("%H:%M")
            else:
                hora_inicio = dados_json[dia][0]

            if horario_final_alterado:
                hora_final = hora2.strftime("%H:%M")
            else:
                hora_final = dados_json[dia][1]

            print("____________________________________________________")
            if horas[indice][1] != hora_inicio:
                atualizar_horario(driver,id_tabela_horarios,1,hora_inicio,indice)
                alterado = True
            time.sleep(2)
            if horas[indice][2] != hora_final:
                atualizar_horario(driver,id_tabela_horarios,2,hora_final,indice)
                alterado = True
        else: 
            if dia in ["Sábado", "Domingo"]: 
                if  horas[indice][1] != "00:00": 
                    atualizar_horario(driver,id_tabela_horarios,1,"00:00",indice)
                if horas[indice][2] != "23:59":
                    atualizar_horario(driver,id_tabela_horarios,2,"23:59",indice)
            else: 
                if  horas[indice][1] != "06:00": 
                    atualizar_horario(driver,id_tabela_horarios,1,"06:00",indice)
                if horas[indice][2] != "19:00":
                    atualizar_horario(driver,id_tabela_horarios,2,"19:00",indice) 
            #continue


    if alterado: 
        funcao_tres_e_demais(driver, "wa-button", "Confirmar")
        funcao_tres_e_demais(driver, "wa-button", "Fechar")
    else: 
        funcao_tres_e_demais(driver, "wa-button", "Fechar")
    None
