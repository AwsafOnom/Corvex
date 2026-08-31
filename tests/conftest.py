"""Global test isolation for Corvex's persistent store.

Every test gets a throwaway ``CORVEX_HOME`` (and a clean slate for the
memory/bank env switches). Without this, a developer machine where
persistent memory is ENABLED in ``~/.corvex/config.json`` leaks in both
directions: agent-running tests write fixture scripts into the developer's
REAL script bank / staging buffer, and the bank's retrieval hooks inject
exemplar blocks into golden-pinned prompts (observed live: 7 golden
mismatches + fixture records in the real store the first time the suite ran
on a memory-enabled machine).

Tests that exercise the memory features opt back in explicitly with their
own ``monkeypatch.setenv`` calls, which run after this autouse fixture and
override it.
"""

import pytest


@pytest.fixture(autouse=True)
def _isolated_corvex_home(tmp_path_factory, monkeypatch):
    home = tmp_path_factory.mktemp("corvex_home")
    monkeypatch.setenv("CORVEX_HOME", str(home))
    monkeypatch.delenv("CORVEX_MEMORY", raising=False)
    monkeypatch.delenv("CORVEX_SCRIPT_BANK", raising=False)
