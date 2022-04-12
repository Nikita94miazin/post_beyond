class CustomError(ValueError):
    def __init__(self, code: int, description: str) -> None:
        self.code: int = code
        self.description: str = description
