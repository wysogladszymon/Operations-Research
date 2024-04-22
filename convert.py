import nbformat
from nbconvert import HTMLExporter, PDFExporter
import os

import pdfkit

def html_to_pdf_pdfkit(html_path, pdf_path):
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,  # Dodatkowa opcja dla bezpieczeństwa
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'no-images': None,  # Wyłączenie obrazków (opcjonalne)
        'quiet': None,  # Wyłączenie komunikatów (opcjonalne)
        'disable-javascript': None,  # Wyłączenie JavaScript (opcjonalne)
        'load-media-error-handling': 'ignore',  # Ignorowanie błędów ładowania multimediów (opcjonalne)
        'user-style-sheet': 'path/to/your/custom.css'  # Dodanie niestandardowego arkusza stylów CSS (opcjonalne)
    }
    pdfkit.from_file(html_path, pdf_path, options=options)
    print(f"Converted {html_path} to {pdf_path} using pdfkit")
def convert_notebook_to_html(notebook_path, output_path):
    # Wczytanie notebooka
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Konwersja do HTML
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    (body, resources) = html_exporter.from_notebook_node(nb)

    # Zapisanie do pliku HTML
    html_path = notebook_path.replace('.ipynb', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(body)
    
    print(f"Converted {notebook_path} to {html_path}")

# Przykładowe użycie
convert_notebook_to_html('lab5/PERT.ipynb', 'lab5')
html_to_pdf_pdfkit('lab5/PERT.html', 'lab5/PERT.pdf')