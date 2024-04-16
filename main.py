from solver import solver
from solver.tools import totaltimeit_dump

if __name__ == "__main__":
    numbers = input("Entre les cartes dispo séparées par un espace: ").split()
    assert len(numbers) == 6
    target = int(input("Combien je dois trouver: "))
    assert 100 <= target < 1000
    solver.solve(numbers, target)
    totaltimeit_dump()
