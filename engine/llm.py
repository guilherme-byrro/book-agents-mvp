"""
LLM Engine - Interface with Ollama for AI-powered content generation
"""

import requests
import json
import yaml
from pathlib import Path
import time

class LLMEngine:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        self.config = self._load_config(config_path)
        self.base_url = "http://localhost:11434"  # Default Ollama URL
        self.model = self.config.get('provider', {}).get('model', 'llama3.1')
        
    def _load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            return {'provider': {'name': 'ollama', 'model': 'llama3.1'}}
    
    def generate(self, prompt, max_tokens=800, temperature=0.7, timeout=120):
        """Generate text using Ollama with improved error handling"""
        
        # First, ensure model is loaded
        if not self._ensure_model_loaded():
            print("⚠️ Modelo não pôde ser carregado, usando fallback...")
            return self._fallback_response(prompt)
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }
            
            print(f"🤖 Gerando com {self.model}... (timeout: {timeout}s)")
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                
                if generated_text and len(generated_text) > 50:
                    print(f"✅ Geração concluída! ({len(generated_text)} caracteres)")
                    return generated_text
                else:
                    print("⚠️ Resposta muito curta, usando fallback...")
                    return self._fallback_response(prompt)
            else:
                print(f"❌ Ollama API error: {response.status_code}")
                return self._fallback_response(prompt)
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout após {timeout}s. Ollama pode estar sobrecarregado.")
            return self._fallback_response(prompt)
        except requests.exceptions.ConnectionError:
            print("🔌 Não foi possível conectar ao Ollama. Está rodando?")
            return self._fallback_response(prompt)
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return self._fallback_response(prompt)
    
    def _ensure_model_loaded(self):
        """Ensure the model is loaded in Ollama"""
        try:
            # Check if model exists
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code != 200:
                return False
            
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            
            # Check if our model is in the list
            model_found = any(self.model in name for name in model_names)
            
            if not model_found:
                print(f"⚠️ Modelo {self.model} não encontrado. Modelos disponíveis: {model_names}")
                return False
            
            # Try to load/warm up the model with a simple prompt
            test_payload = {
                "model": self.model,
                "prompt": "Olá",
                "stream": False,
                "options": {"num_predict": 5}
            }
            
            test_response = requests.post(
                f"{self.base_url}/api/generate",
                json=test_payload,
                timeout=30
            )
            
            return test_response.status_code == 200
            
        except Exception as e:
            print(f"⚠️ Erro ao verificar modelo: {e}")
            return False
    
    def _fallback_response(self, prompt):
        """Enhanced fallback response when Ollama is not available"""
        
        # Extract key information from prompt
        if "BRIEF DA CENA:" in prompt:
            brief_start = prompt.find("BRIEF DA CENA:") + len("BRIEF DA CENA:")
            brief_end = prompt.find("\n\n", brief_start)
            if brief_end == -1:
                brief_end = brief_start + 200
            brief = prompt[brief_start:brief_end].strip()
        else:
            brief = "cena não especificada"
        
        return f"""[Gerado com fallback - Ollama indisponível]

**Cena baseada no brief:** {brief}

O ambiente estava carregado de expectativa. A atmosfera densa prenunciava que algo importante estava prestes a acontecer.

Os personagens se encontraram no local combinado, cada um trazendo suas próprias motivações e segredos. Havia uma tensão palpável no ar, como se as palavras não ditas pesassem mais do que aquelas que seriam pronunciadas.

"Precisamos conversar," disse uma voz, quebrando o silêncio.

"Eu sei," veio a resposta, carregada de significado.

O diálogo que se seguiu revelou camadas de complexidade que nenhum dos dois havia antecipado. Cada palavra trocada os aproximava mais de uma verdade que ambos temiam e desejavam ao mesmo tempo.

Quando o encontro chegou ao fim, ambos sabiam que nada seria como antes. As decisões tomadas naquele momento ecoariam por muito tempo, moldando o futuro de maneiras que ainda não conseguiam compreender completamente.

*[Nota: Para obter conteúdo gerado por IA, certifique-se de que o Ollama está rodando e o modelo {self.model} está disponível]*"""
    
    def is_available(self):
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self):
        """Get list of available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [m.get('name', '') for m in models]
            return []
        except:
            return []
