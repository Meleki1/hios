from hios.intelligence.matchers.base import RuleMatcher
from hios.intelligence.models.rule import Rule


class KeywordRuleMatcher(RuleMatcher):
    """
    Matches rules using keyword lookup.
    """

    def matches(
        self,
        rule: Rule,
        text: str,
    ) -> bool:

        text = text.lower()

        return any(
            keyword.lower() in text
            for keyword in rule.keywords
        )