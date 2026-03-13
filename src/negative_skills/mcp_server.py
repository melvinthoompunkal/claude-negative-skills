import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from negative_skills.compiler import compile_skill, save_skill, install_skill

app = Server("negative-skills")

@app.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="generate_negative_skill",
            description="Interview the user about Claude frustrations and generate a SKILL.md constraint file that stops Claude from doing annoying things.",
            inputSchema={
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "What is this skill for? e.g. 'coding help', 'writing emails'"
                    },
                    "bad_behaviors": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of things Claude has done that annoyed the user"
                    },
                    "forbidden_topics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Topics Claude should never bring up"
                    },
                    "style_hates": {
                        "type": "string",
                        "description": "Style things the user hate, e.g. 'bullet points, long disclaimers'"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["strict", "moderate", "soft"],
                        "description": "How strict the rules should be"
                    },
                    "auto_install": {
                        "type": "boolean",
                        "description": "Whether to automatically install the skill into Claude Code's skills folder"
                    }
                },
                "required": ["context", "bad_behaviors"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name != "generate_negative_skill":
        raise ValueError(f"Unknown tool: {name}")

    answers = {
        "context": arguments["context"],
        "bad_behaviors": arguments["bad_behaviors"],
        "forbidden_topics": arguments.get("forbidden_topics", []),
        "style_hates": arguments.get("style_hates", ""),
        "severity": arguments.get("severity", "moderate"),
    }

    skill_content = compile_skill(answers)
    filepath = save_skill(skill_content, answers["context"])

    if arguments.get("auto_install", False):
        installed_path = install_skill(skill_content, answers["context"])
        result = f"✅ Skill generated and installed to: {installed_path}\n\n{skill_content}"
    else:
        result = f"✅ Skill generated and saved to: {filepath}\n\n{skill_content}"

    return [types.TextContent(type="text", text=result)]


def run():
    asyncio.run(stdio_server(app))

if __name__ == "__main__":
    run()