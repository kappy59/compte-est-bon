from functools import lru_cache
from copy import copy
import re
from .tools import timeit, totaltimeit


@totaltimeit
def value__(str):
    return eval(str)


@lru_cache(maxsize=None)
def value(str):
    return value__(str)


@totaltimeit
def add_solution_to_set(candidate: str, solutions: set[str]) -> set[str]:
    score = len(re.findall(r"\d+", candidate))
    if solutions:
        best_score = len(re.findall(r"\d+", list(solutions)[0]))
        if score < best_score:
            solutions.clear()
            solutions.add(candidate)
        elif score == best_score:
            solutions.add(candidate)
    else:
        solutions.add(candidate)

    return solutions


def loop(expressions: list[str], target: int) -> set[str]:
    results = set([])

    first_value = value(expressions[0])
    if first_value < 0:
        return results

    elif first_value == target:
        results.add(expressions[0])
        return results

    for idx_1 in range(len(expressions) - 1):
        for idx_2 in range(idx_1 + 1, len(expressions)):
            comb = copy(expressions)
            a = comb.pop(idx_2)
            b = comb.pop(idx_1)

            a, b = (a, b) if value(a) < value(b) else (b, a)
            for solution in loop([f"({a} + {b})"] + comb, target):
                results = add_solution_to_set(solution, results)
            for solution in loop([f"({b} - {a})"] + comb, target):
                results = add_solution_to_set(solution, results)
            for solution in loop([f"({a} * {b})"] + comb, target):
                results = add_solution_to_set(solution, results)

            if value(b) and value(a) % value(b) == 0:
                for solution in loop([f"({a} // {b})"] + comb, target):
                    results = add_solution_to_set(solution, results)

            if value(a) and value(b) % value(a) == 0:
                for solution in loop([f"({b} // {a})"] + comb, target):
                    results = add_solution_to_set(solution, results)

    return results


@totaltimeit
def make_readable_for_ilyes(msg: str):
    return msg[1:-1].replace("*", "x").replace("//", "÷")


@totaltimeit
def explain(msg: str) -> None:
    while True:
        group_found = False
        for i in re.finditer(r"\([^\(\)]*\)", msg):
            group = i.group()
            if group[1:-1]:
                group_found = True
                clean_group = group.replace("°", "")

                print(
                    make_readable_for_ilyes(group), "=", str(value(clean_group)) + "°"
                )
                msg = msg.replace(group, str(value(clean_group)) + "°", 1)

        if not group_found:
            return

        if msg[:-1].isnumeric():
            return


@timeit
def solve(numbers: list[int], target: int) -> int:
    solutions = list(loop(numbers, target))
    if solutions:
        print(
            len(solutions),
            "solutions avec",
            len(re.findall(r"\d+", solutions[0])),
            "cartes",
        )
        print("--------------")
        for solution in solutions:
            explain(solution)
            print("--------------")
    else:
        print("Pas de solutions exactes")
