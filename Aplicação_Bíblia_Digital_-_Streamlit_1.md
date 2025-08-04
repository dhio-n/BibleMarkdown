# Aplicação Bíblia Digital - Streamlit

## Descrição

Esta é uma aplicação web desenvolvida em Streamlit que permite a leitura da Bíblia em formato digital, utilizando os arquivos Markdown do repositório BibleMarkdown. A aplicação inclui integração com a API da OpenAI para fornecer traduções para o hebraico original e traduções diretas para o português moderno.

## Características

- **Interface intuitiva**: Navegação fácil por livros e capítulos da Bíblia
- **Texto completo**: Versão João Ferreira de Almeida Corrigida Fiel 2007
- **Comentários incluídos**: Comentários de Matthew Henry integrados ao texto
- **Imagens**: Ilustrações do SweetPublishing incluídas nos textos
- **Integração OpenAI**: Funcionalidade para obter versões originais em hebraico e traduções modernas
- **Layout responsivo**: Interface adaptada para diferentes tamanhos de tela

## Estrutura dos Dados

A aplicação utiliza os arquivos Markdown organizados da seguinte forma:
```
BibleMarkdown/versoes_online/acf2007-MHenry/
├── 01A-Gn/          # Gênesis
│   ├── 01.md        # Capítulo 1
│   ├── 02.md        # Capítulo 2
│   └── ...
├── 02A-Ex/          # Êxodo
└── ...
```

## Funcionalidades

### 1. Navegação
- Seleção de livros através de dropdown
- Seleção de capítulos específicos
- Interface sidebar para navegação rápida

### 2. Leitura
- Exibição do texto bíblico formatado
- Comentários de Matthew Henry integrados
- Imagens ilustrativas quando disponíveis

### 3. Tradução (OpenAI)
- Botão "Obter Versão Original" para consultar traduções
- Integração com GPT-4o-mini para traduções precisas
- Exibição de versões em hebraico e traduções modernas

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- Streamlit
- OpenAI Python SDK
- Repositório BibleMarkdown clonado

### Passos para execução

1. **Clone o repositório da Bíblia:**
```bash
git clone https://github.com/ameisehaufen/BibleMarkdown.git
```

2. **Instale as dependências:**
```bash
pip install streamlit openai
```

3. **Configure as variáveis de ambiente:**
```bash
export OPENAI_API_KEY="sua_chave_api"
export OPENAI_API_BASE="url_base_da_api"
```

4. **Execute a aplicação:**
```bash
streamlit run bible_app.py --server.port 8501 --server.address 0.0.0.0
```

5. **Acesse no navegador:**
```
http://localhost:8501
```

## Configuração da API OpenAI

A aplicação está configurada para usar o modelo `gpt-4o-mini` da OpenAI. Para funcionar corretamente, você precisa:

1. Ter uma chave de API válida da OpenAI
2. Configurar as variáveis de ambiente `OPENAI_API_KEY` e `OPENAI_API_BASE`
3. Ter créditos suficientes na conta OpenAI

## Estrutura do Código

### Principais Componentes

- **`BIBLE_BOOKS`**: Mapeamento dos códigos dos livros para nomes legíveis
- **`get_available_books()`**: Função para listar livros disponíveis
- **`get_chapters()`**: Função para listar capítulos de um livro
- **`read_chapter()`**: Função para ler conteúdo de um capítulo
- **`get_hebrew_translation()`**: Integração com OpenAI para traduções
- **`main()`**: Interface principal da aplicação

### Layout da Interface

- **Sidebar**: Navegação por livros e capítulos
- **Área principal**: Exibição do conteúdo bíblico
- **Área de ferramentas**: Botões para funcionalidades extras
- **Área de informações**: Detalhes sobre a versão da Bíblia

## Limitações Conhecidas

1. **Dependência de internet**: Necessária para funcionalidades da OpenAI
2. **Custo da API**: Uso da OpenAI pode gerar custos
3. **Tamanho dos arquivos**: Repositório completo é relativamente grande
4. **Formato das imagens**: Algumas imagens podem não carregar corretamente

## Melhorias Futuras

- [ ] Cache local para traduções já consultadas
- [ ] Busca por versículos específicos
- [ ] Comparação entre diferentes versões
- [ ] Exportação de capítulos em PDF
- [ ] Sistema de favoritos/marcadores
- [ ] Modo escuro/claro
- [ ] Suporte a outras línguas

## Licença

Esta aplicação utiliza conteúdo do repositório BibleMarkdown, que está sob licença Unlicense. A aplicação em si é fornecida como está, para fins educacionais e de estudo.

## Créditos

- **Texto bíblico**: João Ferreira de Almeida Corrigida Fiel 2007
- **Comentários**: Matthew Henry
- **Imagens**: SweetPublishing
- **Repositório fonte**: [ameisehaufen/BibleMarkdown](https://github.com/ameisehaufen/BibleMarkdown)
- **Framework**: Streamlit
- **IA**: OpenAI GPT-4o-mini

