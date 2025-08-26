"""
Writer Agent - AI-powered content generation using Ollama
"""

import sys
from pathlib import Path

# Add engine to path
engine_path = Path(__file__).parent.parent / "engine"
sys.path.insert(0, str(engine_path))

from llm import LLMEngine

class Writer:
    def __init__(self, project_data):
        self.project_data = project_data
        self.style_guide = project_data.get('style_guide', '')
        self.characters = project_data.get('characters', '')
        self.world = project_data.get('world', '')
        self.timeline = project_data.get('timeline', '')
        
        # Initialize LLM engine
        self.llm = LLMEngine()
        
        # Check if Ollama is available
        if not self.llm.is_available():
            print("⚠️ Warning: Ollama não está rodando. Usando fallback rule-based.")
            self.use_fallback = True
        else:
            print("✅ Ollama conectado com sucesso!")
            self.use_fallback = False
    
    def write_scene(self, brief, scene_plan):
        """Generate scene content using AI or fallback to rule-based"""
        
        if self.use_fallback:
            return self._write_scene_fallback(brief, scene_plan)
        
        # Use AI to generate content
        return self._write_scene_ai(brief, scene_plan)
    
    def _write_scene_ai(self, brief, scene_plan):
        """Generate scene using Ollama AI"""
        
        # Build context from project data
        context_parts = []
        
        if self.style_guide:
            context_parts.append(f"GUIA DE ESTILO:\n{self.style_guide}")
        
        if self.characters:
            context_parts.append(f"PERSONAGENS:\n{self.characters}")
        
        if self.world:
            context_parts.append(f"MUNDO/CENÁRIO:\n{self.world}")
        
        context = "\n\n".join(context_parts) if context_parts else ""
        
        # Create comprehensive prompt
        prompt = f"""Você é um escritor profissional especializado em narrativa literária. Sua tarefa é escrever uma cena baseada no brief e plano fornecidos.

{context}

BRIEF DA CENA:
{brief}

PLANO ESTRUTURAL:
{scene_plan}

INSTRUÇÕES:
- Escreva uma cena narrativa completa e envolvente
- Use terceira pessoa onisciente
- Inclua descrições sensoriais detalhadas
- Desenvolva diálogos naturais e significativos
- Mantenha consistência com o estilo e personagens
- A cena deve ter entre 300-600 palavras
- Use linguagem literária em português brasileiro

CENA:"""

        try:
            # Generate content using Ollama
            scene_content = self.llm.generate(
                prompt=prompt,
                max_tokens=800,
                temperature=0.8
            )
            
            # Clean up the response
            scene_content = scene_content.strip()
            
            # Ensure we have content
            if not scene_content or len(scene_content) < 50:
                print("⚠️ AI gerou conteúdo muito curto, usando fallback...")
                return self._write_scene_fallback(brief, scene_plan)
            
            return scene_content
            
        except Exception as e:
            print(f"❌ Erro na geração AI: {e}")
            return self._write_scene_fallback(brief, scene_plan)
    
    def _write_scene_fallback(self, brief, scene_plan):
        """Fallback rule-based content generation"""
        
        # Extract key elements from the brief
        scene_elements = self._analyze_brief(brief)
        
        # Generate the scene using rules
        scene_content = self._generate_scene_content(scene_elements, scene_plan, brief)
        
        return scene_content
    
    def _analyze_brief(self, brief):
        """Analyze the brief to extract key elements (fallback method)"""
        elements = {
            'setting': '',
            'characters': [],
            'mood': '',
            'time': '',
            'weather': '',
            'action': ''
        }
        
        brief_lower = brief.lower()
        
        # Extract setting
        if 'masp' in brief_lower:
            elements['setting'] = 'MASP (Museu de Arte de São Paulo)'
        elif 'biblioteca' in brief_lower:
            elements['setting'] = 'biblioteca antiga'
        elif 'café' in brief_lower:
            elements['setting'] = 'café movimentado'
        elif 'metrô' in brief_lower or 'metro' in brief_lower:
            elements['setting'] = 'estação de metrô'
        
        # Extract characters
        if 'ivana' in brief_lower:
            elements['characters'].append('Ivana')
        if 'dr. manoel' in brief_lower or 'manoel' in brief_lower or 'dr manoel' in brief_lower:
            elements['characters'].append('Dr. Manoel')
        if 'pai' in brief_lower and 'filha' in brief_lower:
            elements['characters'].extend(['pai', 'filha'])
        
        # Extract mood/atmosphere
        if 'tenso' in brief_lower:
            elements['mood'] = 'tenso'
        elif 'suspense' in brief_lower:
            elements['mood'] = 'suspense'
        elif 'emotivo' in brief_lower:
            elements['mood'] = 'emotivo'
        elif 'ação' in brief_lower or 'acao' in brief_lower:
            elements['mood'] = 'ação'
        
        # Extract time
        if 'noite' in brief_lower:
            elements['time'] = 'noite'
        elif 'dia' in brief_lower:
            elements['time'] = 'dia'
        elif 'tarde' in brief_lower:
            elements['time'] = 'tarde'
        elif 'manhã' in brief_lower or 'manha' in brief_lower:
            elements['time'] = 'manhã'
        
        # Extract weather
        if 'chuvosa' in brief_lower or 'chuva' in brief_lower:
            elements['weather'] = 'chuva'
        elif 'sol' in brief_lower:
            elements['weather'] = 'sol'
        
        # Extract action/activity
        if 'encontro' in brief_lower:
            elements['action'] = 'encontro'
        elif 'discussão' in brief_lower or 'discutindo' in brief_lower:
            elements['action'] = 'discussão'
        elif 'diálogo' in brief_lower or 'dialogo' in brief_lower:
            elements['action'] = 'diálogo'
        elif 'rush' in brief_lower or 'lotado' in brief_lower:
            elements['action'] = 'movimento intenso'
        
        return elements
    
    def _generate_scene_content(self, elements, scene_plan, brief):
        """Generate content using rule-based approach (fallback)"""
        
        content = []
        
        # Atmospheric opening
        if elements['weather'] == 'chuva' and 'MASP' in elements.get('setting', ''):
            content.append("A chuva tamborilava contra as grandes janelas do MASP, criando um ritmo hipnótico que ecoava pelos corredores vazios do museu. As luzes da Paulista se difundiam através das gotas d'água, pintando sombras dançantes nas paredes brancas.")
        elif elements['weather'] == 'chuva':
            content.append(f"A chuva caía pesadamente sobre a cidade, criando uma cortina de água que transformava {elements['setting']} em um refúgio isolado do mundo exterior.")
        elif elements['setting']:
            if 'MASP' in elements['setting']:
                content.append("O MASP se erguia majestoso na Paulista, suas linhas modernas contrastando com o movimento constante da avenida. No interior, o silêncio era quebrado apenas pelos passos ecoando no piso de concreto polido.")
            elif 'café' in elements['setting']:
                content.append("O café fervilhava de atividade, o aroma intenso misturando-se às conversas sobrepostas e ao tinir constante de xícaras e pratos.")
            elif 'biblioteca' in elements['setting']:
                content.append("A biblioteca antiga exalava o cheiro característico de livros velhos e madeira envelhecida. A luz filtrada pelas janelas altas criava um ambiente solene e contemplativo.")
            elif 'metrô' in elements['setting']:
                content.append("A estação de metrô pulsava com o movimento incessante de pessoas. O som dos trens chegando e partindo criava uma sinfonia urbana constante.")
        else:
            content.append("O ambiente estava carregado de expectativa, como se algo importante estivesse prestes a acontecer.")
        
        # Character interactions
        if 'Ivana' in elements['characters'] and 'Dr. Manoel' in elements['characters']:
            content.extend([
                "\nIvana chegou primeiro, seus passos ecoando no espaço. Dr. Manoel apareceu momentos depois, o semblante grave.",
                '\n"Você veio," disse Ivana.',
                '\n"Tinha que vir," respondeu Dr. Manoel. "Precisamos resolver isso."',
                '\nO silêncio se estendeu entre eles, carregado de tensão.',
                '\n"Então você sabe a verdade," ela disse.',
                '\n"Sei mais do que você imagina," ele respondeu, dando um passo à frente.'
            ])
        elif 'pai' in elements['characters'] and 'filha' in elements['characters']:
            content.extend([
                "\nO pai chegou pontualmente, como sempre. Sua filha já estava lá, mexendo nervosamente no celular, evitando o olhar direto que sabia que viria.",
                '\nQuando seus olhos finalmente se encontraram, ambos souberam que aquela conversa não poderia ser adiada por mais tempo.'
            ])
        else:
            content.append("\nOs personagens se encontraram, cada um carregando suas próprias intenções. A conversa que se seguiu revelaria verdades há muito escondidas.")
        
        # Closing
        if elements['weather'] == 'chuva':
            content.append("\nLá fora, a chuva continuava caindo, mas algo havia mudado entre eles. O que aconteceria a seguir dependeria das escolhas que cada um faria.")
        elif elements['mood'] == 'tenso':
            content.append("\nO encontro chegava ao fim, mas as questões levantadas ecoariam por muito tempo. Algumas palavras, uma vez ditas, não podem ser desfeitas.")
        else:
            content.append("\nQuando se separaram, ambos sabiam que nada seria como antes. As palavras trocadas ecoariam por muito tempo.")
        
        return '\n'.join(content)
