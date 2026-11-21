from pathlib import Path

for name, kind in (("users", "user"), ("orgs", "org")):
    p = Path(f"app/{name}.py")
    p.write_text(p.read_text().replace('make_key("profile",', f'make_key("{kind}", "profile",'))
print("Namespaced the cache keys.")
