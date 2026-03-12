import click

def run_interview():
    print("\n🧠 Negative Skills Builder")
    print("=" * 40)
    print("Answer a few questions and I'll build a skill that stops Claude from doing things you hate.\n")

    answers = {}

    # Q1 - Context
    answers["context"] = click.prompt(
        "1. What is this skill for? (e.g. coding help, writing emails, customer support)"
    )

    # Q2 - Bad behaviors
    print("\n2. What has Claude done that annoyed or frustrated you?")
    print("   (Type each one and press Enter. Type 'done' when finished)\n")
    bad_behaviors = []
    while True:
        behavior = input("   > ").strip()
        if behavior.lower() == "done":
            break
        if behavior:
            bad_behaviors.append(behavior)
    answers["bad_behaviors"] = bad_behaviors

    # Q3 - Forbidden topics
    print("\n3. Are there any topics Claude should never bring up?")
    print("   (Type each one and press Enter. Type 'done' when finished)\n")
    forbidden_topics = []
    while True:
        topic = input("   > ").strip()
        if topic.lower() == "done":
            break
        if topic:
            forbidden_topics.append(topic)
    answers["forbidden_topics"] = forbidden_topics

    # Q4 - Style
    answers["style_hates"] = click.prompt(
        "\n4. Any style things you hate? (e.g. bullet points, long disclaimers, formal tone) — or press Enter to skip",
        default=""
    )

    # Q5 - Severity
    answers["severity"] = click.prompt(
        "\n5. How strict should these rules be?",
        type=click.Choice(["strict", "moderate", "soft"]),
        default="moderate"
    )

    return answers


if __name__ == "__main__":
    answers = run_interview()
    print("\n--- Your answers ---")
    print(answers)