import flet as ft
import mysql.connector

user = "root"
senha = ""
host = "localhost"
banco = "noticias"

def conectar():
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=senha,
            database=banco
        )
        print("Conectado com sucesso ao banco de dados.")
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o BD: {e}")

    return conexao

def fechar_conexao(conexao):
    if conexao.is_connected():
        conexao.close()
        print("Conexão com o BD encerrada!")

def main(pg: ft.Page):
    pg.auto_scroll = ft.ScrollMode.AUTO
    pg.theme_mode = ft.ThemeMode.DARK
    pg.window.width = 900

    conexao = conectar()

    tb_tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color="blue", size=16)),
            ft.DataColumn(ft.Text("Titulo", color="blue", size=16)),
            ft.DataColumn(ft.Text("Data", color="blue", size=16)),
        ]
    )

    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, titulo, data FROM noticia")
        resultados = cursor.fetchall()

        for resultado in resultados:
            id, titulo, data = resultado
            tb_tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id))),
                        ft.DataCell(ft.Text(titulo)),
                        ft.DataCell(ft.Text(str(data))),
                    ]
                )
            )
    
    pg.add(tb_tabela)

    fechar_conexao(conexao)

ft.app(main)