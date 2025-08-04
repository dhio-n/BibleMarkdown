import streamlit as st
import os
import glob
from pathlib import Path
from openai import OpenAI
import re
import os
import streamlit as st

BIBLE_PATH = "versoes_online/acf2007-MHenry"

def test_bible_path():
    st.write(f"Caminho absoluto da Bíblia: {os.path.abspath(BIBLE_PATH)}")
    existe = os.path.exists(BIBLE_PATH)
    st.write(f"A pasta existe? {existe}")
    if existe:
        subpastas = os.listdir(BIBLE_PATH)
        st.write(f"Conteúdo da pasta: {subpastas}")
    else:
        st.error(f"Pasta {BIBLE_PATH} não encontrada")

test_bible_path()


# Configuração da página
st.set_page_config(
    page_title="Bíblia Digital - ACF 2007",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração da API OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

BIBLE_PATH = "versoes_online/acf2007-MHenry"

# (BIBLE_BOOKS permanece igual)

# Funções auxiliares (get_available_books, get_chapters, process_image_paths, get_image_base64, read_chapter)
# permanecem iguais, vou alterar só para incluir função para extrair versículos:

def extract_verses(content):
    """
    Extrai os versículos do conteúdo markdown, 
    retornando lista de strings no formato "**n** texto do versículo".
    """
    verses = []
    # Regex para identificar linhas de versículo no formato **n**
    for line in content.splitlines():
        if re.match(r"^\*\*\d+\*\*", line):
            verses.append(line.strip())
    return verses

def get_hebrew_translation(text):
    """Obtém tradução literal palavra por palavra do hebraico para o português"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um tradutor acadêmico de hebraico bíblico. "
                        "Receberá versículos em português e deverá retornar o equivalente hebraico "
                        "e uma tradução palavra por palavra. Use o seguinte formato:\n\n"
                        "**1**\n"
                        "יְהוָה = O Senhor\n"
                        "רֹעִי = meu pastor\n"
                        "לֹא = não\n"
                        "אֶחְסָר = faltarei\n\n"
                        "Faça isso para cada versículo enviado. Não interprete. Não resuma. "
                        "Apenas traduza e explique palavra por palavra."
                    )
                },
                {
                    "role": "user",
                    "content": f"Faça a tradução literal dos seguintes versículos:\n{text}"
                }
            ],
            max_tokens=1500,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao obter tradução: {str(e)}"


def main():
    st.title("📖 Bíblia Digital - João Ferreira de Almeida Corrigida Fiel 2007")
    st.markdown("---")

    st.sidebar.title("Navegação")

    available_books = get_available_books()
    if not available_books:
        st.error("Nenhum livro encontrado. Verifique se o diretório da Bíblia está correto.")
        return

    book_options = [f"{book_name}" for book_code, book_name in available_books]
    selected_book_name = st.sidebar.selectbox("Selecione o livro:", book_options)

    selected_book_code = None
    for book_code, book_name in available_books:
        if book_name == selected_book_name:
            selected_book_code = book_code
            break

    if selected_book_code:
        chapters = get_chapters(selected_book_code)
        if chapters:
            chapter_options = [f"Capítulo {ch}" if ch != "00" else "Introdução" for ch in chapters]
            selected_chapter_display = st.sidebar.selectbox("Selecione o capítulo:", chapter_options)

            selected_chapter = chapters[chapter_options.index(selected_chapter_display)]

            col1, col2 = st.columns([3, 1])

            with col1:
                st.header(f"{selected_book_name} - {selected_chapter_display}")

                content = read_chapter(selected_book_code, selected_chapter)
                if content:
                    st.markdown(content, unsafe_allow_html=True)
                else:
                    st.error("Não foi possível carregar o conteúdo do capítulo.")

            with col2:
                st.subheader("Ferramentas")

                if content:
                    # Extrair os versículos para seleção
                    verses = extract_verses(content)

                    if verses:
                        # Obter números dos versículos disponíveis
                        verse_numbers = [int(re.findall(r"\*\*(\d+)\*\*", v)[0]) for v in verses]
                        min_verse = min(verse_numbers)
                        max_verse = max(verse_numbers)

                        st.markdown(f"**Versículos disponíveis:** {min_verse} a {max_verse}")

                        # Seleção do intervalo de versículos (máximo 5 por vez)
                        start_verse = st.number_input(
                            "Versículo inicial para tradução (máx 5 por vez):",
                            min_value=min_verse,
                            max_value=max_verse,
                            value=min_verse,
                            step=1
                        )
                        # O final deve ser no máximo start_verse+4 e não ultrapassar max_verse
                        max_end = min(start_verse + 4, max_verse)
                        end_verse = st.number_input(
                            "Versículo final para tradução:",
                            min_value=start_verse,
                            max_value=max_end,
                            value=max_end,
                            step=1
                        )

                        if st.button("🔍 Obter Versão Original (Hebraico)"):
                            # Filtrar versículos selecionados
                            selected_verses = [v for v in verses if start_verse <= int(re.findall(r"\*\*(\d+)\*\*", v)[0]) <= end_verse]
                            text_to_translate = "\n".join(selected_verses)

                            with st.spinner("Consultando versão original..."):
                                translation = get_hebrew_translation(text_to_translate)
                                st.subheader("Versão Original e Tradução")
                                st.text_area("Resultado:", translation, height=300)
                    else:
                        st.warning("Não foi possível extrair versículos para tradução.")

                st.markdown("---")
                st.markdown("**Sobre esta versão:**")
                st.markdown("João Ferreira de Almeida Corrigida Fiel 2007")
                st.markdown("Considerada uma das traduções mais fiéis ao texto original em português.")

        else:
            st.warning("Nenhum capítulo encontrado para este livro.")

if __name__ == "__main__":
    main()
