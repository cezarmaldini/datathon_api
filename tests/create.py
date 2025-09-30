import requests
import json
from datetime import date

url = "http://localhost:8001/vagas/"

vaga = {
    "data_requisicao": str(date.today()),
    "titulo_vaga": "Desenvolvedor Python Júnior",
    "tipo_contratacao": "CLT",
    "vaga_pcd": False,
    "cidade": "São Paulo",
    "estado": "SP",
    "pais": "Brasil",
    "nivel_profissional": "Júnior",
    "nivel_academico": "Superior",
    "areas_atuacao": ["TI", "Desenvolvimento"],
    "principais_atividades": "Desenvolvimento de aplicações Python com FastAPI",
    "competencias_tecnicas": ["Python", "FastAPI", "PostgreSQL"],
    "habilidades_comportamentais": ["Trabalho em equipe", "Comunicação"],
    "modalidade": "Remoto"
}

response = requests.post(url, json=vaga)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))