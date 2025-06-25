# run_agent.py
from agents import Runner
from agent import beauty_blogger
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime

def save_to_html(content: str, base_filename="output"):
    html_body = content.replace('\n', '<br>')  # escape line breaks for HTML

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{base_filename}_{timestamp}.txt"

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI-Generated Blog Post</title>
</head>
<body>
    <article>
        {html_body}
    </article>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"✅ Blog post saved to: {filename}")


if __name__ == "__main__":
    result = Runner.run_sync(
        beauty_blogger,
        "Write a blog post about 2025 anti-aging skincare trends."
    )
    print(result.final_output)
    save_to_html(result.final_output)
