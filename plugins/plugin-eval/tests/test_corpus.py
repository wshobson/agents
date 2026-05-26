from pathlib import Path

import pytest

from plugin_eval.corpus import Corpus


class TestCorpus:
    def test_init_from_plugins(self, sample_plugin_dir: Path, tmp_path: Path):
        corpus_dir = tmp_path / "corpus"
        corpus = Corpus.init_from_source(sample_plugin_dir.parent, corpus_dir)
        assert corpus.size > 0
        assert (corpus_dir / "index.json").exists()

    def test_select_references(self, sample_plugin_dir: Path, tmp_path: Path):
        corpus_dir = tmp_path / "corpus"
        corpus = Corpus.init_from_source(sample_plugin_dir.parent, corpus_dir)
        refs = corpus.select_references(category="development", n=3)
        assert len(refs) <= 3

    def test_list_skills(self, sample_plugin_dir: Path, tmp_path: Path):
        corpus_dir = tmp_path / "corpus"
        corpus = Corpus.init_from_source(sample_plugin_dir.parent, corpus_dir)
        skills = corpus.list_skills()
        assert len(skills) > 0
