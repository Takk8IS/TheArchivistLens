import os
import re
import spacy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from gensim import corpora, models
from nltk.corpus import stopwords
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

try:
    import google.generativeai as genai
except ImportError:
    genai = None
import warnings

warnings.filterwarnings("ignore")

# Import do módulo Reinert
from reinert import ReinertAnalyzer

# --- CONFIGURAÇÃO INICIAL ---
print("Carregando recursos NLTK (stopwords)...")
try:
    STOPWORDS_PT = set(stopwords.words("portuguese"))
except LookupError:
    nltk.download("stopwords")
    STOPWORDS_PT = set(stopwords.words("portuguese"))

print("Carregando modelo de linguagem spaCy (pt_core_news_sm)...")
try:
    NLP = spacy.load("pt_core_news_sm")
except OSError:
    print("Modelo 'pt_core_news_sm' do spaCy não encontrado. Instalando...")
    os.system("python -m spacy download pt_core_news_sm")
    NLP = spacy.load("pt_core_news_sm")
print("Modelo spaCy carregado.")

# Configuração matplotlib para UTF-8
plt.rcParams["font.size"] = 10
plt.rcParams["figure.dpi"] = 300


# --- FUNÇÕES DE ANÁLISE AVANÇADAS ---


def preprocess_for_analysis(text):
    """Lematiza, remove stopwords e pontuação para análises de NLP."""
    # Adiciona palavras comuns que podem não estar nas stopwords padrão mas poluem os resultados
    custom_stopwords = STOPWORDS_PT.union(
        {
            "fig",
            "pag",
            "capitulo",
            "livro",
            "coisa",
            "disse",
            "ser",
            "estar",
            "ter",
            "fazer",
            "dizer",
            "ir",
            "ver",
            "dar",
            "saber",
            "ficar",
            "vir",
            "querer",
            "poder",
            "todo",
            "toda",
            "todos",
            "todas",
            "muito",
            "bem",
            "assim",
            "então",
        }
    )

    # Aumenta o limite do modelo se o texto for muito grande
    if len(text) > NLP.max_length:
        NLP.max_length = len(text) + 100

    doc = NLP(text.lower())
    tokens = [
        token.lemma_
        for token in doc
        if token.is_alpha
        and len(token.lemma_) > 2
        and token.lower_ not in custom_stopwords
        and token.lemma_ not in custom_stopwords
        and not token.is_stop
    ]
    return tokens


def generate_advanced_wordcloud(tokens, output_dir, filename_prefix):
    """Gera nuvem de palavras avançada com melhor visualização."""
    print("Gerando nuvem de palavras avançada...")
    path = os.path.join(output_dir, f"wordcloud_{filename_prefix}.png")
    text_for_wc = " ".join(tokens)

    if not text_for_wc:
        print("AVISO: Não há texto suficiente para gerar a nuvem de palavras.")
        return None

    # Configuração avançada da wordcloud
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color="white",
        colormap="viridis",
        max_words=200,
        relative_scaling=0.5,
        min_font_size=10,
        prefer_horizontal=0.7,
        include_numbers=False,
        collocations=False,
    ).generate(text_for_wc)

    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(
        f"Nuvem de Palavras - {filename_prefix}", fontsize=16, fontweight="bold", pad=20
    )
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Nuvem de palavras salva em: {os.path.basename(path)}")
    return os.path.basename(path)


def perform_sentiment_analysis(text):
    """Realiza análise de sentimentos do texto."""
    print("Realizando análise de sentimentos...")

    if TextBlob is None:
        return {
            "polarity": 0.0,
            "subjectivity": 0.5,
            "sentiment_label": "Neutro (TextBlob não disponível)",
            "subjectivity_label": "Objetivo",
        }

    try:
        # Usar TextBlob para análise básica
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Interpretar resultados
        sentiment_label = "Neutro"
        if polarity > 0.1:
            sentiment_label = "Positivo"
        elif polarity < -0.1:
            sentiment_label = "Negativo"

        subjectivity_label = "Objetivo"
        if subjectivity > 0.5:
            subjectivity_label = "Subjetivo"

        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment_label": sentiment_label,
            "subjectivity_label": subjectivity_label,
        }
    except Exception as e:
        print(f"Erro na análise de sentimentos: {e}")
        return None


def perform_advanced_topic_modeling(tokens, num_topics=5):
    """Realiza modelagem de tópicos LDA avançada."""
    print(f"Realizando modelagem de tópicos LDA avançada para {num_topics} tópicos...")

    if len(tokens) < 20:
        print("AVISO: Texto insuficiente para modelagem de tópicos.")
        return "Texto insuficiente para análise.", None, None

    try:
        # Criar dicionário e corpus
        dictionary = corpora.Dictionary([tokens])
        dictionary.filter_extremes(no_below=2, no_above=0.8)
        corpus = [dictionary.doc2bow(tokens)]

        # Treinar modelo LDA com parâmetros otimizados
        lda_model = models.LdaModel(
            corpus,
            num_topics=num_topics,
            id2word=dictionary,
            passes=50,
            iterations=100,
            random_state=42,
            alpha="auto",
            eta="auto",
        )

        # Extrair tópicos
        topics = lda_model.print_topics(num_words=12)

        # Formatar saída
        topics_html = "<ul>"
        topic_data = []

        for i, topic in topics:
            words = re.findall(r'"(.*?)"', topic)
            probabilities = re.findall(r"(\d+\.\d+)\*", topic)

            formatted_topic = ", ".join(words[:10])
            topics_html += f"<li><b>Tópico {i+1}:</b> {formatted_topic}</li>"

            topic_data.append(
                {
                    "topic_id": i + 1,
                    "words": words,
                    "probabilities": [float(p) for p in probabilities],
                }
            )

        topics_html += "</ul>"

        print("Modelagem de tópicos LDA concluída.")
        return topics_html, lda_model, topic_data

    except Exception as e:
        print(f"ERRO ao treinar modelo LDA: {e}")
        return f"Erro na modelagem de tópicos: {e}", None, None


def perform_clustering_analysis(tokens, output_dir, filename_prefix):
    """Realiza análise de clustering com visualizações."""
    print("Realizando análise de clustering...")

    if len(tokens) < 50:
        return "Texto insuficiente para clustering.", None

    try:
        # Criar documentos artificiais dividindo tokens
        chunk_size = 50
        chunks = [
            " ".join(tokens[i : i + chunk_size])
            for i in range(0, len(tokens), chunk_size)
        ]

        if len(chunks) < 3:
            return "Texto insuficiente para clustering.", None

        # Vetorização TF-IDF
        vectorizer = TfidfVectorizer(max_features=200, stop_words=list(STOPWORDS_PT))
        tfidf_matrix = vectorizer.fit_transform(chunks)

        # K-means clustering
        optimal_k = min(5, len(chunks) // 2)
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)

        # Redução dimensional para visualização
        try:
            if hasattr(tfidf_matrix, "shape") and tfidf_matrix.shape[1] > 2:
                tsne = TSNE(
                    n_components=2, random_state=42, perplexity=min(30, len(chunks) - 1)
                )
                coords_2d = tsne.fit_transform(tfidf_matrix.toarray())
            else:
                coords_2d = tfidf_matrix.toarray()
        except Exception as e:
            print(f"Erro na redução dimensional: {e}")
            return f"Erro no clustering: {e}", None

        # Criar visualização
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(
            coords_2d[:, 0],
            coords_2d[:, 1],
            c=cluster_labels,
            cmap="viridis",
            s=100,
            alpha=0.7,
        )

        plt.title("Análise de Clustering (t-SNE)", fontsize=14, fontweight="bold")
        plt.xlabel("Dimensão 1")
        plt.ylabel("Dimensão 2")
        plt.colorbar(scatter, label="Cluster")
        plt.grid(True, alpha=0.3)

        # Salvar
        clustering_path = os.path.join(output_dir, f"clustering_{filename_prefix}.png")
        plt.tight_layout()
        plt.savefig(clustering_path, dpi=300, bbox_inches="tight")
        plt.close()

        # Caracterizar clusters
        feature_names = vectorizer.get_feature_names_out()
        cluster_info = []

        for i in range(optimal_k):
            cluster_center = kmeans.cluster_centers_[i]
            top_indices = cluster_center.argsort()[-10:][::-1]
            top_words = [str(feature_names[idx]) for idx in top_indices]
            cluster_info.append(f"**Cluster {i+1}:** {', '.join(top_words)}")

        clustering_summary = "\n".join(cluster_info)

        return clustering_summary, os.path.basename(clustering_path)

    except Exception as e:
        print(f"Erro no clustering: {e}")
        return f"Erro na análise de clustering: {e}", None


def extract_advanced_entities(text):
    """Extrai e analisa entidades nomeadas com estatísticas avançadas."""
    print("Extraindo entidades nomeadas com análise avançada...")

    try:
        doc = NLP(text)

        # Filtrar entidades
        entities = [
            (ent.text.strip().title(), ent.label_)
            for ent in doc.ents
            if len(ent.text.strip()) > 2
            and not ent.text.isnumeric()
            and not any(char.isdigit() for char in ent.text)
        ]

        if not entities:
            return "Nenhuma entidade nomeada relevante foi encontrada.", None

        # Criar DataFrame e analisar
        df = pd.DataFrame(entities, columns=["Entidade", "Tipo"])
        entity_counts = df.groupby(["Tipo", "Entidade"]).size().reset_index()
        entity_counts.columns = ["Tipo", "Entidade", "Contagem"]
        entity_counts = entity_counts.sort_values(by="Contagem", ascending=False)

        # Estatísticas por tipo
        type_stats = df["Tipo"].value_counts()

        # Criar relatório detalhado
        report_parts = []
        report_parts.append("### Estatísticas por Tipo de Entidade")
        for tipo, count in type_stats.items():
            report_parts.append(f"- **{tipo}:** {count} ocorrências")

        report_parts.append("\n### Top 25 Entidades Mais Mencionadas")
        top_entities = entity_counts.head(25)
        report_parts.append(top_entities.to_markdown(index=False))

        return "\n".join(report_parts), entity_counts

    except Exception as e:
        print(f"Erro na extração de entidades: {e}")
        return f"Erro na análise de entidades: {e}", None


def generate_llm_interpretation(text):
    """Gera interpretação especializada usando LLM com sistema multi-API e fallback."""
    import os
    import time
    import random
    
    print("Gerando interpretação com LLM...")
    
    # Carregar chaves de API
    gemini_key = os.getenv("GEMINI_API_KEY")
    xai_key = os.getenv("XAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not any([gemini_key, xai_key, groq_key, openai_key]):
        return "Interpretação LLM não disponível (nenhuma chave API configurada)."
    
    # Preparar prompt
    prompt = f"""
Como especialista em análise literária e linguística computacional, analise o seguinte texto:

{text[:3000]}...

Forneça uma interpretação focando em:
1. Temas centrais e motivos recorrentes
2. Estilo narrativo e características linguísticas
3. Contexto cultural e social evidenciado
4. Elementos culturais ou históricos evidentes
5. Particularidades da escrita ou estrutura textual

Responda de forma objetiva e acadêmica, focando nos aspectos mais relevantes para análise textual computacional.
"""
    
    # Lista de APIs disponíveis
    apis = []
    if gemini_key: apis.append('gemini')
    if xai_key: apis.append('xai')
    if groq_key: apis.append('groq')
    if openai_key: apis.append('openai')
    
    max_attempts = 48  # 4 horas com tentativas a cada 5 minutos
    attempt = 0
    
    while attempt < max_attempts:
        # Embaralhar ordem das APIs para distribuir carga
        random.shuffle(apis)
        
        for api in apis:
            try:
                if api == 'gemini' and genai:
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(prompt)
                    return response.text
                    
                elif api == 'xai':
                    import requests
                    headers = {
                        'Authorization': f'Bearer {xai_key}',
                        'Content-Type': 'application/json'
                    }
                    data = {
                        'model': 'grok-2-latest',
                        'messages': [{'role': 'user', 'content': prompt}],
                        'max_tokens': 1000
                    }
                    response = requests.post('https://api.x.ai/v1/chat/completions', 
                                           headers=headers, json=data, timeout=60)
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
                        
                elif api == 'groq':
                    import requests
                    headers = {
                        'Authorization': f'Bearer {groq_key}',
                        'Content-Type': 'application/json'
                    }
                    data = {
                        'model': 'qwen-qwq-32b',
                        'messages': [{'role': 'user', 'content': prompt}],
                        'max_tokens': 1000
                    }
                    response = requests.post('https://api.groq.com/openai/v1/chat/completions',
                                           headers=headers, json=data, timeout=60)
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
                        
                elif api == 'openai':
                    import requests
                    headers = {
                        'Authorization': f'Bearer {openai_key}',
                        'Content-Type': 'application/json'
                    }
                    data = {
                        'model': 'gpt-5',
                        'messages': [{'role': 'user', 'content': prompt}],
                        'max_tokens': 1000
                    }
                    response = requests.post('https://api.openai.com/v1/chat/completions',
                                           headers=headers, json=data, timeout=60)
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
                        
            except Exception as e:
                print(f"Erro na API {api}: {e}")
                continue
        
        # Se todas as APIs falharam, aguardar 5 minutos
        attempt += 1
        if attempt < max_attempts:
            print(f"Todas as APIs falharam. Tentativa {attempt}/{max_attempts}. Aguardando 5 minutos...")
            time.sleep(300)  # 5 minutos
    
    return "Erro: Todas as APIs falharam após múltiplas tentativas."


# --- GERAÇÃO DE RELATÓRIO PRINCIPAL ---


def generate_analysis_report(text, original_filename, output_dir):
    """Orquestra todas as análises avançadas e gera relatório consolidado."""
    filename_prefix = os.path.splitext(original_filename)[0]
    report_path = os.path.join(output_dir, f"relatorio_{filename_prefix}.md")
    print(f"Iniciando geração de relatório avançado para: {original_filename}")

    # 1. Pré-processamento
    processed_tokens = preprocess_for_analysis(text)

    # 2. **ANÁLISE REINERT (PRINCIPAL NOVIDADE)**
    print("\n=== EXECUTANDO ANÁLISE REINERT ===")
    reinert_analyzer = ReinertAnalyzer(text, min_freq=3, max_features=300)
    reinert_results = reinert_analyzer.run_complete_analysis()

    reinert_table = ""
    reinert_images = []

    if reinert_results:
        # Gerar tabela Reinert
        reinert_table = reinert_analyzer.generate_reinert_table()

        # Gerar visualizações Reinert
        dendrogram_file = reinert_analyzer.generate_dendrogram(
            output_dir, filename_prefix
        )
        if dendrogram_file:
            reinert_images.append(dendrogram_file)

        class_clouds = reinert_analyzer.generate_class_wordclouds(
            output_dir, filename_prefix, reinert_results["cluster_labels"]
        )
        reinert_images.extend(class_clouds)

        similarity_file = reinert_analyzer.generate_similarity_analysis(
            output_dir, filename_prefix
        )
        if similarity_file:
            reinert_images.append(similarity_file)

    # 3. Análises complementares
    wc_filename = generate_advanced_wordcloud(
        processed_tokens, output_dir, filename_prefix
    )
    sentiment_analysis = perform_sentiment_analysis(text)
    topics_html, lda_model, topic_data = perform_advanced_topic_modeling(
        processed_tokens, 6
    )
    clustering_summary, clustering_image = perform_clustering_analysis(
        processed_tokens, output_dir, filename_prefix
    )
    entities_report, entity_data = extract_advanced_entities(text)

    # 4. Interpretação LLM (se disponível)
    llm_interpretation = generate_llm_interpretation(text)

    # 5. Montar Relatório Completo
    report_content = f"""# Relatório de Análise Textual Avançada: {filename_prefix}

Este relatório apresenta uma análise linguística e estatística abrangente da obra, utilizando técnicas avançadas de Processamento de Linguagem Natural, Machine Learning e o **Método Reinert** de Classificação Hierárquica Descendente (CHD), seguindo os padrões do software IRaMuTeQ.

---

## Método Reinert - Classificação Hierárquica Descendente (CHD)

O Método Reinert (1983, 1991) é uma técnica estatística de análise lexicométrica que identifica automaticamente classes lexicais homogêneas no corpus textual, revelando os "mundos lexicais" ou universos de sentido presentes no texto através de Classificação Hierárquica Descendente maximizando a estatística χ².

### Resultados da Classificação Hierárquica Descendente

{reinert_table}

### Dendrograma da CHD

O dendrograma abaixo mostra a estrutura hierárquica da classificação, ilustrando como os segmentos de texto foram agrupados:

"""

    # Adicionar imagens do Método Reinert
    for img_file in reinert_images:
        if "dendrograma" in img_file:
            report_content += f"![Dendrograma CHD](./{img_file})\n\n"
        elif "classe_" in img_file:
            class_num = img_file.split("_")[1]
            report_content += f"#### Nuvem de Palavras - Classe {class_num}\n\n![Classe {class_num}](./{img_file})\n\n"
        elif "similitude" in img_file:
            report_content += f"### Análise de Similitude\n\nA análise de similitude mostra as relações de coocorrência entre as palavras mais frequentes:\n\n![Análise de Similitude](./{img_file})\n\n"

    # Continuar com outras análises
    report_content += f"""---

## Nuvem de Palavras Geral

A nuvem de palavras oferece uma visualização das palavras mais frequentes após lematização e remoção de stopwords:

"""

    if wc_filename:
        report_content += f"![Nuvem de Palavras Geral](./{wc_filename})\n\n"

    report_content += f"""---

## Interpretação Especializada (LLM)

{llm_interpretation}

---

## Análise de Sentimentos

"""

    if sentiment_analysis:
        report_content += f"""
- **Polaridade:** {sentiment_analysis['polarity']:.3f} ({sentiment_analysis['sentiment_label']})
- **Subjetividade:** {sentiment_analysis['subjectivity']:.3f} ({sentiment_analysis['subjectivity_label']})

A polaridade varia de -1 (muito negativo) a +1 (muito positivo). A subjetividade varia de 0 (objetivo) a 1 (subjetivo).
"""
    else:
        report_content += "Análise de sentimentos não disponível.\n"

    report_content += f"""---

## Modelagem de Tópicos LDA (Complementar)

Além das classes Reinert, a modelagem LDA identifica tópicos latentes baseados em coocorrências:

{topics_html}

---

## Análise de Clustering

{clustering_summary}
"""

    if clustering_image:
        report_content += f"\n![Clustering Analysis](./{clustering_image})\n"

    report_content += f"""---

## Entidades Nomeadas (NER)

{entities_report}

---

## Estatísticas Gerais

- **Total de tokens processados:** {len(processed_tokens):,}
- **Vocabulário único:** {len(set(processed_tokens)):,}
- **Densidade lexical:** {len(set(processed_tokens))/len(processed_tokens):.3f}

---

**Relatório gerado automaticamente com técnicas avançadas de Processamento de Linguagem Natural (NLP), Machine Learning (ML) e Método Reinert (CHD).**

**Tecnologias Utilizadas:** Método Reinert (1983, 1991), Modelos de Linguagem (LLM), Processamento e Análise Documental, Interfaces de Programação de IA, Processamento de Linguagem Natural (PLN), Aprendizado de Máquina e Mineração de Dados, Geração de Visualizações e Gráficos, Análise Estatística Avançada, Ferramentas de Produtividade, Análise Textual Aprofundada, Computação Paralela e Distribuída, e Estruturação de Relatórios Técnicos.

---

## Consultoria

David C Cavalcante

AI ML Engineer | Researcher Scientist | LLM Philosopher

- Email: [davcavalcante@proton.me](mailto:davcavalcante@proton.me)
- LinkedIn: [David C Cavalcante](https://linkedin.com/in/hellodav)
"""

    # Salvar relatório
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"Relatório avançado salvo em: {os.path.basename(report_path)}")
    total_images = len(reinert_images if reinert_images else [])
    total_images += 1 if wc_filename else 0
    total_images += 1 if clustering_image else 0
    print(f"Arquivos de visualização gerados: {total_images}")
