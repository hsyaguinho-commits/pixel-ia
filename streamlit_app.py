import streamlit as st
import requests

NOME_IA = "Pixel"
MODELO = "qwen3:1.7b"

st.set_page_config(page_title=NOME_IA, page_icon="🤖", layout="wide")

st.markdown("""
<style>
.block-container{padding-top:1.2rem;padding-bottom:1rem;max-width:1400px;}
[data-testid="stSidebar"]{background:#f4f8ff;border-right:1px solid #dce7f7;}
.hero{display:flex;gap:28px;align-items:center;padding:18px 10px 10px 10px;}
.hero img{width:290px;max-width:35vw;border-radius:24px;box-shadow:0 8px 28px rgba(15,45,90,.10)}
.hero h1{font-size:3.2rem;margin:0;color:#0d2b57}.hero h1 span{color:#1976e9}
.hero h3{margin:.2rem 0 1rem;color:#5d6f8c;font-weight:500}.hero p{font-size:1.15rem;color:#243b5a;line-height:1.6}
.quick-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px}
.quick{background:#fff;border:1px solid #dfe8f5;border-radius:18px;padding:18px;text-align:center;box-shadow:0 4px 12px rgba(15,45,90,.06)}
.quick b{display:block;margin-top:6px;color:#16355e}.quick .ico{font-size:2rem}
.chatbox{background:#fff;border:1px solid #dfe8f5;border-radius:22px;padding:18px;box-shadow:0 10px 30px rgba(15,45,90,.07);margin-top:24px}
.small-note{text-align:center;color:#8b97aa;font-size:.85rem;margin-top:10px}
.footer-note{text-align:center;color:#6f7f96;font-size:.9rem;margin-top:12px}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 💬 Pixel")
    st.caption("SEMPRE AO SEU LADO")
    st.divider()
    menu = st.radio("", ["💬 Chat", "📚 Base de Conhecimento", "▶️ Tutoriais", "🎫 Abrir Chamado", "📢 Novidades", "ℹ️ Sobre a Pixel"])
    st.divider()
    st.markdown("**Precisa de um humano?**")
    st.button("👤 Falar com o time de TI", use_container_width=True)
    st.write("")
    st.markdown("### Pixel")
    st.caption("Mais que tecnologia. Soluções para o seu dia a dia.")

if menu == "💬 Chat":
    col1, col2 = st.columns([1, 2.2])
    with col1:
        try:
            st.image("pixel_seu_assistente_de_ti.png", use_container_width=True)
        except Exception:
            st.markdown("### 🤖 Pixel")
    with col2:
        st.markdown("# Olá! Eu sou o <span style='color:#1976e9'>Pixel</span>", unsafe_allow_html=True)
        st.markdown("### Seu assistente virtual de suporte de TI")
        st.write("Estou aqui para ajudar com suas dúvidas, solucionar problemas e tornar o seu dia a dia mais fácil. **Pode perguntar!**")
        st.markdown("""
        <div class='quick-grid'>
          <div class='quick'><div class='ico'>🪟</div><b>Problemas no Windows</b></div>
          <div class='quick'><div class='ico'>🖨️</div><b>Impressoras</b></div>
          <div class='quick'><div class='ico'>✉️</div><b>Outlook</b></div>
          <div class='quick'><div class='ico'>👥</div><b>Teams</b></div>
          <div class='quick'><div class='ico'>🌐</div><b>Internet / VPN</b></div>
          <div class='quick'><div class='ico'>🔐</div><b>Acessos e Senhas</b></div>
          <div class='quick'><div class='ico'>⚙️</div><b>Sistemas</b></div>
          <div class='quick'><div class='ico'>💡</div><b>Dicas e Tutoriais</b></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='chatbox'>", unsafe_allow_html=True)

    if "mensagens" not in st.session_state:
        st.session_state.mensagens = [
            {"role":"assistant","content":"Olá! 👋 Sou o Pixel, seu assistente de suporte de TI. Como posso ajudar hoje?"}
        ]

    for m in st.session_state.mensagens:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    pergunta = st.chat_input("Digite sua dúvida aqui...")

    if pergunta:
        st.session_state.mensagens.append({"role":"user","content":pergunta})
        with st.chat_message("user"):
            st.write(pergunta)

        mensagens_ollama = [
            {
                "role":"system",
                "content":(
                    "Você é Pixel, um assistente virtual masculino de suporte de TI. "
                    "Responda sempre em português do Brasil. "
                    "Seja claro, direto, educado e útil. "
                    "Não mostre raciocínio interno. Dê somente a resposta final. /no_think"
                )
            }
        ] + st.session_state.mensagens

        try:
            with st.spinner("Pensando..."):
                r = requests.post(
                    "http://localhost:11434/api/chat",
                    json={"model":MODELO,"messages":mensagens_ollama,"stream":False,"think":False},
                    timeout=300
                )
            r.raise_for_status()
            texto = r.json()["message"]["content"]
        except Exception as erro:
            texto = f"Não consegui acessar o Ollama. Erro: {erro}"

        st.session_state.mensagens.append({"role":"assistant","content":texto})
        with st.chat_message("assistant"):
            st.write(texto)

    st.markdown("<div class='small-note'>O Pixel pode cometer erros. Em dúvidas críticas, confirme com o time de TI.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer-note'>🔒 Seguro &nbsp;&nbsp; 👥 Confiável &nbsp;&nbsp; 📈 Sempre evoluindo</div>", unsafe_allow_html=True)

elif menu == "📚 Base de Conhecimento":
    st.title("📚 Base de Conhecimento")
    st.info("Aqui você poderá adicionar procedimentos, manuais e conteúdos para o Pixel consultar.")
elif menu == "▶️ Tutoriais":
    st.title("▶️ Tutoriais")
    st.info("Área para tutoriais de suporte e vídeos.")
elif menu == "🎫 Abrir Chamado":
    st.title("🎫 Abrir Chamado")
    st.info("Aqui você poderá integrar um formulário de abertura de chamados.")
elif menu == "📢 Novidades":
    st.title("📢 Novidades")
    st.info("Área para avisos e atualizações de TI.")
else:
    st.title("ℹ️ Sobre a Pixel")
    st.write("Pixel é um assistente virtual de suporte de TI.")
