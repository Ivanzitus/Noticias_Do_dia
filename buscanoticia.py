import requests
from bs4 import BeautifulSoup
import mysql.connector
import datetime

host="localhost"
user="root"
senha=""
banco="noticias"

def conectar():
    conexao=None
    try:
        conexao =  mysql.connector.connect(
            host=host,
            user=user,
            password=senha,
            database=banco
        )
        print("Conectado com")
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o BD:{e}")

    return conexao


def extrair_e_salvar_titulos():
    url = 'https://g1.globo.com/'

    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, 'html.parser')

        titulos = []

        for h2 in soup.find_all('h2'):  
            titulo = h2.get_text(strip=True)
            if titulo:
                titulos.append(titulo)
                print(titulos)

        if titulos:
            conexao=conectar()

            cursor = conexao.cursor()

            for titulo in titulos:
                data = datetime.datetime.now()  
                cursor.execute(
                    "INSERT INTO noticia (titulo, data) VALUES (%s, %s)",
                    (titulo, data)
                )

            conexao.commit()
            print(f"{len(titulos)} títulos armazenados no banco de dados.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if conexao:
            conexao.close()
        if cursor:
            cursor.close()

extrair_e_salvar_titulos()

def resgatar_titulos():
    conexao = None
    try:
        # Conectar ao banco de dados
        conexao = conectar()
        
        cursor = conexao.cursor()

        # Consultar os títulos armazenados
        cursor.execute("SELECT titulo, data FROM noticia")
        
        # Obter todos os resultados
        resultados = cursor.fetchall()

        if resultados:
            print(f"{len(resultados)} títulos encontrados no banco de dados:")
            for resultado in resultados:
                titulo, data = resultado
                print(f"{titulo} - {data}")
        else:
            print("Nenhum título encontrado no banco de dados.")

    except mysql.connector.Error as e:
        print(f"Erro ao consultar o banco de dados: {e}")
    finally:
        if conexao:
            conexao.close()
        if cursor:
            cursor.close()

# Chamar a função para resgatar os títulos
resgatar_titulos()