import os
from dotenv import load_dotenv
from negative_skills.interviewer import run_interview
from negative_skills.compiler import compile_skill, save_skill, install_skill

load_dotenv()

def main():
    print("\n🚫 Negative Skills CLI")
    print("Turn your Claude frustrations into an installable skill.\n")

    # Step 1: Interview the user
    answers = run_interview()

    # Step 2: Compile into a SKILL.md
    skill_content = compile_skill(answers)

    # Step 3: Save it
    filepath = save_skill(skill_content, answers["context"])

   # Step 4: Show the result
    print("\n" + "=" * 40)
    print("✅ Your negative skill is ready!\n")
    print(skill_content)
    print("=" * 40)

    # Save to output folder
    filepath = save_skill(skill_content, answers["context"])
    print(f"\n📁 Saved to: {filepath}")

    # Offer to install directly into Claude Code
    install = input("\n⚡ Install directly into Claude Code? (y/n): ").strip().lower()
    if install == "y":
        from negative_skills.compiler import install_skill
        installed_path = install_skill(skill_content, answers["context"])
        print(f"\n🚀 Installed to: {installed_path}")
        print("Restart Claude Code and your skill will be active immediately.")
    else:
        print("\nTo install manually, copy the file to ~/.claude/skills/[skill-name]/SKILL.md")

if __name__ == "__main__":
    main()