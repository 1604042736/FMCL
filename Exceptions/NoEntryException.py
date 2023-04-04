class NoEntryException(Exception):
    """没有入口异常"""

    def __init__(self, function_name: str) -> None:
        super().__init__(function_name)
