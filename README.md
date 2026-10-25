# TK SAAB AI — Full starter project

Android-friendly Streamlit website starter with:
- AI Chat (OpenRouter free model router)
- Image Generator (external free image endpoint; may be rate-limited or unavailable)
- Code Generator
- Text Summarizer

## Step A — Upload to GitHub from Android
1. Download and extract this ZIP on your phone.
2. Go to https://github.com and sign in.
3. Create a new repository named `tk-saab-ai`.
4. Upload `app.py`, `requirements.txt`, and `README.md`. You may also upload `.streamlit/config.toml`.
5. Do not upload API keys, private chat logs, passwords, or personal data.

## Step B — Set up text AI
1. Open https://openrouter.ai/ and create an account.
2. Create an API key and keep it private.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Create an app using repository `tk-saab-ai`, branch `main`, main file `app.py`.
5. Open Advanced settings → Secrets and add:
   OPENROUTER_API_KEY = "YOUR_PRIVATE_KEY"
6. Deploy.

## Step C — Test
Open your new `streamlit.app` link. Test chat, code generator, summarizer and image generator separately.

## Zero-budget limitations
- Free AI models have request limits and availability can change.
- The image generator uses a third-party endpoint without a guaranteed service level. If it stops working, you may need to replace it with another provider.
- Do not expose your API key in GitHub or frontend code.
- Public sites can attract abuse; don't advertise it as unlimited.
- This is a starter, not a guarantee of monetization or income.
