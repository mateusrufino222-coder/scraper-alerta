"""
Projeto de Portfólio 3: Scraper + Alerta Automático
-------------------------------------------------------
Esse script coleta um valor que muda com frequência (ex: cotação
do dólar) e envia um alerta por e-mail quando o valor ultrapassa
um limite definido pelo usuário.

Ideia: esse tipo de automação é muito valorizado por clientes,
porque combina coleta de dados (scraping) com uma ação automática
(notificação) — economiza tempo de quem precisaria checar
manualmente todo dia.

Bibliotecas usadas:
- requests: pra buscar os dados
- smtplib: biblioteca nativa do Python pra enviar e-mails
"""

import requests
import smtplib
from email.mime.text import MIMEText

# ---------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------
# API pública e gratuita de cotação de moedas, usada aqui
# como exemplo de uma fonte de dados que muda com frequência.
URL_COTACAO = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

VALOR_LIMITE = 5.50  # dispara alerta se o dólar passar disso

# Dados de e-mail (preencha com os seus dados reais para usar).
# Para Gmail, é necessário criar uma "senha de app" nas
# configurações de segurança da conta — não use a senha normal.
EMAIL_REMETENTE = "seuemail@gmail.com"
SENHA_APP = "sua_senha_de_app_aqui"
EMAIL_DESTINATARIO = "seuemail@gmail.com"


def buscar_cotacao_dolar():
    """Busca a cotação atual do dólar (USD -> BRL) via API pública."""
    resposta = requests.get(URL_COTACAO)
    resposta.raise_for_status()
    dados = resposta.json()

    valor = float(dados["USDBRL"]["bid"])
    return valor


def enviar_alerta(valor_atual):
    """Envia um e-mail de alerta informando o valor atual."""
    assunto = "Alerta: Dólar ultrapassou o limite definido"
    corpo = (
        f"O dólar está em R$ {valor_atual:.2f}, "
        f"ultrapassando o limite de R$ {VALOR_LIMITE:.2f}."
    )

    mensagem = MIMEText(corpo)
    mensagem["Subject"] = assunto
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = EMAIL_DESTINATARIO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(EMAIL_REMETENTE, SENHA_APP)
        servidor.send_message(mensagem)


if __name__ == "__main__":
    print("Consultando cotação do dólar...")
    valor_atual = buscar_cotacao_dolar()
    print(f"Cotação atual: R$ {valor_atual:.2f}")

    if valor_atual > VALOR_LIMITE:
        print(f"Valor ultrapassou o limite de R$ {VALOR_LIMITE:.2f}. Enviando alerta...")
        enviar_alerta(valor_atual)
        print("Alerta enviado por e-mail!")
    else:
        print("Valor dentro do limite. Nenhum alerta necessário.")