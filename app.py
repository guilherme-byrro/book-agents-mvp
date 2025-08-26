#!/usr/bin/env python3
"""
Book Agents MVP - Main Application
Coordinates writing agents to generate book content based on briefs.
"""

import argparse
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import yaml

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.writer import Writer
from agents.editor import Editor
from agents.planner import Planner

console = Console()

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

def process_brief(brief_text, project_data):
    """Process a writing brief and generate content"""
    console.print(Panel(f"[bold blue]Processando brief:[/bold blue]\n{brief_text}", 
                       title=" Brief", border_style="blue"))
    
    # Initialize agents
    planner = Planner(project_data)
    writer = Writer(project_data)
    editor = Editor(project_data)
    
    # Step 1: Plan the scene
    console.print("\n[yellow] Planejando a cena...[/yellow]")
    scene_plan = planner.plan_scene(brief_text)
    console.print(Panel(scene_plan, title=" Plano da Cena", border_style="yellow"))
    
    # Step 2: Write the scene
    console.print("\n[green] Escrevendo a cena...[/green]")
    scene_content = writer.write_scene(brief_text, scene_plan)
    console.print(Panel(scene_content, title=" Cena Escrita", border_style="green"))
    
    # Step 3: Edit and refine
    console.print("\n[magenta] Editando e refinando...[/magenta]")
    final_content = editor.edit_scene(scene_content, brief_text, scene_plan)
    console.print(Panel(final_content, title=" Versão Final", border_style="magenta"))
    
    return final_content

def save_output(content, output_file=None):
    """Save generated content to file"""
    if not output_file:
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "generated_scene.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    console.print(f"\n[bold green] Conteúdo salvo em: {output_file}[/bold green]")

def main():
    parser = argparse.ArgumentParser(description="Book Agents MVP - Gerador de conteúdo de livro")
    parser.add_argument("--brief", "-b", required=True, 
                       help="Brief da cena a ser escrita")
    parser.add_argument("--output", "-o", 
                       help="Arquivo de saída (opcional)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Modo verboso")
    
    args = parser.parse_args()
    
    try:
        # Load project data
        console.print("[cyan] Carregando dados do projeto...[/cyan]")
        project_data = load_project_data()
        
        # Process the brief
        final_content = process_brief(args.brief, project_data)
        
        # Save output
        save_output(final_content, args.output)
        
        console.print("\n[bold green] Processo concluído com sucesso![/bold green]")
        
    except Exception as e:
        console.print(f"[bold red] Erro: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
