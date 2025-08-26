#!/usr/bin/env python3
"""
Ollama Diagnostic Script - Check Ollama status and troubleshoot issues
"""

import requests
import json
import yaml
import time
from pathlib import Path

def load_config():
    """Load configuration"""
    config_path = Path(__file__).parent / "config.yaml"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar config.yaml: {e}")
        return None

def check_ollama_service():
    """Check if Ollama service is running"""
    print("🔍 Verificando se Ollama está rodando...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está rodando!")
            return True
        else:
            print(f"❌ Ollama respondeu com status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao Ollama na porta 11434")
        print("💡 Certifique-se de que o Ollama está rodando: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def list_available_models():
    """List available models"""
    print("\n📋 Verificando modelos disponíveis...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            if models:
                print(f"✅ {len(models)} modelo(s) encontrado(s):")
                for model in models:
                    name = model.get('name', 'N/A')
                    size = model.get('size', 0)
                    size_mb = size / (1024 * 1024) if size else 0
                    print(f"   - {name} ({size_mb:.1f} MB)")
                return [m.get('name', '') for m in models]
            else:
                print("⚠️ Nenhum modelo encontrado!")
                print("💡 Instale um modelo: ollama pull llama3.1")
                return []
        else:
            print(f"❌ Erro ao listar modelos: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")
        return []

def check_configured_model(config):
    """Check if configured model is available"""
    if not config:
        return False
    
    configured_model = config.get('provider', {}).get('model', 'llama3.1')
    print(f"\n🎯 Verificando modelo configurado: {configured_model}")
    
    available_models = list_available_models()
    
    # Check if configured model is in available models
    model_found = any(configured_model in model for model in available_models)
    
    if model_found:
        print(f"✅ Modelo {configured_model} está disponível!")
        return True
    else:
        print(f"❌ Modelo {configured_model} não encontrado!")
        print(f"💡 Instale o modelo: ollama pull {configured_model}")
        return False

def test_model_generation(model_name):
    """Test model generation with a simple prompt"""
    print(f"\n🧪 Testando geração com {model_name}...")
    
    test_payload = {
        "model": model_name,
        "prompt": "Escreva uma frase simples sobre o tempo.",
        "stream": False,
        "options": {
            "num_predict": 50,
            "temperature": 0.7
        }
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=test_payload,
            timeout=60
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('response', '').strip()
            duration = end_time - start_time
            
            print(f"✅ Teste bem-sucedido! ({duration:.1f}s)")
            print(f"📝 Resposta: {generated_text[:100]}...")
            return True
        else:
            print(f"❌ Erro na geração: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout! O modelo pode estar sobrecarregado ou muito lento.")
        print("💡 Tente um modelo menor ou aumente o timeout.")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def provide_recommendations():
    """Provide troubleshooting recommendations"""
    print("\n🔧 RECOMENDAÇÕES DE TROUBLESHOOTING:")
    print()
    print("1. **Iniciar Ollama:**")
    print("   ollama serve")
    print()
    print("2. **Instalar modelo (se necessário):**")
    print("   ollama pull llama3.1")
    print("   ollama pull llama3.1:8b  # versão menor")
    print()
    print("3. **Verificar modelos instalados:**")
    print("   ollama list")
    print()
    print("4. **Testar modelo manualmente:**")
    print("   ollama run llama3.1")
    print()
    print("5. **Se o modelo for muito lento:**")
    print("   - Use um modelo menor (llama3.1:8b)")
    print("   - Aumente a RAM disponível")
    print("   - Feche outros programas pesados")
    print()
    print("6. **Verificar logs do Ollama:**")
    print("   - Windows: %USERPROFILE%\\.ollama\\logs")
    print("   - Linux/Mac: ~/.ollama/logs")

def main():
    """Main diagnostic function"""
    print("🚀 DIAGNÓSTICO DO OLLAMA")
    print("=" * 50)
    
    # Load config
    config = load_config()
    if config:
        model_name = config.get('provider', {}).get('model', 'llama3.1')
        print(f"📋 Modelo configurado: {model_name}")
    else:
        model_name = 'llama3.1'
        print("⚠️ Usando modelo padrão: llama3.1")
    
    # Check Ollama service
    if not check_ollama_service():
        provide_recommendations()
        return
    
    # List models
    available_models = list_available_models()
    
    # Check configured model
    if not check_configured_model(config):
        provide_recommendations()
        return
    
    # Test generation
    if not test_model_generation(model_name):
        provide_recommendations()
        return
    
    print("\n🎉 DIAGNÓSTICO CONCLUÍDO!")
    print("✅ Ollama está funcionando corretamente!")
    print("🚀 Você pode usar os agentes com IA agora!")

if __name__ == "__main__":
    main()
