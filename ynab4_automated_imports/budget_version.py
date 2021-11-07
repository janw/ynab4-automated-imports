class BudgetVersion:
    _version: int
    _prefix: str

    def __init__(self, version: str):
        self._prefix, ver = version.split("-", maxsplit=1)
        self._version = int(ver)

    def bump(self):
        self._version += 1
        return str(self)

    def __str__(self):
        return f"{self._prefix}-{self._version}"

    def __repr__(self):
        return f"BudgetVersion({self})"

    def __eq__(self, other):
        if isinstance(other, str):
            other = BudgetVersion(other)
        return self._version == other._version

    def __lt__(self, other):
        if isinstance(other, str):
            other = BudgetVersion(other)
        return self._version < other._version
