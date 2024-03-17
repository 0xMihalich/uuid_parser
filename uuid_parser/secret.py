class Secret(dict):

    def __str__(self: "Secret") -> str:
        """Строковое представление класса."""

        string: str = ""

        for name, value in self.items():
            string += f"\n{name}: {value}"
        
        return string or "\nUndefined"

    def __repr__(self: "Secret") -> str:
        """Строковое представление класса для интерпретатора."""

        return self.__str__()
