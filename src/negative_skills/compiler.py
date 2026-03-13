import anthropic
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def compile_skill(answers):
    print("\n⚙️  Compiling your negative skill...\n")

    # Build a prompt from the user's answers
    prompt = f"""
You are a skill compiler. Turn the user's frustrations into a valid SKILL.md file.

Context: {answers["context"]}

Things Claude did that annoyed them:
{chr(10).join(f"- {b}" for b in answers["bad_behaviors"])}

Topics Claude should never bring up:
{chr(10).join(f"- {t}" for t in answers["forbidden_topics"]) if answers["forbidden_topics"] else "- None specified"}

Style things they hate:
{answers["style_hates"] if answers["style_hates"] else "None specified"}

Strictness level: {answers["severity"]}

Output ONLY a valid SKILL.md file. Start with YAML frontmatter exactly like this:

---
name: [short-kebab-case-name]
description: [one sentence — when should Claude load this skill automatically]
---

Then write the full constraint instructions in markdown below the frontmatter.
Include sections for: Description, Context, Constraints (CRITICAL/WARNING/PREFERENCE), and Instructions for Claude.

No preamble. No explanation. Start with --- immediately.
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    skill_content = message.content[0].text
    return skill_content


def save_skill(skill_content, context):
    # Generate a filename from the context
    filename = context.lower().replace(" ", "-").replace("/", "-")[:30]
    filepath = f"output/{filename}-constraints.md"

    with open(filepath, "w") as f:
        f.write(skill_content)

    return filepath

def install_skill(skill_content, context):
    import re
    import platform

    # Find the skill name from frontmatter
    match = re.search(r'name:\s*(.+)', skill_content)
    skill_name = match.group(1).strip() if match else context.lower().replace(" ", "-")[:30]

    # Find the right skills folder for the OS
    if platform.system() == "Windows":
        base = os.path.expanduser("~\\.claude\\skills")
    else:
        base = os.path.expanduser("~/.claude/skills")

    skill_dir = os.path.join(base, skill_name)
    os.makedirs(skill_dir, exist_ok=True)

    filepath = os.path.join(skill_dir, "SKILL.md")
    with open(filepath, "w") as f:
        f.write(skill_content)

    return filepath


if __name__ == "__main__":
    # Test with dummy data
    test_answers = {
        "context": "coding help",
        "bad_behaviors": [
            "adds unnecessary comments to every line",
            "always suggests I use a library instead of writing the code myself",
            "gives me a 3 paragraph explanation when I just want the code"
        ],
        "forbidden_topics": ["suggesting I rewrite everything in Rust"],
        "style_hates": "bullet points, long disclaimers",
        "severity": "strict"
    }

    skill_content = compile_skill(test_answers)
    filepath = save_skill(skill_content, test_answers["context"])

    print(skill_content)
    print(f"\n✅ Saved to {filepath}")