class GetFunctionFailException(Exception):
    """获取功能失败异常"""

    def __init__(self, function_name: str) -> None:
        super().__init__(function_name)
