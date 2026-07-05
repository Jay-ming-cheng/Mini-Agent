"""
计算器工具。

职责：
1. 计算数学表达式。
2. 返回计算结果。

注意：
- 不负责解析用户意图。
- 不负责组织自然语言。
- 不负责异常恢复。
"""


def calculate(expression: str) -> int | float:
    """
    计算数学表达式。

    Args:
        expression: 数学表达式，例如 "2+3*4"

    Returns:
        计算结果。
    """
    try:
        #注意：
        #此处使用eval() 仅用于演示 Tool Workflow
        #在真实项目中，应使用安全的表达式解析器，
        #而不是直接执行用户输入。
        return eval(expression)
    except Exception as e:
        raise ValueError(f"非法数学表达式：{expression}") from e