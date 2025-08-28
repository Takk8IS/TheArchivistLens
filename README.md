# TheArchivistLens: A Reliable, Open and Secure Alternative to IRaMuTeQ

[Example Clean Text Output](https://raw.githubusercontent.com/Takk8IS/TheArchivistLens/refs/heads/main/output/textos_limpos/Anoitecidas%20WOR.txt)

[Example Report Output](https://github.com/Takk8IS/TheArchivistLens/blob/main/output/relatorios/relatorio_Anoitecidas%20WOR.md)

## Overview

**TheArchivistLens** is an advanced text analysis tool developed in Python as a **reliable, open and secure alternative to IRaMuTeQ**. This system implements the complete **Reinert Method** of Descending Hierarchical Classification (DHC), offering all IRaMuTeQ functionalities with additional advantages:

**Open and Transparent Code** - Fully auditable and modifiable
**Robust Multi-API System** - Automatic fallback between Gemini, xAI, Groq and OpenAI
**Complete Reinert Method** - DHC, dendrograms, tables and similarity analysis
**Modern Processing** - Advanced OCR, intelligent cleaning and AI refinement
**Professional Reports** - Structured Markdown with integrated PNG graphics
**Data Security** - Local processing with optional APIs

The system automates a complete pipeline, from document conversion (PDF, DOCX) to the generation of sophisticated analytical reports, using Natural Language Processing (NLP) techniques, Machine Learning and the rigorous **Reinert Method** for lexicometric analysis.

## Architecture and Features (Complete Reinert Method)

The system operates through a main orchestrator (`main.py`) that manages a modular pipeline implementing the complete **Reinert Method**, following IRaMuTeQ standards.

### Module 1: Text Processing and Refinement (`processing.py`)

This module prepares documents for rigorous lexicometric analysis:

- **Intelligent Conversion:** Extracts text from `.docx` and `.pdf` files whilst preserving structure
- **Advanced OCR:** Optimised **Tesseract** engine for scanned PDFs
- **Specialised Programmatic Cleaning:**
    - **Dynamic Stopwords:** Automatic extraction of author/title from filename
    - **Noise Filters:** Removes artifacts, headers, footers and metadata
    - **Text Normalisation:** Specific preparation for Reinert analysis
- **Robust Multi-API System:** Automatic fallback (Gemini → xAI → Groq → OpenAI)
- **AI Refinement:** OCR correction and text standardisation for maximum precision
- **Quality Assurance:** Processing paused if all APIs fail (retry every 5min)

### Module 2: Reinert Method and Lexicometric Analysis (`reinert.py`)

**Complete implementation of the Reinert Method (1983, 1991)** following IRaMuTeQ standards:

- **Textual Segmentation:** Automatic division into elementary context units (ECU)
- **Binary Matrix:** Creation of term-document matrix with `CountVectorizer`
- **Correspondence Factor Analysis (CFA):** Dimensional reduction with `TruncatedSVD`
- **Descending Hierarchical Classification (DHC):** Maximisation of χ² statistic
- **Class Characterisation:** Identification of keywords by lexical class
- **DHC Dendrogram:** Visualisation of hierarchical structure (PNG)
- **Word Clouds by Class:** Specific visualisation for each class (PNG)
- **Similarity Analysis:** Co-occurrence graph between words (PNG)
- **Reinert Tables:** Results in Markdown format with percentages and keywords

### Module 3: Complementary Analyses (`analysis.py`)

Additional analyses that complement the Reinert Method:

- **LDA Topic Modelling:** Identification of latent themes
- **Sentiment Analysis:** Emotional polarity of text
- **Named Entity Recognition (NER):** Extraction of people, places and organisations
- **Text Clustering:** Grouping of similar segments
- **General Word Cloud:** Visualisation of complete vocabulary
- **LLM Interpretation:** Specialised AI analysis
- **Integrated Reports:** Professional Markdown with all analyses

## Technologies and Implementation of the Reinert Method

### Main Technology Stack
- **Language:** Python 3.12+
- **Reinert Method:** Complete implementation following Reinert (1983, 1991)
- **Compatibility:** Results equivalent to IRaMuTeQ

### Specialised Libraries

#### AI APIs (Multi-API System)
- `google-generativeai`: Gemini Pro Integration
- `groq`: Llama Models via Groq
- `openai`: OpenAI GPT and xAI Grok

#### Lexicometric Analysis (Reinert Method)
- `scikit-learn`: DHC, CFA, binary matrix, χ² statistics
- `scipy`: Hierarchical analysis and clustering
- `pandas`: Textual data manipulation
- `numpy`: Matrix operations for DHC

#### Natural Language Processing
- `spacy`: NER, tokenisation, lemmatisation (model `pt_core_news_sm`)
- `nltk`: Portuguese stopwords and basic processing
- `gensim`: LDA topic modelling
- `textblob`: Sentiment analysis

#### Visualisation and Graphics
- `matplotlib`: Dendrograms and statistical graphs
- `seaborn`: Advanced statistical visualisations
- `wordcloud`: Word clouds by class
- `networkx`: Similarity analysis (graphs)
- `plotly`: Interactive graphs

#### Document Processing
- `PyMuPDF` (fitz): PDF text extraction
- `python-docx`: DOCX file processing
- `pytesseract` + `Pillow`: OCR with Tesseract

#### Utilities
- `python-dotenv`: Secure API key management
- `unidecode`: Character normalisation
- `tqdm`: Progress bars
- `tabulate`: Table formatting
- `statsmodels`: Advanced statistical analyses

## How to Run (Complete Guide)

### Prerequisites

1. **Python 3.12+** - Recommended version for best performance
2. **Tesseract OCR** - Optical Character Recognition engine:
   - **macOS:** `brew install tesseract`
   - **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
   - **Windows:** Download from [Official GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
3. **Portuguese spaCy Model:** Will be installed automatically

### Installation and Configuration

#### 1. Clone and Prepare the Environment
```bash
git clone https://github.com/Takk8IS/TheArchivistLens.git
cd TheArchivistLens
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

#### 2. Configure API Keys (At Least One Required)
Create a `.env` file in the project root:
```env
# At least one API is required for text refinement
GEMINI_API_KEY='your_gemini_api_key'
XAI_API_KEY='your_xai_api_key'
GROQ_API_KEY='your_groq_api_key'
OPENAI_API_KEY='your_openai_api_key'
```

**Intelligent Fallback System:**
- Priority order: Gemini → xAI → Groq → OpenAI
- If all fail: 5-minute pause before retrying
- Maximum 48 attempts (4 hours) before failure
- **Guarantee:** Only refined texts are processed

#### 3. Add Your Documents
Place `.pdf` and `.docx` files in the `/docs/` folder

#### 4. Run Complete Analysis
```bash
python main.py
```

### Generated Results

After execution, you will have:
- **Clean texts** in `/output/clean_texts/`
- **Reinert Reports** in `/output/reports/`
- **DHC Dendrograms** (PNG)
- **Word clouds by class** (PNG)
- **Similarity analyses** (PNG)
- **Markdown tables** with statistical results

## Project Structure

```
TheArchivistLens/
├── docs/                    # INPUT: Documents for analysis
│   ├── file1.pdf
│   ├── file2.docx
│   └── ...
├── output/                  # OUTPUT: All results
│   ├── clean_texts/         # AI-refined texts
│   │   ├── file1.txt
│   │   └── file2.txt
│   └── reports/             # Complete analyses
│       ├── report_file1.md
│       ├── dendrogram_file1.png
│       ├── class_1_file1.png
│       ├── class_2_file1.png
│       ├── similarity_file1.png
│       ├── wordcloud_file1.png
│       └── ...
├── main.py                  # Main orchestrator
├── processing.py            # Processing and cleaning
├── reinert.py               # Complete Reinert Method
├── analysis.py              # Complementary analyses
├── .env                     # API keys (not versioned)
├── requirements.txt         # Python dependencies
└── README.md                # This documentation
```

## Detailed System Outputs

### Processed Texts
- **`/output/clean_texts/*.txt`**: Texts extracted, cleaned and refined by AI
- **Guaranteed quality**: Multi-API system with automatic fallback
- **Optimised OCR**: Precise recognition of scanned PDFs

### Reinert Method (Equivalent to IRaMuTeQ)
- **`report_*.md`**: Complete report with Reinert table
- **`dendrogram_*.png`**: DHC visualisation
- **`class_N_*.png`**: Word cloud for each lexical class
- **`similarity_*.png`**: Co-occurrence graph between words

### Complementary Analyses
- **`wordcloud_*.png`**: General word cloud
- **`clustering_*.png`**: Textual segment clustering
- **Sentiment analysis**: Integrated in the report
- **Named entities**: People, places and organisations
- **LLM Interpretation**: Specialised AI analysis

## TheArchivistLens vs IRaMuTeQ

| Feature | IRaMuTeQ | TheArchivistLens |
|---|---|---|
| **Code** | Closed | **Open and Auditable** |
| **Reinert Method** | Complete | **Faithful Implementation** |
| **Platform** | Windows/R | **Cross-platform (Python)** |
| **AI APIs** | No | **4 APIs with Fallback** |
| **Modern OCR** | Limited | **Optimised Tesseract** |
| **Reports** | Basic | **Professional Markdown** |
| **Graphics** | R plots | **High-Quality PNG** |
| **Security** | Dependent | **Local Processing** |
| **Updates** | Slow | **Active Development** |
| **Support** | Limited | **Open Source Community** |

### Exclusive Advantages

**Complete Transparency**: Auditable and modifiable code
**Multi-API System**: Intelligent fallback between 4 providers
**Advanced OCR**: Superior processing of scanned PDFs
**Modern Reports**: Markdown with integrated PNG graphics
**Security**: Local processing with optional APIs
**Flexibility**: Easily extensible and customisable
**Performance**: Optimised Python for large corpora
**Free**: No licences or commercial restrictions

## Contributions and Community

**TheArchivistLens** is an open source project that values contributions from the academic and developer communities.

### How to Contribute
- **Issues**: Report bugs or suggest improvements
- **Pull Requests**: Contribute code and documentation
- **Documentation**: Help improve guides and examples
- **Testing**: Test with different corpora and share results

### Roadmap
- [ ] Graphical user interface (GUI)
- [ ] Support for more languages
- [ ] Comparative analysis between corpora
- [ ] Export to academic formats
- [ ] Integration with Jupyter Notebooks

## Academic Citation

If you use **TheArchivistLens** in academic research, please cite:

```bibtex
@software{cavalcante2025archivistlens,
  title={TheArchivistLens: Open Source Alternative to IRaMuTeQ for Reinert Method Analysis},
  author={Cavalcante, David C},
  year={2025},
  url={https://github.com/Takk8IS/TheArchivistLens},
  note={Python implementation of Reinert Method (CHD) for lexicometric analysis}
}
```

## Support the Project

If **TheArchivistLens** has been useful in your research or work, please consider supporting its development:

**USDT (TRC-20):** `TGpiWetnYK2VQpxNGPR27D9vfM6Mei5vNA`

## About the Author

**David C Cavalcante**
*AI ML Engineer | Research Scientist | LLM Philosopher*

**Takk™ Innovate Studio**
**Email:** [davcavalcante@proton.me](mailto:davcavalcante@proton.me)
**LinkedIn:** [https://linkedin.com/in/hellodav](https://linkedin.com/in/hellodav)
**Website:** [https://takk.ag](https://takk.ag)

---

## Licence

**TheArchivistLens** is distributed under the Apache 2.0 Licence, with the additional condition that any use or distribution requires explicit prior authorisation from the author. Please contact the author before using or distributing this software.