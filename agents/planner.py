"""
Planner Agent - Creates structured plans for scenes based on briefs
"""

class Planner:
    def __init__(self, project_data):
        self.project_data = project_data
        self.style_guide = project_data.get('style_guide', '')
        self.characters = project_data.get('characters', '')
        self.world = project_data.get('world', '')
        self.timeline = project_data.get('timeline', '')
    
    def plan_scene(self, brief):
        """Create a structured plan for the scene based on the brief"""
        
        # Analyze the brief
        elements = self._extract_elements(brief)
        
        # Create scene structure
        plan = self._create_scene_structure(elements, brief)
        
        return plan
    
    def _extract_elements(self, brief):
        """Extract key narrative elements from the brief"""
        elements = {
            'characters': [],
            'setting': '',
            'mood': '',
            'conflict_type': '',
            'time_period': '',
            'weather': '',
            'action': ''
        }
        
        brief_lower = brief.lower()
        
        # Characters - more flexible detection
        if 'ivana' in brief_lower:
            elements['characters'].append('Ivana')
        if 'dr. manoel' in brief_lower or 'manoel' in brief_lower or 'dr manoel' in brief_lower:
            elements['characters'].append('Dr. Manoel')
        if 'pai' in brief_lower and 'filha' in brief_lower:
            elements['characters'].extend(['Pai', 'Filha'])
        
        # Setting - more locations
        if 'masp' in brief_lower:
            elements['setting'] = 'MASP - Museu de Arte de São Paulo'
        elif 'biblioteca' in brief_lower:
            elements['setting'] = 'Biblioteca antiga'
        elif 'café' in brief_lower:
            elements['setting'] = 'Café em São Paulo'
        elif 'metrô' in brief_lower or 'metro' in brief_lower:
            elements['setting'] = 'Estação de metrô'
        
        # Mood and atmosphere
        if 'tenso' in brief_lower:
            elements['mood'] = 'tenso'
        elif 'suspense' in brief_lower:
            elements['mood'] = 'suspense'
        elif 'emotivo' in brief_lower:
            elements['mood'] = 'emotivo'
        elif 'ação' in brief_lower or 'acao' in brief_lower:
            elements['mood'] = 'ação'
        
        # Conflict type
        if 'encontro' in brief_lower:
            elements['conflict_type'] = 'encontro/confronto'
        elif 'discussão' in brief_lower or 'discutindo' in brief_lower:
            elements['conflict_type'] = 'discussão'
        elif 'diálogo' in brief_lower or 'dialogo' in brief_lower:
            elements['conflict_type'] = 'diálogo'
        
        # Time and weather
        if 'noite' in brief_lower:
            elements['time_period'] = 'noite'
        elif 'dia' in brief_lower:
            elements['time_period'] = 'dia'
        elif 'tarde' in brief_lower:
            elements['time_period'] = 'tarde'
        elif 'manhã' in brief_lower or 'manha' in brief_lower:
            elements['time_period'] = 'manhã'
            
        if 'chuvosa' in brief_lower or 'chuva' in brief_lower:
            elements['weather'] = 'chuva'
        elif 'sol' in brief_lower or 'ensolarado' in brief_lower:
            elements['weather'] = 'sol'
        
        # Action/activity
        if 'rush' in brief_lower or 'lotado' in brief_lower:
            elements['action'] = 'movimento intenso'
        elif 'vazio' in brief_lower or 'silencioso' in brief_lower:
            elements['action'] = 'ambiente calmo'
        
        return elements
    
    def _create_scene_structure(self, elements, brief):
        """Create a structured plan for the scene"""
        
        plan_parts = []
        
        # Scene setup
        plan_parts.append("## ESTRUTURA DA CENA")
        plan_parts.append(f"\n**Brief Original:** {brief}")
        
        plan_parts.append("\n### 1. AMBIENTAÇÃO")
        plan_parts.append(f"- **Local**: {elements['setting'] or 'Local a definir'}")
        plan_parts.append(f"- **Período**: {elements['time_period'] or 'Período a definir'}")
        plan_parts.append(f"- **Clima**: {elements['weather'] or 'Clima neutro'}")
        plan_parts.append(f"- **Atmosfera**: {elements['mood'] or 'Atmosfera neutra'}")
        if elements['action']:
            plan_parts.append(f"- **Movimento**: {elements['action']}")
        
        # Characters
        plan_parts.append("\n### 2. PERSONAGENS")
        if elements['characters']:
            for char in elements['characters']:
                plan_parts.append(f"- {char}")
        else:
            plan_parts.append("- Personagens a definir")
        
        # Scene progression - dynamic based on elements
        plan_parts.append("\n### 3. PROGRESSÃO NARRATIVA")
        
        if elements['mood'] == 'tenso' and elements['weather'] == 'chuva':
            plan_parts.append("1. **Abertura atmosférica**: Estabelecer ambiente tenso com chuva")
            plan_parts.append("2. **Chegada dos personagens**: Entrada gradual, criando expectativa")
            plan_parts.append("3. **Confronto inicial**: Primeiras palavras carregadas de tensão")
            plan_parts.append("4. **Escalada da tensão**: Revelações e posicionamentos")
            plan_parts.append("5. **Clímax do encontro**: Momento de maior intensidade")
            plan_parts.append("6. **Resolução/gancho**: Desfecho que mantém suspense")
        elif elements['mood'] == 'emotivo':
            plan_parts.append("1. **Ambientação emotiva**: Estabelecer cenário íntimo")
            plan_parts.append("2. **Encontro dos personagens**: Aproximação gradual")
            plan_parts.append("3. **Abertura emocional**: Primeiras palavras sinceras")
            plan_parts.append("4. **Desenvolvimento**: Aprofundamento da conversa")
            plan_parts.append("5. **Clímax emocional**: Momento de maior vulnerabilidade")
            plan_parts.append("6. **Resolução**: Conexão ou separação definitiva")
        elif elements['mood'] == 'ação':
            plan_parts.append("1. **Setup dinâmico**: Estabelecer ambiente de movimento")
            plan_parts.append("2. **Incidente inicial**: Evento que desencadeia a ação")
            plan_parts.append("3. **Escalada**: Intensificação da situação")
            plan_parts.append("4. **Complicações**: Obstáculos e desafios")
            plan_parts.append("5. **Clímax de ação**: Momento de maior intensidade")
            plan_parts.append("6. **Resolução**: Consequências e desfecho")
        else:
            # Generic structure
            plan_parts.append("1. **Abertura**: Estabelecer cenário e atmosfera")
            plan_parts.append("2. **Desenvolvimento**: Introdução dos personagens")
            plan_parts.append("3. **Conflito**: Tensão ou situação central")
            plan_parts.append("4. **Desenvolvimento**: Aprofundamento da situação")
            plan_parts.append("5. **Clímax**: Momento decisivo")
            plan_parts.append("6. **Resolução**: Desfecho da cena")
        
        # Technical notes - adapted to mood
        plan_parts.append("\n### 4. ELEMENTOS TÉCNICOS")
        plan_parts.append("- **Foco narrativo**: Terceira pessoa onisciente")
        
        if elements['mood'] == 'tenso':
            plan_parts.append("- **Ritmo**: Lento e deliberado, construindo tensão")
            plan_parts.append("- **Recursos**: Descrição sensorial, silêncios significativos")
        elif elements['mood'] == 'ação':
            plan_parts.append("- **Ritmo**: Rápido e dinâmico")
            plan_parts.append("- **Recursos**: Frases curtas, verbos de ação")
        elif elements['mood'] == 'emotivo':
            plan_parts.append("- **Ritmo**: Pausado e reflexivo")
            plan_parts.append("- **Recursos**: Introspecção, detalhes emotivos")
        else:
            plan_parts.append("- **Ritmo**: Equilibrado")
            plan_parts.append("- **Recursos**: Descrição equilibrada")
        
        plan_parts.append("- **Diálogos**: Naturais e adequados ao tom da cena")
        
        return '\n'.join(plan_parts)
