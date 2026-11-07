from dataclasses import dataclass


@dataclass
class WordFormat:
    lemma: str
    tags: list[str]
