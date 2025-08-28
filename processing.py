import os
import re
import docx
import fitz  # PyMuPDF
from PIL import Image, ImageEnhance
import pytesseract
import spacy
from unidecode import unidecode
import google.generativeai as genai
from groq import Groq
from openai import OpenAI
import requests
import time

# --- CONFIGURAÇÃO INICIAL ---
print("Carregando modelo de linguagem spaCy (pt_core_news_sm)...")
try:
    NLP = spacy.load("pt_core_news_sm")
except OSError:
    print("Modelo 'pt_core_news_sm' do spaCy não encontrado. Instalando...")
    os.system("python -m spacy download pt_core_news_sm")
    NLP = spacy.load("pt_core_news_sm")
print("Modelo spaCy carregado.")

# --- FUNÇÕES DE CONVERSÃO DE ARQUIVOS ---


def ocr_image(img):
    """Aplica OCR a uma imagem com pré-processamento."""
    img = img.convert("L")  # Converte para escala de cinza
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Aumenta o contraste
    # Tenta preservar a segmentação de parágrafos
    custom_config = r"--oem 3 --psm 4 -l por"
    try:
        return pytesseract.image_to_string(img, config=custom_config)
    except pytesseract.TesseractNotFoundError:
        print(
            "ERRO: Tesseract não foi encontrado. Certifique-se de que está instalado e no PATH do sistema."
        )
        return ""


def convert_to_text(file_path):
    """Converte um arquivo (PDF ou DOCX) para texto bruto."""
    print(f"Convertendo {os.path.basename(file_path)} para texto...")
    _, extension = os.path.splitext(file_path)
    text = ""

    if extension.lower() == ".docx":
        try:
            doc = docx.Document(file_path)
            text = "\n\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Erro ao converter DOCX {os.path.basename(file_path)}: {e}")
            return None

    elif extension.lower() == ".pdf":
        try:
            with fitz.open(file_path) as doc:
                for page_num, page in enumerate(doc):
                    # Tenta extrair texto diretamente
                    page_text = page.get_text("text")
                    # Se o texto direto for insignificante, usa OCR
                    if len(page_text.strip()) < 50:
                        print(
                            f"Página {page_num+1} parece ser uma imagem. Aplicando OCR..."
                        )
                        pix = page.get_pixmap(dpi=300)
                        img = Image.frombytes(
                            "RGB", [pix.width, pix.height], pix.samples
                        )
                        page_text = ocr_image(img)
                    text += page_text + "\n\n"
        except Exception as e:
            print(f"Erro ao converter PDF {os.path.basename(file_path)}: {e}")
            return None

    print("Conversão concluída.")
    return text


# --- FUNÇÕES DE LIMPEZA DE TEXTO ---


def extract_metadata_from_filename(filename):
    """Extrai autor e título do nome do arquivo."""
    # Remove a extensão e substitui underscores por espaços
    base = os.path.splitext(filename)[0].replace("_", " ")
    parts = base.split(" ", 1)
    author = parts[0]
    title = parts[1] if len(parts) > 1 else ""

    # Remove designações como "OCR" ou "Word" do título
    title = re.sub(r" (OCR|WOR|Word)$", "", title, flags=re.IGNORECASE).strip()

    return author, title


def clean_text_programmatically(text, filename):
    """Realiza a primeira passada de limpeza no texto bruto."""
    print("Iniciando limpeza programática...")

    # 1. Extrair autor e título para criar stopwords personalizadas
    author, title = extract_metadata_from_filename(filename)
    custom_stopwords = set()
    if author:
        custom_stopwords.update(unidecode(author).lower().split())
    if title:
        custom_stopwords.update(
            unidecode(t).lower() for t in title.split() if len(t) > 3
        )
    print(f"Stopwords personalizadas: {custom_stopwords}")

    # 2. Remover lixo de cabeçalho/rodapé de OCR e páginas de rosto
    lines = text.split("\n")
    cleaned_lines = []
    garbage_patterns = [
        r"universidade",
        r"biblioteca",
        r"boston university",
        r"copyright",
        r"interlibrary",
        r"isbn",
        r"tipografia",
        r"digitalizado por",
        r"ficha t[eé]cnica",
        r"paginas",
        r"scanned by",
    ]

    for line in lines:
        line_lower = unidecode(line).lower()
        # Remove linhas que são lixo de OCR ou stopwords personalizadas
        if (
            not any(re.search(p, line_lower) for p in garbage_patterns)
            and line_lower.strip() not in custom_stopwords
        ):
            cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # 3. Normalização do texto
    text = re.sub(r"\s*-\n\s*", "", text)  # Une palavras hifenizadas no final da linha
    text = re.sub(r"\n", " ", text)  # Substitui novas linhas por espaços
    text = re.sub(r"\s{2,}", " ", text)  # Remove espaços múltiplos
    text = text.strip()

    print("Limpeza programática concluída.")
    return text


# --- FUNÇÃO DE REVISÃO COM LLM ---


def review_and_refine_with_llm(text, gemini_api_key, chunk_size=25000):
    """Usa múltiplas APIs (Gemini, xAI, Groq, OpenAI) para revisar e refinar o texto limpo.
    PARA o processamento se todas as APIs falharem e aguarda até que uma volte a funcionar.
    """

    attempt = 0
    max_attempts = 48  # 48 tentativas x 5 min = 4 horas máximo

    while attempt < max_attempts:
        # Obtém as chaves das APIs do ambiente
        xai_key = os.getenv("XAI_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        # Tenta diferentes APIs em ordem de preferência
        apis = [
            ("Gemini", lambda chunk: _process_with_gemini(chunk, gemini_api_key)),
            ("xAI", lambda chunk: _process_with_xai(chunk, xai_key)),
            ("Groq", lambda chunk: _process_with_groq(chunk, groq_key)),
            ("OpenAI", lambda chunk: _process_with_openai(chunk, openai_key)),
        ]

        # Encontra a primeira API que funciona
        working_api = None
        api_name = None

        for name, api_func in apis:
            try:
                # Teste com uma pequena string
                test_result = api_func("Teste de conexão.")
                if test_result and len(test_result.strip()) > 0:
                    working_api = api_func
                    api_name = name
                    print(f"API {name} funcionando corretamente.")
                    break
            except Exception as e:
                error_msg = str(e)
                if "rate_limit_exceeded" in error_msg or "429" in error_msg:
                    print(f"API {name} com limite de taxa excedido")
                else:
                    print(f"API {name} falhou: {error_msg[:100]}")
                continue

        if working_api:
            break  # Sai do loop se encontrou uma API funcionando
        else:
            attempt += 1
            print(f"TODAS AS APIs FALHARAM! (Tentativa {attempt}/{max_attempts})")

            if attempt >= max_attempts:
                print("ERRO CRÍTICO: Máximo de tentativas atingido!")
                print("Não foi possível obter uma API funcionando após 4 horas.")
                print(
                    "Por favor, verifique suas chaves de API ou tente novamente mais tarde."
                )
                raise Exception("Todas as APIs falharam após múltiplas tentativas")

            print("Aguardando 5 minutos para tentar novamente...")
            print("O processamento está PAUSADO até que uma API volte a funcionar.")
            print("Isso é ESSENCIAL para garantir a qualidade dos textos limpos.")

            # Countdown visual
            for remaining in range(300, 0, -60):  # A cada minuto
                mins = remaining // 60
                print(f"   {mins} minutos restantes...")
                time.sleep(60)

            print("Tentando APIs novamente...")

    print(f"Usando API {api_name} para processamento.")

    # Se o texto for pequeno, processa de uma vez
    if len(text) <= chunk_size:
        try:
            return working_api(text)
        except Exception as e:
            print(f"ERRO ao processar texto pequeno: {e}")
            return text

    # Para textos grandes, divide em chunks e processa cada um
    print(f"Texto longo detectado ({len(text)} caracteres). Processando em chunks...")

    # Divide o texto em chunks menores respeitando limites de palavras
    chunks = _split_text_into_chunks(text, chunk_size)
    refined_chunks = []

    for i, chunk in enumerate(chunks):
        print(f"Processando chunk {i+1}/{len(chunks)}...")
        try:
            refined_chunk = working_api(chunk)
            refined_chunks.append(refined_chunk)
        except Exception as e:
            error_msg = str(e)
            if "rate_limit_exceeded" in error_msg or "429" in error_msg:
                print(f"Rate limit atingido no chunk {i+1}. Aguardando 60 segundos...")
                time.sleep(60)
                try:
                    refined_chunk = working_api(chunk)
                    refined_chunks.append(refined_chunk)
                except Exception as e2:
                    print(f"ERRO ao processar chunk {i+1} após retry: {e2}")
                    print("Usando chunk original...")
                    refined_chunks.append(chunk)
            else:
                print(f"ERRO ao processar chunk {i+1}: {e}")
                print("Usando chunk original...")
                refined_chunks.append(chunk)

    # Junta todos os chunks refinados
    final_text = " ".join(refined_chunks)
    print(f"Revisão completa com {api_name} concluída com sucesso.")
    return final_text


def _split_text_into_chunks(text, chunk_size):
    """Divide o texto em chunks menores respeitando limites de palavras."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        word_size = len(word) + 1  # +1 para o espaço
        if current_size + word_size > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_size = word_size
        else:
            current_chunk.append(word)
            current_size += word_size

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def _get_base_prompt(text_chunk):
    """Retorna o prompt base para refinamento de texto."""
    return f"""Aja como um especialista em arquivística, biblioteconomia e análise de dados.
O texto a seguir foi extraído de uma obra literária por meio de OCR e passou por uma limpeza inicial.
Sua tarefa é realizar uma revisão final e refinamento.

Instruções:
1. Corrija erros óbvios de OCR que a limpeza automática não pegou (ex: 'tarn' para 'tao', letras trocadas, pontuação estranha).
2. Remova quaisquer metadados remanescentes (nomes de editoras, notas de digitalização, números de página soltos) que não fazem parte do corpo da obra.
3. Preserve a integridade do texto original, mantendo o estilo, a gramática da época e a estrutura dos parágrafos. Não modernize a linguagem.
4. Retorne APENAS o texto literário limpo e refinado. Não inclua nenhum comentário, cabeçalho ou explicação sua na saída.

Texto para revisão:
---
{text_chunk}"""


def _process_with_gemini(text_chunk, api_key):
    """Processa chunk usando Gemini."""
    if not api_key:
        raise Exception("API key não fornecida")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(_get_base_prompt(text_chunk))
    return response.text


def _process_with_xai(text_chunk, api_key):
    """Processa chunk usando xAI (Grok)."""
    if not api_key:
        raise Exception("API key não fornecida")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )

    response = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em arquivística e refinamento de textos literários.",
            },
            {"role": "user", "content": _get_base_prompt(text_chunk)},
        ],
        max_tokens=4000,
        temperature=0.1,
    )
    return response.choices[0].message.content


def _process_with_groq(text_chunk, api_key):
    """Processa chunk usando Groq."""
    if not api_key:
        raise Exception("API key não fornecida")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em arquivística e refinamento de textos literários.",
            },
            {"role": "user", "content": _get_base_prompt(text_chunk)},
        ],
        model="qwen-qwq-32b",
        max_tokens=4000,
        temperature=0.1,
    )
    return response.choices[0].message.content


def _process_with_openai(text_chunk, api_key):
    """Processa chunk usando OpenAI."""
    if not api_key:
        raise Exception("API key não fornecida")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em arquivística e refinamento de textos literários.",
            },
            {"role": "user", "content": _get_base_prompt(text_chunk)},
        ],
        max_tokens=4000,
        temperature=0.1,
    )
    return response.choices[0].message.content
