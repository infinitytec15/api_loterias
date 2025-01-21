import time
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

concursos =[
"quina",
"federal",
]
config = {
    "quina":{
        "cor":"ff0000",
        "ultimoNumero":0
    },
    "federal":{
        "cor":"00ff00",
        "ultimoNumero":0
    }
}

while True:

    for concurso in concursos:
        url="https://servicebus2.caixa.gov.br/portaldeloterias/api/"
        url+=concurso
        r=requests.get(url)
        obj=r.json()
        concurso_config = config[concurso]
        print(obj["acumulado"], obj["dataApuracao"], obj["dataProximoConcurso"], obj["dezenasSorteadasOrdemSorteio"], obj["tipoJogo"], obj["numero"])
        webhook = DiscordWebhook(
            url="https://discord.com/api/webhooks/1331260605683990550/K6IqS74h0gAwuqvX4irG_5HuZ7FHc5TYL9TS8OlSfaRYCsFFTQAbAm3RlL2ZD7X6wX8i")
        embed = DiscordEmbed(title="Resultado Loterias 2025 - Ilotto", description="Resultados de Loterias", color=concurso_config["cor"])
        embed.set_timestamp()

        # add fields to embed
        embed.add_embed_field(name="Acumulado", value=obj["acumulado"])
        embed.add_embed_field(name="Data de Apuração", value=obj["dataApuracao"])
        embed.add_embed_field(name="Próximo Concurso", value=obj["dataProximoConcurso"])
        embed.add_embed_field(name="Dezenas Sorteadas", value=str(obj["dezenasSorteadasOrdemSorteio"]))
        embed.add_embed_field(name="Concurso", value=obj["numero"])
        embed.add_embed_field(name="Tipo de Jogo", value=obj["tipoJogo"])

        if concurso_config["ultimoNumero"] !=obj["numero"]:
            concurso_config["ultimoNumero"] =obj["numero"]

            # add embed object to webhook
            webhook.add_embed(embed)
            response = webhook.execute()

    time.sleep(15)

