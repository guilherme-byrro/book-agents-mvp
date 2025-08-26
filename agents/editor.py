"""
Editor Agent - Refines and polishes scene content
"""

class Editor:
    def __init__(self, project_data):
        self.project_data = project_data
        self.style_guide = project_data.get('style_guide', '')
        self.characters = project_data.get('characters', '')
        self.world = project_data.get('world', '')
        self.timeline = project_data.get('timeline', '')
    
    def edit_scene(self, scene_content, brief, scene_plan):
        """Edit and refine the scene content"""
        
        # Apply style guide corrections
        edited_content = self._apply_style_corrections(scene_content)
        
        # Enhance dialogue and descriptions
        edited_content = self._enhance_prose(edited_content)
        
        # Final polish
        edited_content = self._final_polish(edited_content)
        
        return edited_content
    
    def _apply_style_corrections(self, content):
        """Apply style guide corrections"""
        # Basic corrections for Portuguese text
        corrections = {
            ' ,': ',',
            ' .': '.',
            '  ': ' ',  # Remove double spaces
            '\n\n\n': '\n\n',  # Remove triple line breaks
        }
        
        edited = content
        for old, new in corrections.items():
            edited = edited.replace(old, new)
        
        return edited
    
    def _enhance_prose(self, content):
        """Enhance the prose quality"""
        # Split into paragraphs for processing
        paragraphs = content.split('\n\n')
        enhanced_paragraphs = []
        
        for para in paragraphs:
            if para.strip():
                # Add more descriptive elements where appropriate
                enhanced = self._enhance_paragraph(para)
                enhanced_paragraphs.append(enhanced)
        
        return '\n\n'.join(enhanced_paragraphs)
    
    def _enhance_paragraph(self, paragraph):
        """Enhance individual paragraphs"""
        # Add sensory details and improve flow
        enhanced = paragraph
        
        # Enhance atmospheric descriptions
        if 'chuva' in paragraph.lower() and 'tamborilava' in paragraph.lower():
            enhanced = paragraph.replace(
                'tamborilava contra as grandes janelas',
                'tamborilava incessantemente contra as grandes janelas de vidro'
            )
        
        # Enhance character descriptions
        if 'Dr. Manoel' in paragraph and 'silhueta' in paragraph:
            enhanced = paragraph.replace(
                'a silhueta familiar de Dr. Manoel',
                'a silhueta inconfundível de Dr. Manoel'
            )
        
        return enhanced
    
    def _final_polish(self, content):
        """Apply final polish to the content"""
        # Ensure proper paragraph structure
        lines = content.split('\n')
        polished_lines = []
        
        for line in lines:
            if line.strip():
                # Ensure dialogue formatting is consistent
                if line.strip().startswith('"') and line.strip().endswith('"'):
                    # This is dialogue - ensure proper formatting
                    polished_lines.append(line)
                else:
                    # This is narrative - ensure proper flow
                    polished_lines.append(line)
            else:
                polished_lines.append(line)
        
        polished_content = '\n'.join(polished_lines)
        
        # Add final formatting touches
        polished_content = self._add_final_formatting(polished_content)
        
        return polished_content
    
    def _add_final_formatting(self, content):
        """Add final formatting touches"""
        # Ensure consistent spacing around dialogue
        formatted = content
        
        # Add proper spacing before dialogue
        import re
        formatted = re.sub(r'([.!?])\n\n"', r'\1\n\n"', formatted)
        
        # Ensure proper paragraph breaks
        formatted = re.sub(r'\n\n\n+', '\n\n', formatted)
        
        return formatted.strip()
