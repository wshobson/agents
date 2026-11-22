from dataclasses import dataclass, field


@dataclass
class Summary:
    total: int = 0
    passed: int = 0
    failed_names: list[str] = field(default_factory=list)


def summarize(text: str) -> Summary:
    summary = Summary()
    for line in text.splitlines():
        if not line.strip():
            continue
        name, _, status = line.partition("=")
        summary.total += 1
        if status.strip() == "pass":
            summary.passed += 1
        else:
            summary.failed_names.append(name.strip())
    return summary
