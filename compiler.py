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
You are a skill compiler. Your job is to take a user's frustrations with Claude and turn them into a structured negative skill file.

Here is what the user told you:

Context: {answers["context"]}

Things Claude did that annoyed them:
{chr(10).join(f"- {b}" for b in answers["bad_behaviors"])}

Topics Claude should never bring up:
{chr(10).join(f"- {t}" for t in answers["forbidden_topics"]) if answers["forbidden_topics"] else "- None specified"}

Style things they hate:
{answers["style_hates"] if answers["style_hates"] else "None specified"}

Strictness level: {answers["severity"]}

Your job:
1. Analyze these frustrations and identify the core constraints
2. Write a SKILL.md file that encodes these as negative constraints
3. Make the instructions clear and specific so Claude actually follows them
4. Add a short description explaining what this skill does

Return ONLY the raw markdown content for the SKILL.md file. No explanation, no preamble. Start directly with the markdown.

Use this structure:

# [Skill Name]

## Description
[What this skill does in one sentence]

## Context
[When this skill applies]

## Constraints
[List each constraint clearly, with severity: CRITICAL / WARNING / PREFERENCE]

## Instructions for Claude
[Clear behavioral instructions Claude must follow]
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