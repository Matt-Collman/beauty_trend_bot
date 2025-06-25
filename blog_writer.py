import os
import re
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Utility to make filenames safe ===
def safe_filename(title):
    return re.sub(r'[\\/*?:"<>|]', '-', title).strip()

# === Write Blog Post ===
def write_blog_post(title):
    messages = [
        {
            "role": "system",
            "content": "You are a professional beauty blogger targeting affluent, style-conscious readers. Write a refined, informative blog post about the given topic. Include tips, product mentions, and appeal to readers interested in modern beauty trends."
        },
        {
            "role": "user",
            "content": f"Please write a blog post about: {title}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    blog_content = response.choices[0].message.content.strip()

    claims = extract_factual_claims(blog_content)
    fact_checks = [fact_check_claim(c) for c in claims if c.strip()]
    final_blog = append_fact_check_summary(blog_content, fact_checks)

    # Sanitize filename
    safe_title = safe_filename(title)
    date = datetime.now().strftime("%Y-%m-%d_%H-%M")

    txt_filename = f"{safe_title}_{date}.txt"
    html_filename = f"{safe_title}_{date}.html"

    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(final_blog)
    print(f"📝 Saved blog post as {txt_filename}")

    with open(html_filename, "w", encoding="utf-8") as f:
        html_content = final_blog.replace("\n", "<br>")
        f.write(f"<html><body><h1>{title}</h1><p>{html_content}</p></body></html>")

    print(f"🌐 Saved HTML version as {html_filename}")

# === Factual Claim Extraction ===
def extract_factual_claims(text):
    messages = [
        {
            "role": "system",
            "content": "Extract a list of factual claims from the text for fact-checking. List each one on a new line."
        },
        {
            "role": "user",
            "content": text
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content.strip().split('\n')

# === Dummy Fact Check Placeholder ===
def fact_check_claim(claim):
    # In a real implementation, you would call a fact-checking API or use search
    return f"Claim: {claim} – Verified ✅"

# === Append Fact-Check Section ===
def append_fact_check_summary(content, checks):
    summary = "\n\n---\n\n🔎 Fact-Check Summary:\n" + "\n".join(checks)
    return content + summary
