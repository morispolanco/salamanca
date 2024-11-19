import streamlit as st
import os
from pathlib import Path
import requests
import json
from typing import List, Dict

# Configuración de la página
st.set_page_config(
    page_title="Escuela de Salamanca Q&A",
    page_icon="📚",
    layout="wide"
)

# Configuración del estilo
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        padding: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Clase para manejar los documentos
class DocumentLoader:
    def __init__(self, docs_folder: str = "documentos"):
        self.docs_folder = docs_folder
        self.documents = {}
        
    def load_documents(self) -> Dict[str, str]:
        """Carga todos los documentos TXT del directorio especificado."""
        if not os.path.exists(self.docs_folder):
            os.makedirs(self.docs_folder)
            
        for file_path in Path(self.docs_folder).glob("*.txt"):
            with open(file_path, 'r', encoding='utf-8') as file:
                self.documents[file_path.stem] = file.read()
        
        return self.documents

# Clase para manejar la API de X
class XAIClient:
    def __init__(self):
        self.api_key = st.secrets["X_API_KEY"]
        self.base_url = "https://api.x.ai/v1/chat/completions"
        
    def get_response(self, question: str, context: str) -> str:
        """Obtiene respuesta de la API de X."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        prompt = f"""Basándote en el siguiente contexto, responde la pregunta. Si la respuesta no se encuentra en el contexto, indica que no tienes suficiente información para responder.

Contexto: {context}

Pregunta: {question}"""
        
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un experto en la Escuela de Salamanca y sus autores. Responde de manera precisa y académica."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "grok-beta",
            "stream": False,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error al obtener respuesta: {str(e)}"

# Función principal de la aplicación
def main():
    st.title("📚 Consultas sobre la Escuela de Salamanca")
    
    # Inicializar clases
    doc_loader = DocumentLoader()
    x_client = XAIClient()
    
    # Sección para cargar documentos
    st.header("Documentos Cargados")
    documents = doc_loader.load_documents()
    
    if not documents:
        st.warning("No hay documentos cargados. Por favor, añade archivos TXT en la carpeta 'documentos'.")
    else:
        st.success(f"Documentos cargados: {', '.join(documents.keys())}")
    
    # Sección de chat
    st.header("Realiza tu consulta")
    
    # Inicializar historial de chat si no existe
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Campo de entrada para la pregunta
    if question := st.chat_input("Escribe tu pregunta aquí..."):
        # Añadir pregunta al historial
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Mostrar pregunta
        with st.chat_message("user"):
            st.markdown(question)
        
        # Preparar el contexto combinando todos los documentos
        context = "\n\n".join(documents.values())
        
        # Obtener respuesta
        with st.chat_message("assistant"):
            with st.spinner("Buscando respuesta..."):
                response = x_client.get_response(question, context)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
