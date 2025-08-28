# Relatório de Análise Textual Avançada: O Regresso do Morto

Este relatório apresenta uma análise linguística e estatística abrangente da obra, utilizando técnicas avançadas de Processamento de Linguagem Natural, Machine Learning e o **Método Reinert** de Classificação Hierárquica Descendente (CHD), seguindo os padrões do software IRaMuTeQ.

---

## Método Reinert - Classificação Hierárquica Descendente (CHD)

O Método Reinert (1983, 1991) é uma técnica estatística de análise lexicométrica que identifica automaticamente classes lexicais homogêneas no corpus textual, revelando os "mundos lexicais" ou universos de sentido presentes no texto através de Classificação Hierárquica Descendente maximizando a estatística χ².

### Resultados da Classificação Hierárquica Descendente

| Classe | Percentual | Palavras |
|--------|------------|----------|
| Classe 8 (vermelho) | 77.3% | olhos, laurinda, cabeça, vai, pão, parece, velho, burro, agora, assim, quer |
| Classe 3 (verde) | 5.3% | laurinda, pão, coração, quer, alcatrão, mbunhar, esperança, balcão, força, outra, onda, boca, bater, bicha |
| Classe 5 (azul) | 5.1% | parece, vai, stá, agora, qu, rir, ngilina, bate, chega, descer, difícil, saco, xonguile, boca, ali |
| Classe 7 (amarelo) | 3.8% | assim, burro, mbongolo, vida, sempre, zurro, cidade, quase, ti, xicuembo, tinha, bom, muinto, fora |
| Classe 1 (rosa) | 2.9% | olhos, cachimbo, la, madalena, vez |
| Classe 2 (laranja) | 2.2% | cabeça, levava, bacia, lentamente, sombra, cesto |
| Classe 6 (roxo) | 1.9% | velho, djimo, macie, sabia, mãos |
| Classe 4 (marrom) | 1.5% | velina, vovó, nora, ficou, cesto, vai |

### Dendrograma da CHD

O dendrograma abaixo mostra a estrutura hierárquica da classificação, ilustrando como os segmentos de texto foram agrupados:

![Dendrograma CHD](./dendrograma_O%20Regresso%20do%20Morto.png)

#### Nuvem de Palavras - Classe 1

![Classe 1](./classe_1_O%20Regresso%20do%20Morto.png)

#### Nuvem de Palavras - Classe 2

![Classe 2](./classe_2_O%20Regresso%20do%20Morto.png)

#### Nuvem de Palavras - Classe 3

![Classe 3](./classe_3_O%20Regresso%20do%20Morto.png)

#### Nuvem de Palavras - Classe 4

![Classe 4](./classe_4_O%20Regresso%20do%20Morto.png)

#### Nuvem de Palavras - Classe 5

![Classe 5](./classe_5_O%20Regresso%20do%20Morto.png)

#### Nuvem de Palavras - Classe 6

![Classe 6](./classe_6_O%20Regresso%20do%20Morto.png)

#### Nuvem de Palavras - Classe 7

![Classe 7](./classe_7_O%20Regresso%20do%20Morto.png)

#### Nuvem de Palavras - Classe 8

![Classe 8](./classe_8_O%20Regresso%20do%20Morto.png)

### Análise de Similitude

A análise de similitude mostra as relações de coocorrência entre as palavras mais frequentes:

![Análise de Similitude](./similitude_O%20Regresso%20do%20Morto.png)

---

## Nuvem de Palavras Geral

A nuvem de palavras oferece uma visualização das palavras mais frequentes após lematização e remoção de stopwords:

![Nuvem de Palavras Geral](./wordcloud_O%20Regresso%20do%20Morto.png)

---

## Interpretação Especializada (LLM)

A análise do excerto "O Regresso do Morto" revela uma complexa tapeçaria de elementos literários e linguísticos, profundamente enraizados em um contexto sociocultural específico. Do ponto de vista da análise textual computacional, o texto oferece um corpus rico para o estudo de variações linguísticas, padrões discursivos e representações culturais.

---

### Análise Literária e Linguística Computacional do Excerto:

#### 1. Temas Centrais e Motivos Recorrentes:

*   **Opressão e Violência de Gênero:** Este é o tema dominante. A vida de Ngilina é caracterizada por "insultos sempre-sempre", "muinto porrada", violência física ("Chaga na bochecha, boca inchada, nariz arranhado, dentes partido"), e a ausência de autonomia sobre seu próprio corpo e destino ("ele queria sempre, todos os dias. Como diria não, se lhe pertencia?"). O "lobolo" é apresentado como um mecanismo de alienação e subjugação.
    *   *Relevância Computacional:* A frequência de termos relacionados à dor ("dores na coluna, nas ancas, na cabeça"), violência ("porrada," "partido"), e emoções negativas ("coração inchado," "pesado na garganta," "lágrimas caladas") seria um indicador forte em análises de sentimento e emoção. A identificação de relações de posse e agência ("lhe pertencia," "o pai queria. Mandava.") poderia ser explorada através de parsing sintático e semântico para mapear as dinâmicas de poder.
*   **Morte como Libertação:** O desejo de morrer ("É melhor morrer mesmo. Morrer é mesmo bom. Tudo acaba, tudo. Sim vale a pena morrer...") surge como uma reação extrema à insuportabilidade da vida, contrastando com a resignação forçada ("Mas é assim vida de mulher. Paciença...").
    *   *Relevância Computacional:* A co-ocorrência de termos de morte com palavras que expressam alívio ou fim ("acaba," "bom") em contraste com palavras de sofrimento é um padrão interessante para análise de temas de desespero e escapismo.
*   **Trabalho, Monotonia e Resiliência Forçada:** A descrição da Ngilina pilando, preparando comida e realizando tarefas domésticas pesadas ilustra uma rotina exaustiva e repetitiva. O "corpo da Ngilina também sobe também desce" mimetiza o movimento do pilão.
    *   *Relevância Computacional:* A repetição lexical e sintática ("Pau-de-pilão sobe, pau-de-pilão desce," "Não esquecer...") é altamente detectável e quantificável. Análises de N-gramas e janelas de co-ocorrência revelariam a associação entre o ato de pilar, o corpo de Ngilina e termos de exaustão/sofrimento.

#### 2. Estilo Narrativo e Características Linguísticas:

*   **Oralidade e Variação Linguística (Língua Vernácula/Crioula/Dialetal):** O texto emprega uma linguagem que mimetiza a fala coloquial e apresenta desvios da norma padrão do português europeu ou brasileiro, como "tu vai morrer", "Assim é vida?", "muinto porrada", "Paciença", "qu'stá subir-descer", "Prímeiro", "qu'stou doente". A grafia "Ngilina 'stá pilar" é um exemplo de elisão comum na fala.
    *   *Relevância Computacional:* Esta característica é crucial para Processamento de Linguagem Natural (PLN). Exige modelos de linguagem robustos que possam lidar com variações dialetais, gírias e desvios gramaticais. Técnicas de normalização de texto seriam essenciais para padronizar as palavras para dicionários ou embeddings de palavras, enquanto a análise de Part-of-Speech (POS) tagging e parsing sintático precisaria ser adaptada a essas particularidades. A presença de formas como "sempre-sempre" e "muito muito" (redundâncias enfáticas) é também um marcador estilístico quantificável.
*   **Code-Switching e Code-Mixing:** A integração de termos de línguas africanas ("xicuembo," "nholo," "xicuembo," "capulana de xigueguepau," "xigubo," "ncancana," "libôndzo," "wusua," "moringa," "piripíri," "Tatana," "lobolada," "xivambalana") no discurso em português é um traço marcante.
    *   *Relevância Computacional:* Este é um desafio significativo para o PLN monolíngue. Requer modelos multilíngues ou o uso de léxicos especializados para cada língua para a identificação e interpretação correta desses termos. A análise de sua frequência e distribuição pode revelar padrões de empréstimo linguístico e a profundidade da imersão cultural.
*   **Repetição e Anáfora:** A repetição de frases, palavras e estruturas sintáticas ("Pau-de-pilão sobe, pau-de-pilão desce," "Ngilina pila. A sombra também pila. Ngilina pára. A sombra também pára," "Não esquecer...") cria um ritmo e enfatiza a natureza cíclica e monótona da vida de Ngilina.
    *   *Relevância Computacional:* Ferramentas de análise textual podem quantificar a anáfora e a repetição lexical, identificar padrões rítmicos através da análise de N-gramas e cadeias de Markov, e correlacioná-los com o tema da rotina ou da intensificação.
*   **Similes e Metáforas:** As comparações são vívidas e concretas, enraizadas no cotidiano da personagem ("parece burro de puxar nholo," "parece mesmo boi de puxar charrua," "pilão faz dú, dú, dú," "micaias vermelho parece tomate maduro," "Ngilina 'stá pilar parece máquina de moer farinha," "cantiga assim parece choro de rola, parece lamento de xivambalana").
    *   *Relevância Computacional:* A identificação de estruturas "parece X" ou "como Y" é um passo inicial para detecção de linguagem figurada. A análise semântica contextual seria necessária para interpretar o significado e o efeito dessas figuras de linguagem, especialmente em um contexto cultural específico.
*   **Focalização Interna e Discurso Indireto Livre:** O texto permite acesso direto aos pensamentos e sentimentos de Ngilina ("Assim é maneira que Ngilina fala com o seu coração"), misturando a voz narrativa com a da personagem.
    *   *Relevância Computacional:* A distinção entre discurso direto, indireto e indireto livre é um problema complexo para o PLN. Requer robustas técnicas de detecção de atribuição de fala e análise de vozes narrativas para determinar quem está "falando" e qual a sua perspectiva.

#### 3. Contexto Cultural e Social Evidenciado:

*   **Patriarcado e Estrutura Familiar Tradicional:** A submissão da mulher ao pai e ao marido é explícita. O pai "mandava", e Ngilina "lhe pertencia". O "lobolo" é um elemento central que valida esta estrutura social, transformando a mulher em propriedade transacionável. A figura da sogra no final antecipa mais opressão.
    *   *Relevância Computacional:* Análise de redes de personagens e suas interações, identificando relações de poder (agente/paciente em verbos de comando/submissão), pode iluminar a estrutura patriarcal.
*   **Divisão do Trabalho por Gênero:** As tarefas de Ngilina são estritamente domésticas e extenuantes, refletindo uma divisão tradicional do trabalho.
*   **Pobreza e Sobrevivência Rural:** A menção a pilão, milho, amendoim, ncancana, a palhota e a charrua, bem como a ausência de opções para Ngilina, sugere um ambiente rural de subsistência e dificuldades.

#### 4. Elementos Culturais ou Históricos Evidentes:

*   **Referências Específicas à Cultura Moçambicana (ou de um contexto lusófono africano):** A presença abundante de termos em línguas bantas ("xicuembo", "nholo", "capulana de xigueguepau", "xigubo", "ncancana", "libôndzo", "wusua", "lobolada", "Tatana", "xivambalana") aponta fortemente para Moçambique ou uma região culturalmente similar.
    *   *Relevância Computacional:* A compilação de um léxico cultural e a geolocalização de termos específicos (através de bases de dados geolinguísticas ou corroboração com especialistas) seriam passos importantes para contextualizar o texto automaticamente. A menção de "gaíça" (geralmente guarda ou vigia) também enriquece o perfil cultural.
*   **Práticas e Símbolos Tradicionais:** O "lobolo" como dote matrimonial, a "capulana" como vestimenta e símbolo (com a "mulher forte no meio de milho" representando resiliência e fertilidade), o "pilão" como ferramenta agrícola ancestral, e a referência ao "xigubo" (dança tradicional, por vezes associada a rituais de guerra ou celebração).
*   **Visão de Mundo:** A referência a "xicuembo" (deus ou espírito ancestral) como detentor do conhecimento e do destino.

#### 5. Particularidades da Escrita ou Estrutura Textual:

*   **Estrutura Fragmentada e Final Aberto:** O texto termina abruptamente com "Lá estava a sogra – a...", deixando a situação de Ngilina sem resolução imediata e reforçando a ideia de um ciclo contínuo de opressão e a falta de voz da personagem.
    *   *Relevância Computacional:* A análise da completude sintática das sentenças e a identificação de finais de texto abruptos podem ser programadas. Em termos de análise narrativa, um final aberto como este desafia a detecção automática de desfechos.
*   **Contraste entre Realidade Interior e Exterior:** A beleza do ambiente ("sol detrás da palhota, a cair entre as copas das micaias vermelho parece tomate maduro") contrasta fortemente com o sofrimento interno de Ngilina e a dureza de sua vida.
*   **Personificação e Simbiose:** A sombra de Ngilina que "também pila", "também pára" e "zombeteira, imita a Ngilina" sugere uma dualidade entre o ser e a sua representação, ou uma extensão do eu que acompanha a rotina forçada.
    *   *Relevância Computacional:* A detecção de personificação e a análise de correferência entre "Ngilina" e "sombra" revelaria essa interconexão simbólica.

---

Em suma, o excerto é um espelho de uma realidade social dura, transmitida através de uma linguagem rica e multifacetada. Para a análise computacional, representa um desafio e uma oportunidade para desenvolver modelos de PLN mais sofisticados, capazes de processar variações linguísticas, inferir contextos culturais e desvendar as camadas de significado em textos que transcendem a norma padrão.

---

## Análise de Sentimentos


- **Polaridade:** 0.000 (Neutro)
- **Subjetividade:** 0.100 (Objetivo)

A polaridade varia de -1 (muito negativo) a +1 (muito positivo). A subjetividade varia de 0 (objetivo) a 1 (subjetivo).
---

## Modelagem de Tópicos LDA (Complementar)

Além das classes Reinert, a modelagem LDA identifica tópicos latentes baseados em coocorrências:

Erro na modelagem de tópicos: cannot compute LDA over an empty collection (no terms)

---

## Análise de Clustering

**Cluster 1:** madalena, terra, coração, peito, nyeleti, gente, fabião, chuva, sol, malatana
**Cluster 2:** vovó, filho, andar, olhar, olho, velina, água, cesto, comboio, arnesto
**Cluster 3:** laurinda, pão, bicha, andar, caranguejo, sombra, bater, cabeça, mbunhar, onda
**Cluster 4:** burro, josé, bobi, mbongolo, morto, velho, chão, ninguém, cão, ngilina
**Cluster 5:** homem, mulher, pai, morrer, esperar, filho, dia, ngilina, xicuembo, minina

![Clustering Analysis](./clustering_O%20Regresso%20do%20Morto.png)
---

## Entidades Nomeadas (NER)

### Estatísticas por Tipo de Entidade
- **PER:** 234 ocorrências
- **LOC:** 188 ocorrências
- **MISC:** 52 ocorrências
- **ORG:** 17 ocorrências

### Top 25 Entidades Mais Mencionadas
| Tipo   | Entidade    |   Contagem |
|:-------|:------------|-----------:|
| PER    | Laurinda    |         25 |
| LOC    | Ngilina     |         20 |
| PER    | José        |         17 |
| PER    | Bobi        |         12 |
| PER    | Vovó Velina |         12 |
| LOC    | Madalena    |         12 |
| PER    | Malatana    |         11 |
| LOC    | Laurinda    |         10 |
| MISC   | Lucas       |         10 |
| LOC    | Foliche     |          9 |
| PER    | Arnesto     |          9 |
| PER    | Djimo       |          8 |
| PER    | Maria       |          6 |
| LOC    | Xiluva      |          6 |
| PER    | Pai Do Juse |          5 |
| LOC    | Lua         |          5 |
| LOC    | Neves       |          5 |
| PER    | Nyeleti     |          5 |
| PER    | Nkomáti     |          5 |
| PER    | Fabião      |          5 |
| LOC    | Nyeleti     |          4 |
| LOC    | Pão         |          4 |
| PER    | Marracuene  |          4 |
| PER    | Xilunguini  |          4 |
| PER    | Macie       |          3 |

---

## Estatísticas Gerais

- **Total de tokens processados:** 4,564
- **Vocabulário único:** 1,894
- **Densidade lexical:** 0.415

---

**Relatório gerado automaticamente com técnicas avançadas de Processamento de Linguagem Natural (NLP), Machine Learning (ML) e Método Reinert (CHD).**

**Tecnologias Utilizadas:** Método Reinert (1983, 1991), Modelos de Linguagem (LLM), Processamento e Análise Documental, Interfaces de Programação de IA, Processamento de Linguagem Natural (PLN), Aprendizado de Máquina e Mineração de Dados, Geração de Visualizações e Gráficos, Análise Estatística Avançada, Ferramentas de Produtividade, Análise Textual Aprofundada, Computação Paralela e Distribuída, e Estruturação de Relatórios Técnicos.

---

## Consultoria

David C Cavalcante

AI ML Engineer | Researcher Scientist | LLM Philosopher

- Email: [davcavalcante@proton.me](mailto:davcavalcante@proton.me)
- LinkedIn: [David C Cavalcante](https://linkedin.com/in/hellodav)
