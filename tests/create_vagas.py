import requests
import json

# Configuração
API_URL = "https://datathon-api-ljhdg.ondigitalocean.app/vagas/"  

# Carregar vagas
with open('vagas.json', 'r', encoding='utf-8') as f:
    vagas = json.load(f)

# Cadastrar cada vaga
for i, vaga in enumerate(vagas, 1):
    try:
        response = requests.post(API_URL, json=vaga)
        if response.status_code == 201:
            print(f"✅ Vaga {i}/30 cadastrada: {vaga['titulo_vaga']}")
        else:
            print(f"❌ Erro na vaga {i}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erro na vaga {i}: {str(e)}")

print("🎉 Processo de cadastro concluído!")