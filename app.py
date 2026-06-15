import json
import os
import urllib.error
import urllib.request
from flask import Flask, render_template, request
from dotenv import dotenv_values, load_dotenv

app = Flask(__name__)

DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=DOTENV_PATH, override=True)

# Prioriza o valor definido no .env do projeto, mas mantém fallback do ambiente.
WEBHOOK_URL = dotenv_values(DOTENV_PATH).get('DISCORD_WEBHOOK_URL', '').strip()
if not WEBHOOK_URL:
    WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '').strip()

@app.route('/', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        # 1. Recebendo os dados do formulário (incluindo o nome da equipe!)
        nome_equipe = request.form.get('nome_equipe')
        
        p1_nick = request.form.get('p1_nick')
        p1_id = request.form.get('p1_id')
        
        p2_nick = request.form.get('p2_nick')
        p2_id = request.form.get('p2_id')
        
        p3_nick = request.form.get('p3_nick')
        p3_id = request.form.get('p3_id')

        # 2. Montando a mensagem Embed para o Discord
        embed_data = {
            "content": "🏆 **Nova Inscrição Recebida!**", # Mensagem fora do embed que vai pingar o canal
            "embeds": [
                {
                    "title": f"Equipe: {nome_equipe}",
                    "description": "Uma nova trinca se registrou para o Torneio de Lendas do Vôlei.",
                    "color": 32768, # Cor Verde em formato decimal
                    "fields": [
                        {
                            "name": " Capitão (Jogador 1)",
                            "value": f"**Nick:** {p1_nick}\n**ID:** {p1_id}",
                            "inline": False
                        },
                        {
                            "name": " Jogador 2",
                            "value": f"**Nick:** {p2_nick}\n**ID:** {p2_id}",
                            "inline": False
                        },
                        {
                            "name": " Jogador 3",
                            "value": f"**Nick:** {p3_nick}\n**ID:** {p3_id}",
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": "Sistema de Inscrições automático"
                    }
                }
            ]
        }

        # 3. Disparando os dados para o seu canal
        if WEBHOOK_URL and 'SEU_LINK_AQUI' not in WEBHOOK_URL:
            try:
                data = json.dumps(embed_data).encode('utf-8')
                req = urllib.request.Request(
                    WEBHOOK_URL,
                    data=data,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    }
                ) 
                with urllib.request.urlopen(req) as response:
                    response.read()
                print(f"Inscrição da equipe {nome_equipe} enviada ao Discord!")
            except urllib.error.HTTPError as e:
                print("Erro ao enviar para o Discord (HTTP):", e.code, e.reason)
            except Exception as e:
                print("Erro ao enviar para o Discord:", e)
        else:
            print("Webhook do Discord não configurado. A inscrição foi registrada localmente.")

        # 4. Tela de sucesso para quem preencheu o formulário
        return f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background-color: #FFD700; margin: 0;">
            <div style="background-color: white; padding: 40px; border-radius: 12px; border-top: 8px solid #006400; text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.2);">
                <h1 style="color: #006400; font-family: sans-serif;">Inscrição Concluída!</h1>
                <p style="font-family: sans-serif; color: #333; margin-bottom: 20px;">
                    A equipe <b>{nome_equipe}</b> foi registrada com sucesso.
                </p>
                <a href="/" style="text-decoration: none; background: #006400; color: #FFD700; padding: 10px 20px; font-weight: bold; border-radius: 5px; font-family: sans-serif;">Fazer nova inscrição</a>
            </div>
        </div>
        """

    # Se a pessoa só estiver acessando o site, mostra o formulário HTML
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)

