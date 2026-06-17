# agents

Claude Code 向けの専門エージェント・スキル・ワークフロープラグインを集めたマーケットプレイス。85 のエージェント、47 のスキル、44 のツールを 63 のプラグインに整理し、最小トークン消費で必要な機能だけを読み込める。

## 技術スタック

- Claude Code プラグインアーキテクチャ
- Markdown ベースのエージェント/スキル/コマンド定義
- Haiku / Sonnet ハイブリッドオーケストレーション

## セットアップ

Claude Code でマーケットプレイスを追加する:

```bash
/plugin marketplace add wshobson/agents
```

## クイックスタート

プラグイン一覧を表示してインストール:

```bash
/plugin
/plugin install python-development
/plugin install backend-development
/plugin install full-stack-orchestration
```

## 使用方法

インストールしたプラグインのエージェントをそのまま呼び出す:

```bash
# Python プロジェクトのスキャフォールディング
/python-development:python-scaffold fastapi-microservice

# フルスタック機能開発（7 エージェントが連携）
/full-stack-orchestration:full-stack-feature "user authentication with OAuth2"

# セキュリティ強化
/security-scanning:security-hardening --level comprehensive
```

## ドキュメント

- [plugins.md](docs/plugins.md) — 63 プラグインの完全カタログ
- [agents.md](docs/agents.md) — 85 エージェントの一覧とモデル設定
- [agent-skills.md](docs/agent-skills.md) — 47 スキルの詳細
- [usage.md](docs/usage.md) — コマンドリファレンスとワークフロー例
- [architecture.md](docs/architecture.md) — 設計方針とパターン

## ディレクトリ構成

```text
agents/
├── .claude-plugin/
│   └── marketplace.json      # 63 プラグイン定義
├── plugins/
│   ├── python-development/
│   │   ├── agents/           # Python 専門エージェント
│   │   ├── commands/         # スキャフォールディングツール
│   │   └── skills/           # 5 つの専門スキル
│   ├── kubernetes-operations/
│   ├── security-scanning/
│   └── ... (60 以上のプラグイン)
└── docs/                     # 設計・使用ドキュメント
```

## ライセンス

MIT License — [LICENSE](LICENSE)
