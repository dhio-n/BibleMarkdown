import streamlit as st
import os
import glob
from pathlib import Path
from openai import OpenAI

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

# Caminho para os arquivos da Bíblia
BIBLE_PATH = "versoes_online/acf2007-MHenry"


# Mapeamento dos livros da Bíblia
BIBLE_BOOKS = {
    "00-Pref": "Prefácio",
    "01A-Gn": "Gênesis",
    "02A-Ex": "Êxodo", 
    "03A-Lv": "Levítico",
    "04A-Nm": "Números",
    "05A-Dt": "Deuteronômio",
    "06A-Js": "Josué",
    "07A-Jz": "Juízes",
    "08A-Rt": "Rute",
    "09A-1Sm": "1 Samuel",
    "10A-2Sm": "2 Samuel",
    "11A-1Rs": "1 Reis",
    "12A-2Rs": "2 Reis",
    "13A-1Cr": "1 Crônicas",
    "14A-2Cr": "2 Crônicas",
    "15A-Es": "Esdras",
    "16A-Ne": "Neemias",
    "17A-Et": "Ester",
    "18A-Jo": "Jó",
    "19A-Sl": "Salmos",
    "20A-Pv": "Provérbios",
    "21A-Ec": "Eclesiastes",
    "22A-Ct": "Cantares",
    "23A-Is": "Isaías",
    "24A-Jr": "Jeremias",
    "25A-Lm": "Lamentações",
    "26A-Ez": "Ezequiel",
    "27A-Dn": "Daniel",
    "28A-Os": "Oséias",
    "29A-Jl": "Joel",
    "30A-Am": "Amós",
    "31A-Ob": "Obadias",
    "32A-Jn": "Jonas",
    "33A-Mq": "Miquéias",
    "34A-Na": "Naum",
    "35A-Hc": "Habacuque",
    "36A-Sf": "Sofonias",
    "37A-Ag": "Ageu",
    "38A-Zc": "Zacarias",
    "39A-Ml": "Malaquias",
    "40N-Mt": "Mateus",
    "41N-Mc": "Marcos",
    "42N-Lc": "Lucas",
    "43N-Joa": "João",
    "44N-At": "Atos",
    "45N-Rm": "Romanos",
    "46N-1Co": "1 Coríntios",
    "47N-2Co": "2 Coríntios",
    "48N-Gl": "Gálatas",
    "49N-Ef": "Efésios",
    "50N-Fp": "Filipenses",
    "51N-Cl": "Colossenses",
    "52N-1Ts": "1 Tessalonicenses",
    "53N-2Ts": "2 Tessalonicenses",
    "54N-1Tm": "1 Timóteo",
    "55N-2Tm": "2 Timóteo",
    "56N-Tt": "Tito",
    "57N-Fm": "Filemom",
    "58N-Hb": "Hebreus",
    "59N-Tg": "Tiago",
    "60N-1Pe": "1 Pedro",
    "61N-2Pe": "2 Pedro",
    "62N-1Jo": "1 João",
    "63N-2Jo": "2 João",
    "64N-3Jo": "3 João",
    "65N-Jd": "Judas",
    "66N-Ap": "Apocalipse"
}

def get_available_books():
    """Retorna lista de livros disponíveis no diretório"""
    books = []
    if os.path.exists(BIBLE_PATH):
        for book_code, book_name in BIBLE_BOOKS.items():
            book_path = os.path.join(BIBLE_PATH, book_code)
            if os.path.exists(book_path):
                books.append((book_code, book_name))
    return books

def get_chapters(book_code):
    """Retorna lista de capítulos disponíveis para um livro"""
    chapters = []
    book_path = os.path.join(BIBLE_PATH, book_code)
    if os.path.exists(book_path):
        md_files = glob.glob(os.path.join(book_path, "*.md"))
        for file_path in sorted(md_files):
            filename = os.path.basename(file_path)
            chapter_num = filename.replace(".md", "")
            if chapter_num.isdigit() or chapter_num == "00":
                chapters.append(chapter_num)
    return sorted(chapters, key=lambda x: int(x) if x.isdigit() else 0)

def process_image_paths(content, book_code):
    """Processa o conteúdo Markdown para corrigir caminhos de imagens"""
    import re
    
    # Padrão para encontrar imagens no formato ![](../Images/...)
    image_pattern = r'!\[\]\(\.\./Images/([^)]+)\)'
    
    def replace_image_path(match):
        image_path = match.group(1)
        # Construir o caminho absoluto para a imagem
        full_image_path = os.path.join(BIBLE_PATH, "Images", image_path)
        
        # Verificar se a imagem existe
        if os.path.exists(full_image_path):
            # Retornar o caminho relativo correto para o Streamlit
            return f'<img src="data:image/jpeg;base64,{get_image_base64(full_image_path)}" style="max-width: 100%; height: auto; margin: 10px 0;">'
        else:
            return f'*[Imagem não encontrada: {image_path}]*'
    
    # Substituir todas as ocorrências
    processed_content = re.sub(image_pattern, replace_image_path, content)
    return processed_content

def get_image_base64(image_path):
    """Converte uma imagem para base64 para exibição no Streamlit"""
    import base64
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def read_chapter(book_code, chapter):
    """Lê o conteúdo de um capítulo específico"""
    file_path = os.path.join(BIBLE_PATH, book_code, f"{chapter}.md")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Processar caminhos de imagens
            content = process_image_paths(content, book_code)
            return content
    return None

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



# Interface principal
def main():
    st.title("📖 Bíblia Digital - João Ferreira de Almeida Corrigida Fiel 2007")
    st.markdown("---")
    
    # Sidebar para navegação
    st.sidebar.title("Navegação")
    
    # Seleção do livro
    available_books = get_available_books()
    if not available_books:
        st.error("Nenhum livro encontrado. Verifique se o diretório da Bíblia está correto.")
        return
    
    book_options = [f"{book_name}" for book_code, book_name in available_books]
    selected_book_name = st.sidebar.selectbox("Selecione o livro:", book_options)
    
    # Encontrar o código do livro selecionado
    selected_book_code = None
    for book_code, book_name in available_books:
        if book_name == selected_book_name:
            selected_book_code = book_code
            break
    
    if selected_book_code:
        # Seleção do capítulo
        chapters = get_chapters(selected_book_code)
        if chapters:
            chapter_options = [f"Capítulo {ch}" if ch != "00" else "Introdução" for ch in chapters]
            selected_chapter_display = st.sidebar.selectbox("Selecione o capítulo:", chapter_options)
            
            # Encontrar o número do capítulo
            selected_chapter = chapters[chapter_options.index(selected_chapter_display)]
            
            # Área principal de conteúdo
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.header(f"{selected_book_name} - {selected_chapter_display}")
                
                # Ler e exibir o conteúdo
                content = read_chapter(selected_book_code, selected_chapter)
                if content:
                    st.markdown(content, unsafe_allow_html=True)
                else:
                    st.error("Não foi possível carregar o conteúdo do capítulo.")
            
            with col2:
                st.subheader("Ferramentas")
                
                # Botão para tradução com OpenAI
                if st.button("🔍 Obter Versão Original"):
                    if content:
                        with st.spinner("Consultando versão original..."):
                            # Extrair apenas o texto bíblico (sem comentários)
                            lines = content.split('\n')
                            bible_text = []
                            for line in lines:
                                if line.startswith('**') and '**' in line[2:]:
                                    # Linha com versículo
                                    bible_text.append(line)
                            
                            if bible_text:
                                text_to_translate = '\n'.join(bible_text[:5])  # Primeiros 5 versículos
                                translation = get_hebrew_translation(text_to_translate)
                                
                                st.subheader("Versão Original e Tradução")
                                st.text_area("Resultado:", translation, height=300)
                            else:
                                st.warning("Não foi possível extrair texto bíblico para tradução.")
                
                # Informações adicionais
                st.markdown("---")
                st.markdown("**Sobre esta versão:**")
                st.markdown("João Ferreira de Almeida Corrigida Fiel 2007")
                st.markdown("Considerada uma das traduções mais fiéis ao texto original em português.")
        else:
            st.warning("Nenhum capítulo encontrado para este livro.")

if __name__ == "__main__":
    main()

