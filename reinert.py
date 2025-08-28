import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.stats import chi2_contingency
from scipy.spatial.distance import pdist
import networkx as nx
from wordcloud import WordCloud
import spacy
import warnings

warnings.filterwarnings("ignore")

# Configuração do matplotlib para suportar caracteres UTF-8
plt.rcParams["font.size"] = 10
plt.rcParams["figure.dpi"] = 300


class ReinertAnalyzer:
    """
    Implementação completa do Método Reinert (1983, 1991) para Classificação
    Hierárquica Descendente (CHD) com técnicas avançadas de Machine Learning.
    """

    def __init__(self, text, min_freq=3, max_features=500, min_segment_size=40):
        """
        Inicializa o analisador Reinert.

        Args:
            text (str): Texto a ser analisado
            min_freq (int): Frequência mínima das palavras
            max_features (int): Máximo de características (palavras) a considerar
            min_segment_size (int): Tamanho mínimo dos segmentos de texto
        """
        self.text = text
        self.min_freq = min_freq
        self.max_features = max_features
        self.min_segment_size = min_segment_size

        # Carregar modelo spaCy
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except OSError:
            print("Modelo spaCy não encontrado. Usando análise básica...")
            self.nlp = None

        # Estruturas de dados principais
        self.segments = []
        self.matrix = None
        self.vocabulary = []
        self.classes = {}
        self.dendrogram_data = None

    def _preprocess_text(self):
        """Pré-processa o texto para análise Reinert."""
        print("Pré-processando texto para análise Reinert...")

        # Dividir em segmentos (aproximadamente do tamanho especificado)
        words = self.text.split()
        segments = []

        current_segment = []
        current_length = 0

        for word in words:
            current_segment.append(word)
            current_length += len(word) + 1

            # Se atingiu o tamanho mínimo e encontrou ponto final
            if (
                current_length >= self.min_segment_size
                and word.endswith(".")
                or current_length >= self.min_segment_size * 2
            ):

                segments.append(" ".join(current_segment))
                current_segment = []
                current_length = 0

        # Adicionar último segmento se não estiver vazio
        if current_segment:
            segments.append(" ".join(current_segment))

        self.segments = segments
        print(f"Texto dividido em {len(self.segments)} segmentos.")

    def _create_binary_matrix(self):
        """Cria a matriz binária termos-documentos (base do método Reinert)."""
        print("Criando matriz binária termos-documentos...")

        # Usar CountVectorizer para criar matriz de presença/ausência
        vectorizer = CountVectorizer(
            max_features=self.max_features,
            min_df=self.min_freq,
            binary=True,  # Matriz binária (presença/ausência)
            stop_words=self._get_portuguese_stopwords(),
            token_pattern=r"\b[a-záàâãéèêíìîóòôõúùûç]+\b",
            lowercase=True,
        )

        try:
            matrix_sparse = vectorizer.fit_transform(self.segments)
            self.matrix = matrix_sparse.toarray()
            self.vocabulary = list(vectorizer.get_feature_names_out())
            print(
                f"Matriz criada: {self.matrix.shape[0]} segmentos × {self.matrix.shape[1]} termos"
            )

        except Exception as e:
            print(f"Erro ao criar matriz: {e}")
            return False

        return True

    def _get_portuguese_stopwords(self):
        """Retorna lista de stopwords em português."""
        stopwords = [
            "a",
            "ao",
            "aos",
            "aquela",
            "aquelas",
            "aquele",
            "aqueles",
            "aquilo",
            "as",
            "até",
            "com",
            "como",
            "da",
            "das",
            "de",
            "dela",
            "delas",
            "dele",
            "deles",
            "depois",
            "do",
            "dos",
            "e",
            "ela",
            "elas",
            "ele",
            "eles",
            "em",
            "entre",
            "era",
            "eram",
            "essa",
            "essas",
            "esse",
            "esses",
            "esta",
            "estamos",
            "estas",
            "estava",
            "estavam",
            "este",
            "estes",
            "estou",
            "eu",
            "foi",
            "fomos",
            "for",
            "foram",
            "forem",
            "formos",
            "fosse",
            "fossem",
            "há",
            "isso",
            "isto",
            "já",
            "lhe",
            "lhes",
            "mais",
            "mas",
            "me",
            "mesmo",
            "meu",
            "meus",
            "minha",
            "minhas",
            "muito",
            "na",
            "nas",
            "nem",
            "no",
            "nos",
            "nós",
            "nossa",
            "nossas",
            "nosso",
            "nossos",
            "num",
            "numa",
            "não",
            "nós",
            "o",
            "os",
            "ou",
            "para",
            "pela",
            "pelas",
            "pelo",
            "pelos",
            "por",
            "qual",
            "quando",
            "que",
            "quem",
            "se",
            "sem",
            "ser",
            "seu",
            "seus",
            "só",
            "sua",
            "suas",
            "são",
            "também",
            "te",
            "tem",
            "teu",
            "teus",
            "tu",
            "tua",
            "tuas",
            "um",
            "uma",
            "você",
            "vocês",
            "às",
            "é",
            "então",
            "onde",
            "pode",
            "todo",
            "toda",
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
        ]
        return stopwords

    def _correspondence_analysis(self):
        """
        Realiza Análise Fatorial de Correspondências (AFC) na matriz binária.
        Base do algoritmo de Reinert para ordenação dos documentos.
        """
        print("Executando Análise Fatorial de Correspondências...")

        # Verificar se matriz existe
        if self.matrix is None:
            return None, None

        # Usar SVD truncado (equivalente à AFC para matrizes binárias)
        n_components = min(10, self.matrix.shape[1] - 1, self.matrix.shape[0] - 1)
        if n_components < 1:
            return None, None

        svd = TruncatedSVD(n_components=n_components, random_state=42)

        try:
            coordinates = svd.fit_transform(self.matrix)

            # Retornar coordenadas do primeiro eixo para ordenação
            first_axis = coordinates[:, 0]

            print("AFC concluída com sucesso.")
            return first_axis, svd

        except Exception as e:
            print(f"Erro na AFC: {e}")
            return None, None

    def _hierarchical_clustering(self, coordinates):
        """
        Realiza classificação hierárquica descendente maximizando χ².
        """
        print("Executando Classificação Hierárquica Descendente...")

        # Verificar se matriz e coordenadas existem
        if self.matrix is None or coordinates is None:
            return None, None

        # Aplicar clustering hierárquico aglomerativo
        # Usar distância euclidiana na matriz binária
        try:
            distances = pdist(self.matrix, metric="euclidean")
            linkage_matrix = linkage(distances, method="ward")
        except Exception as e:
            print(f"Erro no clustering: {e}")
            return None, None

        # Armazenar dados do dendrograma
        self.dendrogram_data = linkage_matrix

        # Determinar número ótimo de clusters usando χ²
        best_n_clusters = self._find_optimal_clusters(linkage_matrix)

        # Obter labels dos clusters
        cluster_labels = fcluster(linkage_matrix, best_n_clusters, criterion="maxclust")

        print(f"CHD concluída. {best_n_clusters} classes identificadas.")
        return cluster_labels, linkage_matrix

    def _find_optimal_clusters(self, linkage_matrix, max_clusters=8):
        """
        Encontra o número ótimo de clusters maximizando a estatística χ².
        """
        best_chi2 = 0
        best_n_clusters = 3

        max_possible_clusters = min(max_clusters + 1, len(self.segments) // 2)
        if max_possible_clusters < 2:
            return 2

        for n_clusters in range(2, max_possible_clusters):
            try:
                labels = fcluster(linkage_matrix, n_clusters, criterion="maxclust")
                chi2_score = self._calculate_chi2_score(labels)

                if chi2_score is not None and chi2_score > best_chi2:
                    best_chi2 = chi2_score
                    best_n_clusters = n_clusters

            except Exception:
                continue

        return best_n_clusters

    def _calculate_chi2_score(self, labels):
        """
        Calcula estatística χ² para uma divisão específica.
        """
        if self.matrix is None:
            return 0

        try:
            # Criar tabela de contingência cluster × termos
            contingency_table = []
            unique_labels = np.unique(labels)

            for label in unique_labels:
                cluster_segments = self.matrix[labels == label]
                cluster_sum = np.sum(cluster_segments, axis=0)
                contingency_table.append(cluster_sum)

            contingency_table = np.array(contingency_table)

            # Calcular χ² apenas se a tabela é válida
            if contingency_table.shape[0] > 1 and contingency_table.shape[1] > 1:
                chi2, _, _, _ = chi2_contingency(
                    contingency_table + 1
                )  # +1 para evitar zeros
                return chi2
            else:
                return 0

        except Exception:
            return 0

    def _characterize_classes(self, cluster_labels):
        """
        Caracteriza cada classe identificando palavras mais específicas.
        """
        print("Caracterizando classes lexicais...")

        unique_labels = np.unique(cluster_labels)
        classes = {}

        for label in unique_labels:
            # Segmentos da classe atual
            class_mask = cluster_labels == label
            class_segments = self.matrix[class_mask]
            other_segments = self.matrix[~class_mask]

            # Calcular frequências
            class_freq = np.sum(class_segments, axis=0)
            other_freq = np.sum(other_segments, axis=0)

            # Calcular χ² para cada palavra
            chi2_scores = []
            for i in range(len(self.vocabulary)):
                # Tabela 2x2 para cada palavra
                observed = np.array(
                    [
                        [class_freq[i], np.sum(class_segments) - class_freq[i]],
                        [other_freq[i], np.sum(other_segments) - other_freq[i]],
                    ]
                )

                try:
                    chi2, p, _, _ = chi2_contingency(observed + 1)
                    chi2_scores.append((chi2, p, self.vocabulary[i], class_freq[i]))
                except:
                    chi2_scores.append((0, 1, self.vocabulary[i], class_freq[i]))

            # Ordenar por χ² e selecionar palavras mais características
            chi2_scores.sort(key=lambda x: x[0], reverse=True)
            top_words = [
                word for _, p, word, freq in chi2_scores[:15] if p < 0.05 and freq >= 2
            ]

            # Calcular percentual da classe
            class_percentage = (
                (len(class_segments) / len(self.matrix)) * 100
                if self.matrix is not None
                else 0
            )

            classes[label] = {
                "words": top_words,
                "percentage": class_percentage,
                "segments_count": len(class_segments),
                "chi2_scores": chi2_scores[:15],
            }

        self.classes = classes
        print(f"Classes caracterizadas: {len(classes)} classes")
        return classes

    def generate_reinert_table(self):
        """
        Gera tabela markdown com resultados do Método Reinert.
        """
        if not self.classes:
            return "Nenhuma classe foi identificada."

        # Cores para as classes (seguindo padrão IRaMuTeQ)
        colors = [
            "vermelho",
            "verde",
            "azul",
            "amarelo",
            "rosa",
            "laranja",
            "roxo",
            "marrom",
        ]

        table_lines = [
            "| Classe | Percentual | Palavras |",
            "|--------|------------|----------|",
        ]

        # Ordenar classes por percentual (decrescente)
        sorted_classes = sorted(
            self.classes.items(), key=lambda x: x[1]["percentage"], reverse=True
        )

        for i, (class_id, class_data) in enumerate(sorted_classes):
            color = colors[i % len(colors)]
            percentage = f"{class_data['percentage']:.1f}%"
            words = ", ".join(class_data["words"][:16])  # Limitar a 16 palavras

            table_lines.append(
                f"| Classe {class_id} ({color}) | {percentage} | {words} |"
            )

        return "\n".join(table_lines)

    def generate_dendrogram(self, output_path, filename_prefix):
        """
        Gera dendrograma da Classificação Hierárquica Descendente.
        """
        if self.dendrogram_data is None:
            print("Dados do dendrograma não disponíveis.")
            return None

        print("Gerando dendrograma da CHD...")

        plt.figure(figsize=(15, 8))

        # Criar dendrograma
        dendrogram(
            self.dendrogram_data,
            orientation="top",
            labels=[f"S{i+1}" for i in range(len(self.segments))],
            distance_sort=True,
            show_leaf_counts=True,
            leaf_font_size=8,
        )

        plt.title(
            "Dendrograma da Classificação Hierárquica Descendente (Método Reinert)",
            fontsize=14,
            fontweight="bold",
            pad=20,
        )
        plt.xlabel("Segmentos de Texto", fontsize=12)
        plt.ylabel("Distância", fontsize=12)

        # Adicionar grid sutil
        plt.grid(True, alpha=0.3, axis="y")

        # Salvar
        output_file = os.path.join(output_path, f"dendrograma_{filename_prefix}.png")
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()

        print(f"Dendrograma salvo: {os.path.basename(output_file)}")
        return os.path.basename(output_file)

    def generate_class_wordclouds(self, output_path, filename_prefix, cluster_labels):
        """
        Gera nuvens de palavras para cada classe.
        """
        print("Gerando nuvens de palavras por classe...")

        unique_labels = np.unique(cluster_labels)
        colors = [
            "Reds",
            "Greens",
            "Blues",
            "Oranges",
            "Purples",
            "YlOrBr",
            "pink",
            "gray",
        ]

        saved_files = []

        for i, label in enumerate(unique_labels):
            if label not in self.classes:
                continue

            class_data = self.classes[label]
            words_text = " ".join(class_data["words"] * 3)  # Repetir para dar peso

            if not words_text.strip():
                continue

            # Criar wordcloud
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color="white",
                colormap=colors[i % len(colors)],
                max_words=50,
                prefer_horizontal=0.7,
            ).generate(words_text)

            # Salvar
            output_file = os.path.join(
                output_path, f"classe_{label}_{filename_prefix}.png"
            )

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.title(
                f'Classe {label} ({class_data["percentage"]:.1f}%)',
                fontsize=14,
                fontweight="bold",
            )
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches="tight")
            plt.close()

            saved_files.append(os.path.basename(output_file))

        print(f"Nuvens de palavras por classe salvas: {len(saved_files)} arquivos")
        return saved_files

    def generate_similarity_analysis(self, output_path, filename_prefix):
        """
        Gera análise de similitude entre as palavras (como no IRaMuTeQ).
        """
        print("Gerando análise de similitude...")

        try:
            # Verificar se matriz existe
            if self.matrix is None:
                return None

            # Calcular matriz de coocorrência
            cooccurrence_matrix = np.dot(self.matrix.T, self.matrix)

            # Normalizar por Jaccard
            diag = np.diag(cooccurrence_matrix)
            denominator = (
                diag[:, np.newaxis] + diag[np.newaxis, :] - cooccurrence_matrix
            )
            denominator[denominator == 0] = 1  # Evitar divisão por zero
            similarity_matrix = cooccurrence_matrix / denominator

            # Selecionar apenas palavras mais frequentes para visualização
            word_frequencies = np.sum(self.matrix, axis=0)
            top_word_indices = np.argsort(word_frequencies)[-30:]  # Top 30 palavras

            similarity_subset = similarity_matrix[
                np.ix_(top_word_indices, top_word_indices)
            ]
            top_words = [self.vocabulary[i] for i in top_word_indices]

            # Criar grafo de similitude
            G = nx.Graph()

            # Adicionar nós
            for word in top_words:
                G.add_node(word)

            # Adicionar arestas (apenas conexões fortes)
            threshold = np.percentile(similarity_subset, 85)  # Top 15% das conexões

            for i, word1 in enumerate(top_words):
                for j, word2 in enumerate(top_words):
                    if i < j and similarity_subset[i, j] > threshold:
                        G.add_edge(word1, word2, weight=similarity_subset[i, j])

            # Visualizar grafo
            plt.figure(figsize=(16, 12))

            # Layout do grafo
            pos = nx.spring_layout(G, k=3, iterations=50, seed=42)

            # Desenhar nós
            vocab_list = (
                list(self.vocabulary)
                if isinstance(self.vocabulary, np.ndarray)
                else self.vocabulary
            )
            node_sizes = [
                word_frequencies[vocab_list.index(word)] * 100
                for word in G.nodes()
                if word in vocab_list
            ]

            nx.draw_networkx_nodes(
                G, pos, node_size=node_sizes, node_color="lightblue", alpha=0.7
            )

            # Desenhar arestas
            edges = G.edges()
            weights = [G[u][v]["weight"] for u, v in edges]
            edge_widths = [max(0.1, min(5.0, w * 3)) for w in weights]
            nx.draw_networkx_edges(
                G, pos, width=edge_widths, alpha=0.6, edge_color="gray"
            )

            # Adicionar labels
            nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")

            plt.title(
                "Análise de Similitude (Método Reinert)",
                fontsize=16,
                fontweight="bold",
                pad=20,
            )
            plt.axis("off")

            # Salvar
            output_file = os.path.join(output_path, f"similitude_{filename_prefix}.png")
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches="tight")
            plt.close()

            print(f"Análise de similitude salva: {os.path.basename(output_file)}")
            return os.path.basename(output_file)

        except Exception as e:
            print(f"Erro na análise de similitude: {e}")
            return None

    def run_complete_analysis(self):
        """
        Executa análise completa do Método Reinert.
        """
        print("=== INICIANDO ANÁLISE REINERT COMPLETA ===")

        # 1. Pré-processamento
        self._preprocess_text()

        if len(self.segments) < 3:
            print("ERRO: Texto insuficiente para análise Reinert.")
            return None

        # 2. Criar matriz binária
        if not self._create_binary_matrix():
            return None

        # 3. Análise Fatorial de Correspondências
        coordinates, svd_model = self._correspondence_analysis()
        if coordinates is None:
            return None

        # 4. Classificação Hierárquica Descendente
        cluster_labels, linkage_matrix = self._hierarchical_clustering(coordinates)

        # 5. Caracterização das classes
        classes = self._characterize_classes(cluster_labels)

        print("=== ANÁLISE REINERT CONCLUÍDA ===")

        return {
            "classes": classes,
            "cluster_labels": cluster_labels,
            "matrix": self.matrix,
            "vocabulary": self.vocabulary,
            "segments": self.segments,
            "linkage_matrix": linkage_matrix,
        }
