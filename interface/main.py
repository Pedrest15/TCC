import pandas as pd
import streamlit as st
from chat import MyChat

template="""
            Tarefa: Agrupamento Semântico de Emendas Parlamentares
            Você foi designado para realizar um agrupamento semântico das emendas parlamentares. Cada emenda é identificada por um texto descritivo.
            Todas as emendas são referentes ao mesmo projeto de lei, PL.

            Texto do PL:
            <context>
            {context}
            </context>

            Detalhes da Tarefa:
            Você receberá um conjunto de emendas parlamentares, cada uma representada por um texto descritivo. As emendas podem abordar uma variedade de tópicos.
            Seu modelo deve atribuir cada emenda a um grupo semântico com base em seus tópicos principais.
            Certifique-se de que cada emenda seja atribuída a um único grupo e que todas as emendas sejam atribuídas a um grupo.

            Exemplo de Emenda:
            AQUI SE INICIA A EMENDA ID 000001 TEXTO

            Texto das Emendas:
            {emendas}

            Question: {input}
        """

query = f"""Realize o agrupamento semântico das emendas parlamentares fornecidas, atribuindo cada emenda a um grupo com base em seus tópicos principais."""

def upload_emendas():
    st.markdown('<div align="left"><h5>Suba as emendas',unsafe_allow_html=True)
    #option = st.radio(
    #    label=".",
    #    key="visibility",
    #    options=["Arquivo csv contendo todas","Um arquivo txt para cada emendas"],
    #    label_visibility="collapsed"
    #)

    #if option == "Arquivo csv contendo todas":
    emendas_file = st.file_uploader("Escolha um arquivo",type='csv') 
    if emendas_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(emendas_file)
        #st.write(dataframe)

        return dataframe
    else:
        return None

    #elif option == "Um arquivo txt para cada emendas":
    #    emendas_files = st.file_uploader("Escolha um arquivo", type='txt',accept_multiple_files=True)
    #    if emendas_files is not None:
    #        for emendas_files in emendas_files:
    #            break

    #    return None

def upload_pl():
    st.markdown('<div align="left"><h5>Suba o Projeto de Lei',unsafe_allow_html=True)
    pl_file = st.file_uploader("Escolha um arquivo",type='pdf') 
    if pl_file is not None:
        # Save uploaded file to 'F:/tmp' folder.
        #save_path = Path(save_folder, File.name)
        with open(pl_file.name, mode='wb') as w:
            w.write(pl_file.getvalue())

            st.success(f'File {pl_file.name} is successfully saved!')
            
        return pl_file.name
    return None

@st.experimental_dialog("Erro")
def empty_files(df_emendas:pd.DataFrame,pl):
    if (df_emendas is None) and (pl is None):
        st.markdown('<div align="left"><h4>Faça o upload das emendas e do pl para poder realizar o agrupamento.',unsafe_allow_html=True)
    elif df_emendas is None:
        st.markdown('<div align="center"><h4>Faça o upload das emendas para poder realizar o agrupamento.',unsafe_allow_html=True)
    else:
        st.markdown('<div align="center"><h4>Faça o upload do pl para poder realizar o agrupamento.',unsafe_allow_html=True)

if  __name__ == '__main__':
    st.markdown('<div align="center"><h1>Agrupar Emendas',unsafe_allow_html=True)

    df_emendas = upload_emendas()
    pl = upload_pl()

    if st.button(label="Agrupar"):
        if (df_emendas is None) or (pl is None):
            empty_files(df_emendas,pl)
        else:
            emendas = "".join([f"AQUI SE INICIA A EMENDA ID {numero_emenda}:\n{text_proposto_emenda}\n" for numero_emenda, text_proposto_emenda in zip(df_emendas['NUMEROEMENDA'],df_emendas['TEXTOPROPOSTOEMENDA'])])
            
            chat = MyChat("mistral")
            chat.make_vector_store(pl)
            chat.make_chain(template)
            response = chat.ask(query,emendas)

            st.info(response)
