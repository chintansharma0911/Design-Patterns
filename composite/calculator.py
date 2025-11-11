from abc import ABC, abstractmethod


class ArithmeticExpression(ABC):
    @abstractmethod
    def evaluate(self):
        pass


class Number(ArithmeticExpression):

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class Expression(ArithmeticExpression):

    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation

    def evaluate(self):
        if self.operation == '+':
            return self.left.evaluate() + self.right.evaluate()
        elif self.operation == '-':
            return self.left.evaluate() - self.right.evaluate()
        if self.operation == '*':
            return self.left.evaluate() * self.right.evaluate()
        if self.operation == '/':
            return self.left.evaluate() / self.right.evaluate()
        else:
            return 0

if __name__ == '__main__':
    print(Expression(Number(7),Expression(Number(3),Number(4),'+'), '*').evaluate())
