import json
from langchain_core.prompts import PromptTemplate
from prompts import extract_prompt, clean_prompt, classify_prompt, enhance_prompt, ats_prompt
from utils import json_to_text

# -------- MULTI LLM --------
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic


def get_llm(provider, api_key):

    if provider == "OpenAI":
        return ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)

    elif provider == "Gemini":
        return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

    elif provider == "Claude":
        return ChatAnthropic(model="claude-3-sonnet-20240229", anthropic_api_key=api_key)


# -------- SAFE JSON --------
def safe_json(content):
    try:
        return json.loads(content)
    except:
        return {}


def run_pipeline(resume_text, provider, api_key):

    llm = get_llm(provider, api_key)

    # STEP 1: EXTRACT
    res1 = (PromptTemplate.from_template(extract_prompt) | llm).invoke(
        {"resume_text": resume_text}
    )
    data = safe_json(res1.content)
    if not data:
        return {"error": "Extraction failed"}

    # STEP 2: CONVERT
    formatted = json_to_text(data)

    # STEP 3: CLEAN
    cleaned = (PromptTemplate.from_template(clean_prompt) | llm).invoke(
        {"resume_text": formatted}
    ).content

    # STEP 4: CLASSIFY
    res3 = (PromptTemplate.from_template(classify_prompt) | llm).invoke(
        {"resume_text": cleaned}
    )
    classification = safe_json(res3.content)

    # STEP 5: ENHANCE
    enhanced = (PromptTemplate.from_template(enhance_prompt) | llm).invoke(
        {"resume_text": cleaned}
    ).content

    # STEP 6: ATS
    res4 = (PromptTemplate.from_template(ats_prompt) | llm).invoke(
        {"resume_text": enhanced}
    )
    ats = safe_json(res4.content)

    return {
        "raw_json": data,
        "cleaned_resume": cleaned,
        "classification": classification,
        "enhanced_resume": enhanced,
        "ats": ats
    }