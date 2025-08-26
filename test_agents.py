#!/usr/bin/env python3
"""
Test script to debug the agents and identify issues
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.writer import Writer
from agents.editor import Editor
from agents.planner import Planner

def load_project_data():
    """Load project data files"""
    data = {}
    data_dir = project_root / "data"
    
    # Load style guide
    style_guide_path = data_dir / "style_guide.md"
    if style_guide_path.exists():
        with open(style_guide_path, 'r', encoding='utf-8') as f:
            data['style_guide'] = f.read()
    
    # Load canon data
    canon_dir = data_dir / "canon"
    if canon_dir.exists():
        for file_path in canon_dir.glob("*.md"):
            with open(file_path, 'r', encoding='utf-8') as f:
                data[file_path.stem] = f.read()
    
    return data

def test_agents():
    """Test each agent individually"""
    print("🧪 Testando os agentes...")
    
    # Load data
    project_data = load_project_data()
    print(f"📚 Dados do projeto carregados: {list(project_data.keys())}")
    
    # Test brief
    brief = "Escreva um encontro tenso no MASP entre Ivana e Dr. Manoel, noite chuvosa."
    print(f"📝 Brief: {brief}")
    
    # Test Planner
    print("\n🎯 Testando Planner...")
    try:
        planner = Planner(project_data)
        scene_plan = planner.plan_scene(brief)
        print(f"✅ Planner funcionou! Tamanho do plano: {len(scene_plan)} caracteres")
        print(f"📋 Plano (primeiros 200 chars): {scene_plan[:200]}...")
    except Exception as e:
        print(f"❌ Erro no Planner: {e}")
        return
    
    # Test Writer
    print("\n✍️ Testando Writer...")
    try:
        writer = Writer(project_data)
        
        # Debug: test _analyze_brief
        elements = writer._analyze_brief(brief)
        print(f"🔍 Elementos extraídos: {elements}")
        
        # Test write_scene
        scene_content = writer.write_scene(brief, scene_plan)
        print(f"✅ Writer funcionou! Tamanho do conteúdo: {len(scene_content)} caracteres")
        
        if scene_content:
            print(f"📖 Conteúdo (primeiros 200 chars): {scene_content[:200]}...")
        else:
            print("⚠️ PROBLEMA: Writer retornou conteúdo vazio!")
            
            # Debug further
            print("🔍 Debugando Writer...")
            print(f"   - Elementos: {elements}")
            
            # Test _generate_scene_content directly
            test_content = writer._generate_scene_content(elements, scene_plan)
            print(f"   - Conteúdo direto: {len(test_content)} chars")
            if test_content:
                print(f"   - Preview: {test_content[:100]}...")
            
    except Exception as e:
        print(f"❌ Erro no Writer: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test Editor
    print("\n✨ Testando Editor...")
    try:
        editor = Editor(project_data)
        final_content = editor.edit_scene(scene_content, brief, scene_plan)
        print(f"✅ Editor funcionou! Tamanho do conteúdo final: {len(final_content)} caracteres")
        
        if final_content:
            print(f"📚 Conteúdo final (primeiros 200 chars): {final_content[:200]}...")
        else:
            print("⚠️ PROBLEMA: Editor retornou conteúdo vazio!")
            
    except Exception as e:
        print(f"❌ Erro no Editor: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n🎉 Teste completo!")

if __name__ == "__main__":
    test_agents()
