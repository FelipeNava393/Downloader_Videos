import streamlit as st
import os
from yt_dlp import YoutubeDL

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Download de Links",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="expanded"
)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🎬 Downloader de Vídeos")

    st.markdown("""
    **O que é?**  
    Esta aplicação permite colar um link de vídeo
    e obter o arquivo em **MP4**, de forma simples
    e direta.
    """)

    st.divider()

    st.subheader("🔗 Cole o link do vídeo")
    video_link = st.text_input(
        label="Link",
        placeholder="https://exemplo.com/video"
    )

    quality = st.selectbox(
        "🎚️ Qualidade",
        ["Melhor disponível", "720p", "480p"]
    )

    download_btn = st.button("⬇️ Preparar download")

    st.divider()

    st.subheader("❓ Dúvidas rápidas")

    with st.expander("Quais sites funcionam?"):
        st.write(
            "Funciona melhor com vídeos públicos e sem DRM. "
            "Algumas plataformas podem não permitir download."
        )

    with st.expander("O vídeo vem em qual formato?"):
        st.write("O arquivo retornado será em **MP4**.")

    with st.expander("Existe limite de tamanho?"):
        st.write(
            "Sim. Para garantir desempenho, vídeos muito grandes "
            "podem ser bloqueados."
        )

# ---------------- MAIN ----------------
st.title("📥 Painel de Download")

if download_btn:
    if not video_link or not video_link.startswith("http"):
        st.warning("⚠️ Insira um link válido.")
    else:
        status = st.status("⏳ Preparando download...", expanded=True)

        output_path = os.path.join(DOWNLOAD_DIR, "video.mp4")

        if quality == "720p":
            format_opt = "best[ext=mp4][height<=720]"
        elif quality == "480p":
            format_opt = "best[ext=mp4][height<=480]"
        else:
            format_opt = "best[ext=mp4]"

        try:
            status.write("📡 Baixando vídeo...")

            ydl_opts = {
                "format": format_opt,
                "outtmpl": output_path,
                "quiet": True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])

            status.write("✅ Download concluído!")
            status.update(label="Pronto para baixar 🎉", state="complete")

            with open(output_path, "rb") as file:
                st.download_button(
                    label="⬇️ Baixar MP4",
                    data=file,
                    file_name="video.mp4",
                    mime="video/mp4"
                )

        except Exception as e:
            status.update(
                label="❌ Erro ao baixar o vídeo",
                state="error"
            )
            st.error("Não foi possível processar o vídeo.")
            st.exception(e)

else:
    st.info("⬅️ Use a barra lateral para inserir um link.")
