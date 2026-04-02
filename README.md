# 📄 DocuMind-Gen: AI-Powered Document Annotation System

DocuMind-Gen is an intelligent document annotation system that uses **Google's Gemini API** to automatically extract structured data from PDF documents and visualize the results with precise **bounding box annotations**. Built for a **human-in-the-loop** workflow where AI extracts and humans validate.

> Conceived as a next-generation replacement for traditional IDP (Intelligent Document Processing) systems — leveraging GenAI instead of rule-based extraction.

## 🌟 Key Features

* **Gemini-Powered Extraction:** Uses Gemini 2.5 Flash to extract structured fields (names, addresses, etc.) from PDF documents with bounding box coordinates.
* **Structured Output:** Enforces response schema using Pydantic models — ensures consistent, validated JSON output from the LLM.
* **Bounding Box Visualization:** Annotates the original PDF with red bounding boxes around extracted fields using PyMuPDF (fitz).
* **Smart Document Detection:** Automatically detects whether a PDF is digitally native or scanned, enabling different processing paths.
* **Human-in-the-Loop Ready:** Generates annotated PDFs for human review and validation before downstream processing.

## 🏗️ Technical Architecture
```
PDF Input → Digital/Scanned Detection → Gemini API Extraction → Pydantic Validation → Bounding Box Annotation → Annotated PDF Output
```

1. **Document Analysis:** PyMuPDF checks if the PDF contains embedded fonts (digital) or is a scanned image.
2. **AI Extraction:** For non-digital PDFs, the document is sent to Gemini API with a structured prompt requesting field values, bounding boxes, and page numbers.
3. **Schema Enforcement:** Pydantic models (`NameField`, `AddressField`) validate the LLM response, ensuring type safety and required fields.
4. **Annotation:** Bounding box coordinates (normalized 0-1000 scale) are converted to actual page coordinates and drawn on the PDF with field labels.

## 🧠 Why This Approach?

Traditional IDP systems rely on **templates, rules, and pre-trained CV models** — requiring separate configurations for each document type. DocuMind-Gen replaces this with a single Gemini API call that understands document layout, extracts fields, and provides spatial coordinates — **no templates, no rules, no retraining**.

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* Google Gemini API key ([Get one here](https://aistudio.google.com/apikey))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/A-B-Ravte/DocuMind-Gen.git
cd DocuMind-Gen

# Set up virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install google-genai pymupdf pydantic python-dotenv
```

### 3. Configuration
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Run
```bash
python main.py
```

The annotated PDF will be saved as `Anotated.pdf` in the project directory.

## 📁 Project Structure
```
DocuMind-Gen/
├── main.py          # Core extraction pipeline — Gemini API + Pydantic schema
├── utility.py       # Document operations — digital detection + annotation
├── Sample-Doc/      # Sample PDFs for testing
├── .env             # API key configuration
└── README.md
```

## 🔮 Future Roadmap
- [ ] Support for multi-page extraction with per-page field mapping
- [ ] FastAPI endpoint for document upload and processing
- [ ] Configurable extraction schema — define fields via UI/config
- [ ] Traditional extraction path for digitally native PDFs (cost optimization)
- [ ] Batch processing for multiple documents

## 👨‍💻 Author
**Aakash Ravte** — Senior Software Engineer | Applied AI & Intelligent Automation
