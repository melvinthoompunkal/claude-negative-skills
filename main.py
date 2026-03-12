import os
from dotenv import load_dotenv
from interviewer import run_interview
from compiler import compile_skill, save_skill

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
    print(f"\n📁 Saved to: {filepath}")
    print("\nNext step: drop this file into your Claude skills folder and it will start working immediately.")

if __name__ == "__main__":
    main()