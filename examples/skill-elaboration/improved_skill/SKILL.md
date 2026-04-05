---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When the LLM (Claude, ChatGPT, Gemini, or others) needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
license: Proprietary. LICENSE.txt has complete terms
---
# PDF Processing Guide
## Overview
This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.
## Quick Start
```python
from pypdf import PdfReader, PdfWriter
# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")
# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```
## Python Libraries
### pypdf - Basic Operations
#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader
writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
with open("merged.pdf", "wb") as output:
    writer.write(output)
```
#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```
#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```
#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()
page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)
with open("rotated.pdf", "wb") as output:
    writer.write(output)
```
### pdfplumber - Text and Table Extraction
#### Extract Text with Layout
```python
import pdfplumber
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```
#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```
#### Advanced Table Extraction
```python
import pandas as pd
with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)
# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```
### reportlab - Create PDFs
#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter
# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")
# Add a line
c.line(100, height - 140, 400, height - 140)
# Save
c.save()
```
#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []
# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))
body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())
# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))
# Build PDF
doc.build(story)
```
## Command-Line Tools
### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt
# Extract text preserving layout
pdftotext -layout input.pdf output.txt
# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```
### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf
# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees
# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```
### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf
# Split
pdftk input.pdf burst
# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```
## Common Tasks
### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path
# Convert PDF to images
images = convert_from_path('scanned.pdf')
# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"
print(text)
```
### Add Watermark
```python
from pypdf import PdfReader, PdfWriter
# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]
# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)
with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```
### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix
# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```
### Password Protection
```python
from pypdf import PdfReader, PdfWriter
reader = PdfReader("input.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
# Add password
writer.encrypt("userpassword", "ownerpassword")
with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```
## Quick Reference
| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see forms.md) | See forms.md |

## Next Steps
- For advanced pypdfium2 usage, see reference.md
- For JavaScript libraries (pdf-lib), see reference.md
- If you need to fill out a PDF form, follow the instructions in forms.md
- For troubleshooting guides, see reference.md

## P&ID Diagram Analysis

This section covers extraction and analysis of Piping and Instrumentation Diagrams (P&IDs), also known as process flow diagrams. P&ID drawings use standardized notation and P&ID symbols per ISO 10628 and ISO 14617 to represent piping, equipment, instruments, and control loops in process plants.

### P&ID Symbol Identification

P&ID symbols follow standard notation conventions. Identify each symbol by its geometric shape:
- **Circle**: field-mounted instrument (example: flow transmitter FT-101)
- **Circle with line**: control room instrument
- **Diamond**: logic or computer function
- **Rectangle**: PLC or DCS panel-mounted device, also used for vessel and tank outlines
- **Arrow**: indicates flow direction of each process stream

### Process Stream Extraction

Step 1: Trace every process stream from its origin to destination. Each stream carries a line number (example tag format: 4"-WW-101-A1, meaning 4-inch wastewater line 101 in area A1). Follow the flow direction indicated by arrows on piping lines.
Step 2: Record stream properties — fluid type, phase, temperature, pressure, and flow rate when noted in the process data.
Step 3: Assign sequential stream numbers to all piping connections between major equipment. Cross-reference against the line number list in the title block or line schedule.

### Equipment Identification

Step 4: Catalog every equipment tag visible on the P&ID. Equipment types include:
- **Pump** (tag format: P-101, P-102): shown as a circle with discharge arrow
- **Heat exchanger** (tag format: E-101): shown as circle with internal lines
- **Vessel** (tag format: V-101): vertical rectangle with dished heads
- **Tank** (tag format: TK-101): open-top rectangle for atmospheric storage
- **Valve** (tag format: XV-101, CV-101): diamond or bowtie symbol on piping

### Instrument and Control Loop Analysis

Step 5: Identify every instrument by its tag format (example: FIC-101 = Flow Indicating Controller, loop 101). The first letter indicates the measured variable (F=Flow, T=Temperature, P=Pressure, L=Level). Subsequent letters indicate function (I=Indicating, C=Controller, T=Transmitter).
Step 6: Trace each control loop from sensor through controller to final control element. A typical control loop consists of: transmitter (circle) -> controller (circle with line) -> control valve (diamond on piping).

### Structured Output Template

After completing the analysis, produce output in this format:
- **Stream Table**: List each process stream with line number, from-equipment, to-equipment, and flow direction
- **Equipment List**: Every equipment tag with type, service description, and notation references
- **Instrument Index**: All instrument tags grouped by control loop with ISO 14617 symbol references
