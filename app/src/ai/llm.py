"""Thin wrapper around the Gemini client used by the JioPulse assistant.

Google's Gemini API exposes an OpenAI-compatible endpoint, so we keep using
the ``openai`` SDK and just point it at Gemini's base URL. Keeps model names
and credential lookup in one place so the rest of the codebase never talks
to the SDK directly.
"""
import os
import streamlit as st

CHAT_MODEL = "gemini-2.0-flash"
EMBED_MODEL = "text-embedding-004"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def get_api_key():
    """Read the key from Streamlit secrets first, then the environment."""
    key = None
    try:
        key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        key = None
    return key or os.environ.get("GEMINI_API_KEY")


def ai_is_configured():
    """True when a Gemini key is available, so the UI can degrade gracefully."""
    return bool(get_api_key())


@st.cache_resource(show_spinner=False)
def get_client():
    from openai import OpenAI

    key = get_api_key()
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set.")
    return OpenAI(api_key=key, base_url=GEMINI_BASE_URL)


def chat(messages, tools=None, model=CHAT_MODEL, temperature=0.2):
    """Single chat completion. Passes tools through when provided."""
    client = get_client()
    kwargs = {"model": model, "messages": messages, "temperature": temperature}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    return client.chat.completions.create(**kwargs)


def embed(texts, model=EMBED_MODEL):
    """Return embedding vectors for a string or list of strings."""
    client = get_client()
    if isinstance(texts, str):
        texts = [texts]
    resp = client.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]
