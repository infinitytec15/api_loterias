import time
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
from sqlalchemy import String, create_engine
from sqlalchemy.orm import declarative_base, Mapped, Session, mapped_column
from fpdf import FPDF
import os
from datetime import datetime
import pytz

load_dotenv()
DeclarativeBase = declarative_base()

class LoteriaDb(DeclarativeBase):
    __tablename__ = 'loteria'
    id: Mapped[int] = mapped_column(primary_key=True)
    concurso: Mapped[int] = mapped_column()
    data_apuracao: Mapped[str] = mapped_column(String(30))
    dezenas: Mapped[str] = mapped_column(String(20))
    horario: Mapped[str] = mapped_column(String(20))
    jogo: Mapped[str] = mapped_column(String(20))

engine = create_engine("sqlite:///bancoloteria.sqlite3", echo=True)
DeclarativeBase.metadata.create_all(engine)

concursos = ["federal"]
config = {
    "federal": {
        "cor": "00ff00",
        "ultimoNumero": 0
    }
}

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in dados.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)

    tz = pytz.timezone('America/Sao_Paulo')
    brasilia_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, f"Hora de Brasília: {brasilia_time}", ln=True)

    pdf_file = "resultado_loteria.pdf"
    pdf.output(pdf_file)
    return pdf_file

def enviar_pdf_discord(pdf_file, dados):
    webhook_url_pdf = os.getenv("DISCORD_WEBHOOK_URL_PDF")
    webhook = DiscordWebhook(url=webhook_url_pdf)

    with open(pdf_file, "rb") as file:
        webhook.add_file(file=file.read(), filename=pdf_file)

    embed = DiscordEmbed(title="Resultado Loterias 2025 - Ilotto", description="Resultados de Loterias",
                         color="00ff00")
    embed.set_timestamp()

    for key, value in dados.items():
        embed.add_embed_field(name=key, value=str(value))

    webhook.add_embed(embed)
    response = webhook.execute()
    print(f"PDF e embed enviados para o canal de PDFs no Discord: {response}")

def enviar_embed_discord(embed):
    webhook_url_embed = os.getenv("DISCORD_WEBHOOK_URL_EMBED")
    webhook = DiscordWebhook(url=webhook_url_embed)
    webhook.add_embed(embed)
    response = webhook.execute()
    print(f"Embed enviado para o canal de embeds no Discord: {response}")

def salvar_pdf_horario(dados):
    tz = pytz.timezone('America/Sao_Paulo')
    brasilia_time = datetime.now(tz).strftime("%Y-%m-%d_%H-%M-%S")
    pdf_file = f"resultado_loteria_{brasilia_time}.pdf"
    pdf_file = gerar_pdf(dados)
    enviar_pdf_discord(pdf_file, dados)

def salvar_no_banco(dados):
    with Session(engine) as session:
        novo_registro = LoteriaDb(
            concurso=dados["Concurso"],
            data_apuracao=dados["Data de Apuração"],
            dezenas=str(dados["Dezenas Sorteadas"]),
            horario=datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S"),
            jogo=dados["Tipo de Jogo"]
        )
        session.add(novo_registro)
        session.commit()
        print("Dados salvos no banco de dados!")

def consultar_banco():
    with Session(engine) as session:
        registros = session.query(LoteriaDb).all()
        for registro in registros:
            print(f"ID: {registro.id}, Concurso: {registro.concurso}, Data: {registro.data_apuracao}, "
                  f"Dezenas: {registro.dezenas}, Horário: {registro.horario}, Jogo: {registro.jogo}")

ultimo_envio_embed = time.time()
ultimo_envio_pdf = time.time()

while True:
    if time.time() - ultimo_envio_embed >= 60:
        for concurso in concursos:
            try:
                url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/{concurso}"
                r = requests.get(url)
                r.raise_for_status()
                obj = r.json()
                concurso_config = config[concurso]

                print(obj["acumulado"], obj["dataApuracao"], obj["dataProximoConcurso"], obj["dezenasSorteadasOrdemSorteio"],
                      obj["tipoJogo"], obj["numero"])

                embed = DiscordEmbed(title="Resultado Loterias 2025 - Ilotto", description="Resultados de Loterias",
                                     color=concurso_config["cor"])
                embed.set_timestamp()

                embed.add_embed_field(name="Acumulado", value=obj["acumulado"])
                embed.add_embed_field(name="Data de Apuração", value=obj["dataApuracao"])
                embed.add_embed_field(name="Próximo Concurso", value=obj["dataProximoConcurso"])
                embed.add_embed_field(name="Dezenas Sorteadas", value=str(obj["dezenasSorteadasOrdemSorteio"]))
                embed.add_embed_field(name="Concurso", value=obj["numero"])
                embed.add_embed_field(name="Tipo de Jogo", value=obj["tipoJogo"])

                enviar_embed_discord(embed)
                ultimo_envio_embed = time.time()

            except Exception as e:
                print(f"Erro ao processar o concurso {concurso}: {e}")

    if time.time() - ultimo_envio_pdf >= 3600:
        for concurso in concursos:
            try:
                url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/{concurso}"
                r = requests.get(url)
                r.raise_for_status()
                obj = r.json()

                dados_pdf = {
                    "Acumulado": obj["acumulado"],
                    "Data de Apuração": obj["dataApuracao"],
                    "Próximo Concurso": obj["dataProximoConcurso"],
                    "Dezenas Sorteadas": str(obj["dezenasSorteadasOrdemSorteio"]),
                    "Concurso": obj["numero"],
                    "Tipo de Jogo": obj["tipoJogo"],
                }

                salvar_pdf_horario(dados_pdf)
                salvar_no_banco(dados_pdf) 
                consultar_banco()  
                ultimo_envio_pdf = time.time()

            except Exception as e:
                print(f"Erro ao processar o concurso {concurso} para PDF: {e}")

    time.sleep(1)
