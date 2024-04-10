from functools import lru_cache
from copy import copy
import re


@lru_cache(maxsize=None)
def evaluate(expression: str) -> str:
    return str(eval(expression))


@lru_cache(maxsize=None)
def loop_cached(expressions: str, target: int) -> set[str]:
    expressions = expressions.split()

    results = set([])
    if int(evaluate(expressions[0])) < 0:
        return results

    elif evaluate(expressions[0]) == target:
        results.add(expressions[0])
        return results

    for idx_1 in range(len(expressions) - 1):
        for idx_2 in range(1, len(expressions)):
            comb = copy(expressions)
            a = comb.pop(idx_2)
            b = comb.pop(idx_1)

            for result in loop(["(" + a + "+" + b + ")"] + comb, target):
                results.add(result)

            for result in loop(["(" + a + "-" + b + ")"] + comb, target):
                results.add(result)

            for result in loop(["(" + a + "*" + b + ")"] + comb, target):
                results.add(result)

            if eval(b) and eval(a) % eval(b) == 0:
                for result in loop(["(" + a + "//" + b + ")"] + comb, target):
                    results.add(result)

    return results


def loop(expressions: list[str], target: int) -> set[str]:
    expressions = sorted(expressions, key=lambda x: evaluate(x))
    return loop_cached(" ".join(expressions), target)


def main() -> int:
    # numbers = input().split()
    # assert len(numbers) == 6
    # target = int(input())
    # assert 100 <= target < 1000

    numbers = [7, 1, 5, 2, 10, 50]
    target = 527
    target = 406

    numbers = list(map(str, numbers))
    target = str(target)
    solutions = {i: [] for i in range(1, 7)}
    for solution in loop(numbers, target):
        print(solution)
        solutions[len(re.findall(r"\d+", solution))].append(solution)
    print(solutions)


if __name__ == "__main__":
    main()
