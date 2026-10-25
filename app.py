import os
import urllib.parse
import requests
import streamlit as st

st.set_page_config(page_title="TK SAAB AI", page_icon="🌌", layout="wide")

st.markdown("""
<style>
.stApp {background:radial-gradient(circle at top,#121735 0%,#070a14 54%,#03040a 100%);color:#f3f5ff}
[data-testid="stSidebar"]{background:#080c18;border-right:1px solid #293258}
h1,h2,h3,p,label{color:#f3f5ff}
.hero{padding:24px;border:1px solid #303b70;border-radius:22px;background:linear-gradient(135deg,#111936,#090d19);margin-bottom:16px}
.hero h1{margin:0;font-size:2.2rem}.hero p{color:#aeb9e6;margin-bottom:0}
.stButton>button{background:linear-gradient(90deg,#4937ff,#8b35ef);color:white;border:0;border-radius:12px;font-weight:700}
.stTextArea textarea,.stTextInput input{background:#0b1020;color:#f3f5ff;border:1px solid #303b70}
[data-testid="stChatMessage"]{background:#0b1020;border:1px solid #202a4b;border-radius:14px}
</style>
""", unsafe_allow_html=True)

def get_key():
    try:
        return st.secrets.get("OPENROUTER_API_KEY", "")
    except Exception:
        return os.getenv("OPENROUTER_API_KEY", "")

def ask_ai(messages, max_tokens=1000):
    key = get_key()
    if not key:
        st.error("AI chat ke liye API key set nahi hai. README mein diye gaye Streamlit Secrets steps follow karo.")
        return None
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json",
                     "X-Title":"TK SAAB AI"},
            json={"model":"openrouter/free","messages":messages,"max_tokens":max_tokens},
            timeout=60
        )
        if r.status_code != 200:
            st.error(f"AI service error ({r.status_code}). Free model unavailable ho sakta hai ya key check karo.")
            return None
        return r.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        st.error("Request time out ho gayi. Dobara try karo.")
    except Exception:
        st.error("Internet/API connection error. Dobara try karo.")
    return None

with st.sidebar:
    st.markdown("## 🌌 TK SAAB AI")
    st.caption("Your personal AI workspace")
    page = st.radio("Menu", ["AI Chat", "Image Generator", "Code Generator", "Text Summarizer", "About"])
    st.divider()
    st.caption("Free services may have limits or downtime.")

st.markdown("""
<div class="hero">
<h1>🌌 TK SAAB AI</h1>
<p>AI Chat • Image Generator • Code Helper — dark mode assistant</p>
</div>
""", unsafe_allow_html=True)

if page == "AI Chat":
    st.subheader("💬 AI Chat")
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role":"system","content":"You are TK SAAB AI, a helpful assistant. Answer safely and clearly. If the user writes in Roman Urdu, reply in simple Roman Urdu."}
        ]
    for m in st.session_state.chat_messages:
        if m["role"] != "system":
            with st.chat_message("user" if m["role"]=="user" else "assistant"):
                st.markdown(m["content"])
    prompt = st.chat_input("Apna sawal likho...")
    if prompt:
        st.session_state.chat_messages.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("AI soch raha hai..."):
                answer = ask_ai(st.session_state.chat_messages)
                if answer:
                    st.markdown(answer)
                    st.session_state.chat_messages.append({"role":"assistant","content":answer})
    if st.button("🗑️ New chat"):
        st.session_state.chat_messages = [{"role":"system","content":"You are TK SAAB AI, a helpful assistant. Answer safely and clearly. If the user writes in Roman Urdu, reply in simple Roman Urdu."}]
        st.rerun()

elif page == "Image Generator":
    st.subheader("🎨 AI Image Generator")
    st.write("Apni image ka description English mein likho. Misal: cinematic blue Pakistani bus on a mountain road, realistic lighting.")
    prompt = st.text_area("Image prompt", height=120, placeholder="Describe the image you want...")
    style = st.selectbox("Style", ["Realistic", "3D cartoon", "Anime", "Digital art", "Cinematic"])
    if st.button("Generate image"):
        if not prompt.strip():
            st.warning("Pehle image ka description likho.")
        else:
            full_prompt = f"{prompt.strip()}, {style} style, high quality"
            encoded = urllib.parse.quote(full_prompt, safe="")
            image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
            with st.spinner("Image service se image mangwai ja rahi hai..."):
                try:
                    response = requests.get(image_url, timeout=120)
                    content_type = response.headers.get("content-type", "")
                    if response.status_code == 200 and "image" in content_type:
                        st.image(response.content, caption="Generated with an external image service", use_container_width=True)
                        st.download_button("Download image", data=response.content, file_name="tk-saab-ai-image.png", mime=content_type)
                    else:
                        st.error("Free image service abhi available nahi. Kuch der baad try karo; free service ki uptime guaranteed nahi.")
                except Exception:
                    st.error("Image generate nahi ho saki. Service unavailable ya slow ho sakti hai.")
            st.caption("Privacy note: image prompt third-party image service ko bheja jata hai. Sensitive/private details mat likho.")

elif page == "Code Generator":
    st.subheader("💻 AI Code Generator")
    language = st.selectbox("Programming language", ["HTML/CSS/JavaScript", "Python", "JavaScript", "Java", "C++", "Other"])
    task = st.text_area("Kya banana hai?", height=150, placeholder="Misal: simple calculator banao, comments ke sath samjhao")
    level = st.selectbox("Explanation", ["Beginner-friendly", "Code only", "Detailed explanation"])
    if st.button("Generate code"):
        if not task.strip():
            st.warning("Pehle apna task likho.")
        else:
            system = "You are a careful coding assistant. Provide runnable examples, explain assumptions, and never claim code was executed if it was not."
            user = f"Language: {language}\nExplanation style: {level}\nTask: {task}"
            with st.spinner("Code likha ja raha hai..."):
                answer = ask_ai([{"role":"system","content":system},{"role":"user","content":user}], max_tokens=1600)
            if answer:
                st.markdown(answer)
                st.download_button("Download response as TXT", data=answer, file_name="tk-saab-code.txt", mime="text/plain")

elif page == "Text Summarizer":
    st.subheader("📝 Text Summarizer")
    text_in = st.text_area("Text paste karo", height=220)
    style = st.selectbox("Summary style", ["Short bullet points", "Simple Roman Urdu", "Detailed"])
    if st.button("Summarize"):
        if text_in.strip():
            answer = ask_ai([{"role":"system","content":"Summarize faithfully without inventing details."},
                             {"role":"user","content":f"Summarize in this style: {style}\n\n{text_in}"}])
            if answer: st.markdown(answer)
        else:
            st.warning("Pehle text paste karo.")

else:
    st.subheader("About TK SAAB AI")
    st.write("Aapki apni AI website ka starter project.")
    st.markdown("""
**Features**
- AI chat
- AI image generation through an external free service
- Code generator
- Text summarizer

**Important:** Text AI needs an OpenRouter API key. Image generation uses a third-party service whose free access, limits, and availability may change. This starter is not unlimited and does not guarantee earnings.
""")
