import streamlit as st

# Función para cargar el texto de la obra desde una cadena
@st.cache_data
def cargar_obra():
    # Este es un ejemplo de cómo podrías almacenar el texto. 
    # Puedes reemplazar este contenido con el texto completo de la obra.
    texto_obra = """
    [Aquí va el contenido completo de la obra 'Suma de Tratos y Contratos' de Tomás de Mercado]
    """
    return texto_obra

# Función para buscar citas relevantes en la obra
def buscar_citas(texto_obra, pregunta):
    # Convertir todo el texto a minúsculas para facilitar la búsqueda
    texto_obra = texto_obra.lower()
    pregunta = pregunta.lower()
    
    # Dividir el texto en párrafos o secciones para buscar citas
    parrafos = texto_obra.split('\n')
    
    # Buscar coincidencias en los párrafos
    resultados = []
    for parrafo in parrafos:
        if pregunta in parrafo:
            resultados.append(parrafo)
    
    # Si no hay coincidencias, devolver un mensaje genérico
    if len(resultados) == 0:
        return "No se encontraron citas relevantes para tu consulta."
    else:
        return "\n\n".join(resultados[:5])  # Limitar a las 5 primeras coincidencias

# Título de la app
st.title("Experto en el Pensamiento de Tomás de Mercado")

# Introducción a la app
st.write("""
Bienvenido a la app de consulta sobre el pensamiento de Tomás de Mercado. Aquí podrás realizar preguntas relacionadas con su obra *Suma de Tratos y Contratos*, y te proporcionaré citas relevantes de la obra.
""")

# Cargar la obra precargada en la aplicación
texto_obra = cargar_obra()

# Pregunta del usuario
pregunta = st.text_input("Escribe tu pregunta sobre Tomás de Mercado:")

# Botón para realizar la consulta
if st.button("Consultar"):
    if pregunta:
        # Buscar las citas relevantes en la obra
        citas = buscar_citas(texto_obra, pregunta)
        st.write("Citas relevantes encontradas:")
        st.write(citas)
    else:
        st.write("Por favor, escribe una pregunta.")
