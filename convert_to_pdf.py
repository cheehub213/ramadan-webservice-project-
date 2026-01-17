"""Convert Markdown Technical Report to PDF using fpdf2"""

from fpdf import FPDF
import re

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'myRamadan - Technical Report', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title, level=1):
        if level == 1:
            self.set_font('Arial', 'B', 18)
            self.set_text_color(0, 100, 0)
        elif level == 2:
            self.set_font('Arial', 'B', 14)
            self.set_text_color(0, 80, 0)
        else:
            self.set_font('Arial', 'B', 12)
            self.set_text_color(0, 60, 0)
        
        self.multi_cell(0, 10, title)
        self.ln(2)
        self.set_text_color(0, 0, 0)
        
    def body_text(self, text):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, text)
        self.ln(2)
        
    def code_block(self, code):
        self.set_font('Courier', '', 8)
        self.set_fill_color(240, 240, 240)
        lines = code.split('\n')
        for line in lines:
            # Truncate long lines
            if len(line) > 90:
                line = line[:87] + '...'
            self.cell(0, 5, line, 0, 1, fill=True)
        self.ln(2)
        self.set_font('Arial', '', 10)
        
    def table_row(self, cells, is_header=False):
        if is_header:
            self.set_font('Arial', 'B', 9)
            self.set_fill_color(200, 220, 200)
        else:
            self.set_font('Arial', '', 9)
            self.set_fill_color(255, 255, 255)
        
        # Calculate column widths
        page_width = self.w - 2 * self.l_margin
        col_width = page_width / len(cells)
        
        for cell in cells:
            # Truncate long cells
            text = str(cell).strip()
            if len(text) > 25:
                text = text[:22] + '...'
            self.cell(col_width, 7, text, 1, 0, 'L', fill=is_header)
        self.ln()
        
    def bullet_point(self, text):
        self.set_font('Arial', '', 10)
        self.cell(10, 6, chr(149), 0, 0)  # bullet character
        self.multi_cell(0, 6, text)

def parse_markdown(md_content):
    """Parse markdown and return structured elements"""
    elements = []
    lines = md_content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Headers
        if line.startswith('# '):
            elements.append(('h1', line[2:].strip()))
        elif line.startswith('## '):
            elements.append(('h2', line[3:].strip()))
        elif line.startswith('### '):
            elements.append(('h3', line[4:].strip()))
        elif line.startswith('#### '):
            elements.append(('h4', line[5:].strip()))
        
        # Code blocks
        elif line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            elements.append(('code', '\n'.join(code_lines)))
        
        # Tables
        elif '|' in line and line.strip().startswith('|'):
            table_rows = []
            while i < len(lines) and '|' in lines[i]:
                row = lines[i]
                # Skip separator rows
                if not re.match(r'^[\|\s\-:]+$', row):
                    cells = [c.strip() for c in row.split('|')[1:-1]]
                    if cells:
                        table_rows.append(cells)
                i += 1
            i -= 1  # Back up one
            if table_rows:
                elements.append(('table', table_rows))
        
        # Bullet points
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            bullet_text = line.strip()[2:]
            elements.append(('bullet', bullet_text))
        
        # Numbered lists
        elif re.match(r'^\d+\.\s', line.strip()):
            list_text = re.sub(r'^\d+\.\s', '', line.strip())
            elements.append(('bullet', list_text))
        
        # Bold text sections
        elif line.strip().startswith('**') and line.strip().endswith('**'):
            elements.append(('bold', line.strip()[2:-2]))
        
        # Regular paragraphs
        elif line.strip():
            # Clean markdown formatting
            text = line.strip()
            text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove bold
            text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Remove italic
            text = re.sub(r'`([^`]+)`', r'\1', text)  # Remove inline code
            elements.append(('text', text))
        
        i += 1
    
    return elements

def create_pdf(md_file, output_file):
    """Create PDF from markdown file"""
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse markdown
    elements = parse_markdown(content)
    
    # Create PDF
    pdf = PDFReport()
    pdf.add_page()
    
    for elem_type, elem_content in elements:
        try:
            if elem_type == 'h1':
                pdf.chapter_title(elem_content, 1)
            elif elem_type == 'h2':
                pdf.chapter_title(elem_content, 2)
            elif elem_type in ('h3', 'h4'):
                pdf.chapter_title(elem_content, 3)
            elif elem_type == 'code':
                pdf.code_block(elem_content)
            elif elem_type == 'table':
                if elem_content:
                    # First row is header
                    pdf.table_row(elem_content[0], is_header=True)
                    for row in elem_content[1:]:
                        pdf.table_row(row)
                    pdf.ln(3)
            elif elem_type == 'bullet':
                pdf.bullet_point(elem_content)
            elif elem_type == 'bold':
                pdf.set_font('Arial', 'B', 10)
                pdf.multi_cell(0, 6, elem_content)
                pdf.set_font('Arial', '', 10)
            elif elem_type == 'text':
                pdf.body_text(elem_content)
        except Exception as e:
            # Skip problematic elements
            print(f"Skipping element due to error: {e}")
            continue
    
    # Save PDF
    pdf.output(output_file)
    print(f"PDF created: {output_file}")

if __name__ == '__main__':
    md_file = r'c:\Users\cheeh\Desktop\ramadan-webservice-project-\Ramadan_Helper_Technical_Report.pdf.md'
    output_file = r'c:\Users\cheeh\Desktop\ramadan-webservice-project-\Ramadan_Helper_Technical_Report.pdf'
    create_pdf(md_file, output_file)
