import requests
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuración de Slack
slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

# IDs de canal para las conversaciones directas de las cinco personas
person_1_channel_id = os.environ.get("PERSON_1_CHANNEL_ID")
person_2_channel_id = os.environ.get("PERSON_2_CHANNEL_ID")
person_3_channel_id = os.environ.get("PERSON_3_CHANNEL_ID")
person_4_channel_id = os.environ.get("PERSON_4_CHANNEL_ID")
person_5_channel_id = os.environ.get("PERSON_5_CHANNEL_ID")

# Lista de URLs a monitorear
urls = ["https://thebotdev.com/", "https://repuestosus.com/", "https://wotdev.com/"]

def verificar_sitio(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - El sitio {url} está activo.\n"
            )
        else:
            message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - El sitio {url} está inactivo. Código de estado: {response.status_code}\n"
            enviar_mensaje_slack(message)
    except requests.RequestException as e:
        message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - No se pudo acceder al sitio {url}. Error: {e}\n"
        enviar_mensaje_slack(message)

def enviar_mensaje_slack(message):
    channel_ids = [
        person_1_channel_id,
        person_2_channel_id,
        person_3_channel_id,
        person_4_channel_id,
        person_5_channel_id,
    ]

    for channel_id in channel_ids:
        try:
            client.chat_postMessage(channel=channel_id, text=message)
            print(f"Mensaje enviado a Slack con éxito al canal {channel_id}.")
        except SlackApiError as e:
            print(f"Error al enviar mensaje a Slack: {e.response['error']}")

def lambda_handler(event, context):
    for url in urls:
        verificar_sitio(url)
    return {
        'statusCode': 200,
        'body': 'Website monitoring executed successfully'
    }

# Este script monitorea 3 sitios web y envía mensajes según corresponda.
# Ahora envía notificaciones a cinco personas en Slack.
# Además, realiza la verificación cada 2 horas mientras la terminal esté abierta.
