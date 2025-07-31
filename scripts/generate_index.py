import os
import yaml

def extract_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        if f.readline().strip() == "---":
            lines = []
            for line in f:
                if line.strip() == "---":
                    break
                lines.append(line)
            return yaml.safe_load("".join(lines))
    return None

def is_agent_file(filename):
    return (
        filename.endswith(".md")
        and not filename.lower() in ["readme.md", "agents.md"]
        and os.path.isfile(filename)
    )

def main():
    agent_files = [f for f in os.listdir('.') if is_agent_file(f)]
    agent_files.sort()

    with open("AGENTS.md", "w", encoding="utf-8") as out:
        out.write("# 📘 Index of Available Agents\n\n")
        for file in agent_files:
            meta = extract_metadata(file)
            if meta and "name" in meta and "description" in meta:
                out.write(f"- [`{meta['name']}`]({file}): {meta['description']}\n")

if __name__ == "__main__":
    main()
