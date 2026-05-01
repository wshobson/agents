# Machine Learning Ops

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `data-scientist` | inherit | Expert data scientist for advanced analytics, machine learning, and statistical modeling. Handles complex data analys... |
| `ml-engineer` | inherit | Build production ML systems with PyTorch 2.x, TensorFlow, and modern ML frameworks. Implements model serving, feature... |
| `mlops-engineer` | inherit | Build comprehensive ML pipelines, experiment tracking, and model registries with MLflow, Kubeflow, and modern MLOps t... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/machine-learning-ops:ml-pipeline` | Machine Learning Pipeline - Multi-Agent MLOps Orchestration |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `ml-pipeline-workflow` | Build end-to-end MLOps pipelines from data preparation through model training, validation, and production deployment. Use when creating M... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert data scientist for advanced analytics, machine learning, and statistical modeling" → activates `data-scientist`
- "Build end-to-end MLOps pipelines from data preparation through model training, validation, and production deployment" → activates `ml-pipeline-workflow` skill
- In Claude Code: `/machine-learning-ops:ml-pipeline` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
