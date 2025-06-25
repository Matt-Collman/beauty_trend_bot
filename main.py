from trend_sources import get_reddit_beauty_trends
from blog_writer import write_blog_post
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load your OpenAI key from .env
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

import re

def safe_filename(title):
    # Replace all invalid characters with hyphens
    return re.sub(r'[\\/*?:"<>|]', '-', title).strip()

# === History Helpers ===
def has_been_written(topic, history_file="written_topics.txt"):
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            past_topics = [line.strip() for line in f.readlines()]
        return topic in past_topics
    except FileNotFoundError:
        return False

def save_written_topic(topic, history_file="written_topics.txt"):
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(f"{topic}\n")

# === GPT Topic Selector ===
from difflib import get_close_matches

def select_best_topic(topics):
    fresh_topics = [t for t in topics if not has_been_written(t)]
    if not fresh_topics:
        print("❌ All topics have already been written about.")
        return None

    print("\nAsking GPT to select the best topic from:")
    for i, t in enumerate(fresh_topics, 1):
        print(f"{i}. {t}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful beauty content strategist. Respond ONLY with the exact title of the best blog topic from the list."
                },
                {
                    "role": "user",
                    "content": f"Choose the best blog topic from this list: {fresh_topics}"
                }
            ],
            temperature=0.7
        )
        raw_reply = response.choices[0].message.content.strip().strip('"')
        print(f"\n🤖 GPT replied: {raw_reply}")

        # Find the closest actual topic
        closest = get_close_matches(raw_reply, fresh_topics, n=1, cutoff=0.5)
        if closest:
            selected = closest[0]
            print(f"✅ Matched topic: {selected}")
            return selected
        else:
            print("⚠️ Could not match GPT reply to a known topic. Falling back.")
            return fresh_topics[0]

    except Exception as e:
        print(f"❌ GPT failed to select a topic: {e}")
        return fresh_topics[0]

# === Main Program ===
if __name__ == "__main__":
    print("🔎 Fetching trending topics...")
    topics = get_reddit_beauty_trends()

    if not topics:
        print("❌ No topics found.")
        exit()

    selected = select_best_topic(topics)

    if selected:
        print(f"\n📝 Writing blog post about: '{selected}'")
        write_blog_post(selected)
        save_written_topic(selected)
    else:
        print("🚫 No new topics available.")
