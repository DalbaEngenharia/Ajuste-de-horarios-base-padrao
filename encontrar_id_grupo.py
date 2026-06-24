import pyodbc
def encontrar_id_grupo(usuario):
    conn = pyodbc.connect(
        "DRIVER={PostgreSQL ANSI(x64)};"
        "SERVER=192.168.254.212;"
        "PORT=5432;"
        "DATABASE=prd;"
        "UID=gustavo.elicker;"
        "PWD=ge9550;"
    )

    cursor = conn.cursor()

    try:

        query = """
        SELECT
            usr.usr_id,
            usr_grupo,
            usr_codigo,
            usr_nome
            
        FROM sys_usr usr

        LEFT JOIN sys_usr_groups grp
            ON grp.d_e_l_e_t_ = ''
            AND usr.usr_id = grp.usr_id
            
        WHERE usr.d_e_l_e_t_ = ''
            AND usr.usr_msblql = '2'
            AND usr.usr_grprule = '1'
            AND usr.usr_codigo = ?
        ORDER BY usr.usr_codigo
        """

        cursor.execute(query, (usuario,))
        resultados = cursor.fetchall()

        # 📄 salvar em txt

        if resultados:
            for row in resultados:
                linha = (
                    f"ID: {row.usr_id} | "
                    f"Grupo: {row.usr_grupo} | "
                    f"Código: {row.usr_codigo} | "
                    f"Nome: {row.usr_nome}"
                )
                id = row.usr_grupo
                print(linha)

        else:
            msg = "Nenhum resultado encontrado."
            print(msg)
            f.write(msg + "\n")


    except Exception as e:
        print("Erro:", e)

    finally:
        cursor.close()
        conn.close()
    return id