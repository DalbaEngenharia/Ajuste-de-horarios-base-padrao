from Biblioteca_Protheus.tabelas.tabelas_protheus import * 
from listas import horario_base_aceito, horario_base_block

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


def dados_horarios(driver):

    print("____________________________________________________")

    id_tabela_horarios = "COMP7660"

    tabela_horas = linhas_de_tabela(driver, id_tabela_horarios)
    horas = colunas_da_tabela(driver, tabela_horas)

    total_linhas = len(horas)
    alterado = False
    for indice in range(total_linhas):
        print("Horas: ", horas[indice])
        dia = horas[indice][0]
        print("Dia", dia)
        if dia in ["Domingo", "Sábado"]:
            hora_inicio = horario_base_block[0]
            hora_final = horario_base_block[1]
        else:
            hora_inicio = horario_base_aceito[0]
            hora_final = horario_base_aceito[1]
        print("____________________________________________________")
        if horas[indice][1] != hora_inicio:
            atualizar_horario(driver,id_tabela_horarios,1,hora_inicio,indice)
            alterado = True
        time.sleep(2)
        if horas[indice][2] != hora_final:
            atualizar_horario(driver,id_tabela_horarios,2,hora_final,indice)
            alterado = True
    if alterado: 
        funcao_tres_e_demais(driver, "wa-button", "Confirmar")
        funcao_tres_e_demais(driver, "wa-button", "Fechar")
    else: 
        funcao_tres_e_demais(driver, "wa-button", "Fechar")
    None