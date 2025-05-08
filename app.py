import streamlit as st
import openai
import os
from datetime import datetime
from dotenv import load_dotenv
from service.utils import guardar_todas_conversaciones, cargar_contexto, cargar_todas_conversaciones, procesar_documento

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar la clave de la API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración de la API de OpenAI
st.set_page_config(page_title="Chat Local con OpenAI", page_icon="🤖")
st.title("🧠 ChatGPT Local con OpenAI API")


# Cargar todas las conversaciones
todas_conversaciones = cargar_todas_conversaciones()

# Inicializar el estado de la conversación seleccionada
if "conversacion_seleccionada" not in st.session_state:
    st.session_state.conversacion_seleccionada = "Nueva conversación"

# Inicializar el estado del documento procesado
if "documento_procesado" not in st.session_state:
    st.session_state.documento_procesado = None  # Almacena el contenido del documento cargado

# Panel lateral para seleccionar o crear una conversación
st.sidebar.title("Historial de conversaciones")
opciones = ["Nueva conversación"] + list(todas_conversaciones.keys())

# Determinar el índice de la conversación seleccionada
if st.session_state.conversacion_seleccionada in todas_conversaciones:
    indice_seleccionado = opciones.index(st.session_state.conversacion_seleccionada)
else:
    indice_seleccionado = 0  # Por defecto, "Nueva conversación"

conversacion_seleccionada = st.sidebar.selectbox(
    "Selecciona una conversación",
    options=opciones,
    index=indice_seleccionado
)

CONTEXT = cargar_contexto()

# Si se selecciona "Nueva conversación", crear un nuevo ID
if conversacion_seleccionada == "Nueva conversación":
    nueva_conversacion_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Generar un ID único
    todas_conversaciones[nueva_conversacion_id] = [{"role": "system", "content": CONTEXT}]
    guardar_todas_conversaciones(todas_conversaciones)
    st.session_state.conversacion_seleccionada = nueva_conversacion_id
    st.session_state.messages = [{"role": "system", "content": CONTEXT}]
    st.session_state.documento_procesado = None  # Reiniciar el estado del documento procesado
    st.rerun()

# Actualizar la conversación seleccionada en el estado
st.session_state.conversacion_seleccionada = conversacion_seleccionada

# Cargar la conversación seleccionada
st.session_state.messages = todas_conversaciones.get(
    st.session_state.conversacion_seleccionada,
    [{"role": "system", "content": CONTEXT}]
)

# Subir un documento
st.sidebar.title("Análisis de documentos")
archivo = st.sidebar.file_uploader("Sube un archivo PDF o Word", type=["pdf", "docx", "xlsx", "xls", "csv", "png", "jpg", "jpeg", "txt", "py", "java"])

if archivo:
    texto_documento = procesar_documento(archivo)
    if texto_documento:
        st.session_state.documento_procesado = texto_documento
        st.success("El documento ha sido procesado. Puedes añadirlo al contexto si lo deseas.")

# Botón para añadir el documento al contexto
if st.session_state.documento_procesado:
    if st.sidebar.button("Añadir documento al contexto"):
        st.session_state.messages.append({
            "role": "system",
            "content": f"Contexto del documento:\n{st.session_state.documento_procesado}"
        })
        # Guardar el historial actualizado en la conversación actual
        todas_conversaciones[st.session_state.conversacion_seleccionada] = st.session_state.messages
        guardar_todas_conversaciones(todas_conversaciones)
        st.success("El contenido del documento ha sido añadido al contexto.")

# Mostrar historial de la conversación seleccionada
for msg in st.session_state.messages[1:]:
    if "image_url" in msg:  # Si el mensaje contiene una URL de imagen
        st.image(msg["image_url"], caption="Imagen generada", use_column_width=True)
    elif "content" in msg:  # Si el mensaje contiene texto
        st.chat_message(msg["role"]).markdown(msg["content"])

# Entrada del usuario
prompt = st.chat_input("Escribe tu mensaje. Si deseas generar una imagen, escribe 'imagen:' seguido de la descripción.")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if prompt.lower().startswith("imagen:"):
        descripcion_imagen = prompt[len("imagen:"):].strip()
        with st.spinner("Generando imagen..."):
            try:
                response = openai.Image.create(
                    prompt=descripcion_imagen,
                    n=1,
                    size="512x512"
                )
                imagen_url = response["data"][0]["url"]
                st.image(imagen_url, caption="Imagen generada", use_column_width=True)
                st.session_state.messages.append({"role": "assistant", "image_url": imagen_url})
            except Exception as e:
                st.error(f"❌ Error al generar la imagen: {str(e)}")
    else:
        
        with st.spinner("Pensando..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    temperature=0.0,
                    max_tokens=500
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"❌ Error: {str(e)}"

        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Guardar la conversación actualizada
    todas_conversaciones[st.session_state.conversacion_seleccionada] = st.session_state.messages
    guardar_todas_conversaciones(todas_conversaciones)

# Botón para reiniciar conversación
if st.sidebar.button("🗑️ Borrar conversación"):
    if st.session_state.conversacion_seleccionada in todas_conversaciones:
        del todas_conversaciones[st.session_state.conversacion_seleccionada]
        guardar_todas_conversaciones(todas_conversaciones)
        st.session_state.conversacion_seleccionada = "Nueva conversación"
        st.rerun()
