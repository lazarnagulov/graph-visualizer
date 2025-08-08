import operator
from typing import Dict, Callable


class CompareException(Exception):
    """Exception raised when trying to use non-valid operator."""
    def __init__(self, operator: str):
        super().__init__(f"{operator} is not a valid operator.")


class CompareUtil:
    __operators: Dict[str, Callable] = {
        "==": operator.eq,
        "!=": operator.ne,
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge
    }
    @staticmethod
    def compare(operator: str, operand1: any, operand2: any) -> bool:
        """
        Compares two operands using operator.

        Raises CompareException if operator is non-valid.

        :param operator: operator to use
        :param operand1: first operand
        :param operand2: second operand
        :return: comparison result
        """
        if operator not in CompareUtil.__operators:
            raise CompareException(operator)
        return CompareUtil.__operators[operator](operand1, operand2)


