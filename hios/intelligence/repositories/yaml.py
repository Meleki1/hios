from pathlib import Path

import yaml

from hios.intelligence.models.rule import Rule
from hios.intelligence.repositories.base import RuleRepository


class YamlRuleRepository(RuleRepository):

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

    def load(
        self,
    ) -> list[Rule]:

        rules = []

        for file in self._path.glob("*.yaml"):

            with open(file, "r", encoding="utf-8") as stream:

                data = yaml.safe_load(stream)

                rules.append(
                    Rule.model_validate(data)
                )

        return rules