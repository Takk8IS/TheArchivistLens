import os
import shutil
from dotenv import load_dotenv
import processing
import analysis
from tqdm import tqdm
import time

# Carrega as variáveis de ambiente (GEMINI_API_KEY)
load_dotenv()

# --- CONFIGURAÇÃO DOS DIRETÓRIOS ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
CLEAN_TEXT_DIR = os.path.join(OUTPUT_DIR, "textos_limpos")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "relatorios")


def clean_output_directories():
    """Limpa e recria os diretórios de saída para uma execução limpa."""
    print("Limpando diretórios de saída...")
    for dir_path in [CLEAN_TEXT_DIR, REPORTS_DIR]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    print("Diretórios de saída preparados para execução limpa.")


def main():
    """Orquestra o pipeline completo de análise de documentos com Método Reinert."""
    print("=" * 80)
    print("INICIANDO O PIPELINE DE ANÁLISE TEXTUAL AVANÇADA")
    print("Incluindo: Método Reinert (CHD), ML Avançado e Análise LLM")
    print("=" * 80)

    # Etapa 1: Preparar os diretórios de saída
    clean_output_directories()

    start_time = time.time()

    # Etapa 2: Verificar APIs disponíveis
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    available_apis = []

    if gemini_api_key:
        available_apis.append("Gemini")
    if os.getenv("XAI_API_KEY"):
        available_apis.append("xAI")
    if os.getenv("GROQ_API_KEY"):
        available_apis.append("Groq")
    if os.getenv("OPENAI_API_KEY"):
        available_apis.append("OpenAI")

    if not available_apis:
        print("AVISO: Nenhuma API key encontrada.")
        print("O sistema funcionará com análises básicas, mas sem refinamento LLM.")
        print("Para melhor qualidade, configure pelo menos uma API em .env")
    else:
        print(f"APIs disponíveis: {', '.join(available_apis)}")

    # Etapa 3: Processar cada documento individualmente
    all_docs = [f for f in os.listdir(DOCS_DIR) if not f.startswith(".")]
    corpus_completo_text = ""

    print(f"\nDocumentos encontrados: {len(all_docs)}")

    # Usar barra de progresso
    for i, filename in enumerate(tqdm(all_docs, desc="Processando documentos")):
        print(f"\n{'='*60}")
        print(f"PROCESSANDO ({i+1}/{len(all_docs)}): {filename}")
        print(f"{'='*60}")
        doc_path = os.path.join(DOCS_DIR, filename)

        # 1. Conversão para texto bruto
        raw_text = processing.convert_to_text(doc_path)
        if not raw_text:
            continue

        # 2. Limpeza programática inicial
        cleaned_text = processing.clean_text_programmatically(raw_text, filename)

        # 3. Revisão e limpeza final com LLM (se disponível)
        if available_apis:
            print("Iniciando revisão com modelo de linguagem (LLM)...")
            final_text = processing.review_and_refine_with_llm(
                cleaned_text, gemini_api_key
            )
        else:
            print("Pulando refinamento LLM (nenhuma API disponível)")
            final_text = cleaned_text

        # 4. Salvar o texto limpo
        clean_text_path = os.path.join(
            CLEAN_TEXT_DIR, f"{os.path.splitext(filename)[0]}.txt"
        )
        with open(clean_text_path, "w", encoding="utf-8") as f:
            f.write(final_text)
        print(f"Texto limpo salvo: {os.path.basename(clean_text_path)}")

        # 5. Acumular para o corpus completo
        corpus_completo_text += final_text + "\n\n---\n\n"

        # 6. Gerar relatório de análise avançada (Método Reinert + ML)
        print(f"Gerando análise avançada para {filename}...")
        analysis.generate_analysis_report(final_text, filename, REPORTS_DIR)
        print(f"Relatório completo gerado!")

    # Etapa 4: Análise do Corpus Completo
    print(f"\n{'='*60}")
    print(f"PROCESSANDO: CORPUS COMPLETO (TODOS OS DOCUMENTOS)")
    print(f"{'='*60}")

    corpus_filename = "corpus_completo.txt"
    clean_corpus_path = os.path.join(CLEAN_TEXT_DIR, corpus_filename)
    with open(clean_corpus_path, "w", encoding="utf-8") as f:
        f.write(corpus_completo_text)
    print("Corpus completo consolidado.")

    print("Executando análise avançada do corpus completo...")
    analysis.generate_analysis_report(
        corpus_completo_text, corpus_filename, REPORTS_DIR
    )

    # Estatísticas finais
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\n" + "=" * 80)
    print("PIPELINE COMPLETO CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print(f"Tempo total de execução: {elapsed_time:.1f} segundos")
    print(f"Todos os resultados foram gerados em: {OUTPUT_DIR}")
    print(f"Documentos processados: {len(all_docs)}")
    print(f"Relatórios gerados: {len(all_docs) + 1} (individuais + corpus completo)")
    print(f"Método Reinert (CHD) aplicado a todos os documentos")
    print(
        f"APIs utilizadas: {', '.join(available_apis) if available_apis else 'Nenhuma'}"
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
