#!/usr/bin/env python3
"""
Book Agents MVP - Gradio Web Interface
Simple web interface for generating book content using AI agents.
"""

import gradio as gr
import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.writer import Writer
from agents.editor import Editor
from agents.planner import Planner

def load_project_data():
    """Load project data files (characters, world, style guide, etc.)"""
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

def generate_scene(brief_text, include_plan=True, include_draft=True):
    """Generate scene content based on brief"""
    if not brief_text.strip():
        return "❌ Por favor, forneça um brief para a cena.", "", "", ""
    
    try:
        # Load project data
        project_data = load_project_data()
        
        # Initialize agents
        planner = Planner(project_data)
        writer = Writer(project_data)
        editor = Editor(project_data)
        
        # Step 1: Plan the scene
        status_update = "🎯 Planejando a cena..."
        scene_plan = planner.plan_scene(brief_text)
        
        # Step 2: Write the scene
        status_update = "✍️ Escrevendo a cena..."
        scene_content = writer.write_scene(brief_text, scene_plan)
        
        # Step 3: Edit and refine
        status_update = "✨ Editando e refinando..."
        final_content = editor.edit_scene(scene_content, brief_text, scene_plan)
        
        # Save output
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"scene_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Cena Gerada\n\n**Brief:** {brief_text}\n\n")
            if include_plan:
                f.write(f"## Plano da Cena\n\n{scene_plan}\n\n")
            if include_draft:
                f.write(f"## Primeira Versão\n\n{scene_content}\n\n")
            f.write(f"## Versão Final\n\n{final_content}\n")
        
        success_msg = f"✅ Cena gerada com sucesso!\n📁 Salva em: {output_file}"
        
        return (
            success_msg,
            scene_plan if include_plan else "",
            scene_content if include_draft else "",
            final_content
        )
        
    except Exception as e:
        error_msg = f"❌ Erro ao gerar cena: {str(e)}"
        return error_msg, "", "", ""

def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(
        title="Book Agents MVP",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        """
    ) as interface:
        
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>📚 Book Agents MVP</h1>
            <p>Gerador de conteúdo narrativo usando agentes de IA</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.HTML("<h3>📝 Configuração</h3>")
                
                brief_input = gr.Textbox(
                    label="Brief da Cena",
                    placeholder="Ex: Escreva um encontro tenso no MASP entre Ivana e Dr. Manoel, noite chuvosa.",
                    lines=3,
                    max_lines=5
                )
                
                with gr.Row():
                    include_plan = gr.Checkbox(
                        label="Incluir plano da cena",
                        value=True
                    )
                    include_draft = gr.Checkbox(
                        label="Incluir primeira versão",
                        value=True
                    )
                
                generate_btn = gr.Button(
                    "🚀 Gerar Cena",
                    variant="primary",
                    size="lg"
                )
                
                status_output = gr.Textbox(
                    label="Status",
                    interactive=False,
                    lines=3
                )
            
            with gr.Column(scale=2):
                # Output section
                gr.HTML("<h3>📖 Resultado</h3>")
                
                with gr.Tabs():
                    with gr.TabItem("📚 Versão Final"):
                        final_output = gr.Textbox(
                            label="Cena Final",
                            lines=15,
                            max_lines=25,
                            interactive=False
                        )
                    
                    with gr.TabItem("📋 Plano da Cena"):
                        plan_output = gr.Textbox(
                            label="Plano Estrutural",
                            lines=15,
                            max_lines=25,
                            interactive=False
                        )
                    
                    with gr.TabItem("✍️ Primeira Versão"):
                        draft_output = gr.Textbox(
                            label="Rascunho Inicial",
                            lines=15,
                            max_lines=25,
                            interactive=False
                        )
        
        # Examples
        gr.HTML("<h3>💡 Exemplos de Briefs</h3>")
        gr.Examples(
            examples=[
                ["Escreva um encontro tenso no MASP entre Ivana e Dr. Manoel, noite chuvosa."],
                ["Crie uma cena de suspense em uma biblioteca antiga, com dois personagens discutindo um segredo."],
                ["Descreva um diálogo emotivo entre pai e filha em um café movimentado de São Paulo."],
                ["Escreva uma cena de ação em um metrô lotado durante o horário de rush."],
            ],
            inputs=[brief_input]
        )
        
        # Event handlers
        generate_btn.click(
            fn=generate_scene,
            inputs=[brief_input, include_plan, include_draft],
            outputs=[status_output, plan_output, draft_output, final_output]
        )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; border-top: 1px solid #eee;">
            <p>🤖 Powered by AI Agents | 📝 Writer • 🎯 Planner • ✨ Editor</p>
        </div>
        """)
    
    return interface

def main():
    """Launch the Gradio interface"""
    interface = create_interface()
    
    print("🚀 Iniciando Book Agents MVP...")
    print("📱 Interface web disponível em: http://localhost:7860")
    print("🔗 Para acessar externamente, use: http://0.0.0.0:7860")
    print("\n💡 Dica: Use Ctrl+C para parar o servidor")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True if you want a public link
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()
