import requests

# Configurações
BASE_URL = "https://datathon-api-ljhdg.ondigitalocean.app"

def test_api():
    print("🧪 Testando API...")
    
    try:
        # 1. Health Check
        print("1. Health check...")
        response = requests.get(f"{BASE_URL}/")
        print(f"   ✅ Status: {response.status_code}")
        
        # 2. Health detalhado
        print("2. Health detalhado...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Config: {response.json()}")
        
        # 3. Listar vagas
        print("3. Listando vagas...")
        response = requests.get(f"{BASE_URL}/vagas/")
        print(f"   ✅ Status: {response.status_code}")
        vagas = response.json()
        print(f"   📋 Total de vagas: {vagas.get('total', 0)}")
        
        # 4. Teste LLM simples
        print("4. Teste LLM simples...")
        response = requests.post(f"{BASE_URL}/llm/test")
        print(f"   ✅ Status: {response.status_code}")
        print(f"   🤖 Result: {response.json()}")
        
        print("🎉 Todos os testes passaram!")
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")

if __name__ == "__main__":
    test_api()