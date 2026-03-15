---
name: pdf-elaborated
description: |
  Enhanced PDF toolkit with P&ID diagram analysis capabilities.
  Extracts process streams, identifies equipment, traces flow paths,
  and assigns ISA-5.1 stream numbers from engineering diagrams.
  Improved through 8 iterations of autoresearch-skill.
  Incorporates stuck detection, endgame strategy, and TSV logging.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
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

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter
c.drawString(100, height - 100, "Hello World!")
c.line(100, height - 140, 400, height - 140)
c.save()
```

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt
pdftotext -f 1 -l 5 input.pdf output.txt
```

### qpdf
```bash
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf output.pdf --rotate=+90:1
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

---

## P&ID Diagram Analysis

When analyzing Piping and Instrumentation Diagrams (P&IDs), use the following protocol to systematically identify equipment, trace process streams, and assign stream numbers. This section augments the general PDF toolkit with domain-specific knowledge for engineering diagram interpretation.

### Equipment Recognition

Identify equipment by matching visual symbols to their standard representations:

| Symbol | Equipment Type | Visual Cue |
|--------|---------------|------------|
| Circle with arrow | Pump | Small circle, often with a triangular discharge arrow |
| Cylinder (vertical) | Tank / Vessel | Vertical rectangle with rounded or dished ends |
| Cylinder (horizontal) | Storage Tank | Horizontal rectangle with rounded ends |
| Bowtie / hourglass | Valve | Two triangles meeting at a point |
| Circle with "M" | Motor | Circle containing the letter M |
| Rectangle with tubes | Heat Exchanger | Rectangle with internal parallel lines or U-tubes |
| Dashed rectangle | Future / Planned System | Dashed outline indicating equipment not yet installed |
| Trapezoid or triangle | Filter / Separator | Inverted triangle or wedge shape, sometimes with internal lines |
| Rectangle on wheels | Truck / Mobile Equipment | Rectangle with circles beneath representing wheels |

When scanning the diagram, proceed area by area (left to right, top to bottom). List each piece of equipment with its tag number if visible, or assign a positional label (e.g., "Pump-NW" for a pump in the northwest region).

### Stream Identification Protocol

Use simplified rules to identify process streams. Do NOT attempt step-by-step algorithmic tracing -- rules outperform procedural algorithms when used as LLM instructions.

**Rule 1 -- Equipment Connections:** Any line connecting two equipment items is a stream. If a line runs from Pump P-01 to Tank T-02, that is one stream regardless of bends or direction changes along the path.

**Rule 2 -- Boundary Crossings:** Any line entering or exiting the diagram boundary is a stream. These represent inlets (feed streams) and outlets (product or waste streams). Check all four edges of the diagram.

**Rule 3 -- Parallel Lines:** Parallel lines running between the same two pieces of equipment are separate streams, not a single stream drawn twice. Each line represents a distinct process flow.

**Rule 4 -- Instrument Taps:** Short lines terminating at instruments (pressure gauges, flow meters, temperature sensors) are instrument connections, NOT process streams. Do not count these.

**Rule 5 -- Utility Lines:** Lines marked with utility designations (CW for cooling water, S for steam, IA for instrument air) are utility streams. Count them separately from process streams if the analysis scope includes utilities.

### Flow Direction Inference

When arrow indicators are absent, infer flow direction using engineering conventions:

- **Pumps** push fluid from suction (inlet) to discharge (outlet). Flow exits in the direction the pump arrow points.
- **Gravity flow** moves downward. If two vessels are at different elevations with no pump between them, flow moves from the higher vessel to the lower one.
- **Arrows on lines** always indicate flow direction when present -- these override all other inference rules.
- **Process logic** dictates flow from feed to product. Storage tanks typically feed process equipment, which feeds product tanks.
- **Recycle streams** flow backward relative to the main process direction. They are identifiable by looping back to an upstream piece of equipment.

### Stream Numbering Convention (ISA-5.1)

Assign stream numbers following ISA-5.1 conventions:

1. **Format:** Use the prefix `S-` followed by a two-digit sequential number: `S-01`, `S-02`, ..., `S-15`.
2. **Numbering order:** Number streams by process area, then sequentially within each area. Start with the main process train (feed to product), then side streams, then utility streams.
3. **Inlet streams** receive the lowest numbers in their process area.
4. **Outlet streams** receive the highest numbers in their process area.
5. **Recycle streams** are numbered after the forward-flow streams they parallel.

### Bypass and Recycle Detection

Bypass and recycle lines are commonly missed because they do not follow the main process flow path:

- **Bypass lines** skip one or more pieces of equipment, running parallel to the main flow path. Look for lines that branch off before equipment and rejoin after it.
- **Recycle lines** loop back from a downstream point to an upstream point. They often include a pump to overcome pressure drop.
- **Purge streams** branch off a recycle loop and exit the system. They prevent accumulation of inerts.

When stream count does not improve across multiple analysis passes, systematically check for these non-obvious stream types.

### Structured Output Format

Present identified streams as structured JSON for systematic verification:

```json
{
  "equipment": [
    {"id": "P-01", "type": "Pump", "location": "northwest"},
    {"id": "T-01", "type": "Tank", "location": "north-center"}
  ],
  "streams": [
    {
      "id": "S-01",
      "from": "Boundary-West",
      "to": "TK-01",
      "type": "inlet",
      "direction": "left-to-right"
    },
    {
      "id": "S-02",
      "from": "TK-01",
      "to": "P-01",
      "type": "process",
      "direction": "left-to-right"
    }
  ],
  "summary": {
    "total_equipment": 8,
    "total_streams": 15,
    "numbered_streams": 13
  }
}
```

### Stuck Detection Integration

If the stream count does not increase after re-examining the diagram:

1. **First plateau:** Switch recognition approach. If scanning left-to-right, try scanning by equipment type instead (all pumps, then all tanks, then all valves).
2. **Second plateau:** Focus exclusively on diagram boundaries and bypass/recycle lines -- these are the most commonly missed stream categories.
3. **Third plateau:** Accept the current count. The remaining undetected streams likely require process design intent knowledge not available from the diagram alone.

### Endgame Polish

On the final analysis pass, when stream count is near the expected total:

1. Verify every numbered stream has both a source and a destination.
2. Confirm no duplicate streams (two IDs for the same physical line).
3. Cross-check equipment count against the equipment list.
4. Produce the structured JSON output with all fields populated.
5. Flag any streams with uncertain identification for manual review.
