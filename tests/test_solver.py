import io
import contextlib
from solver import solver
from tests.tools import parametrize_yaml

test_explain_data_yaml = """
- empty string:
    input: "()"
    expected_output: ""
- missing ():
    input: "50 + 2"
    expected_output: ""
- stupid text:
    input: "bonzai"
    expected_output: ""
- invalid char:
    input: "$"
    expected_output: ""
- 1 addition:
    input: "(3 + 5)"
    expected_output: "3 + 5 = 8°\\n"
- 1 substraction:
    input: "(13 - 5)"
    expected_output: "13 - 5 = 8°\\n"
- 1 multiplication:
    input: "(3 * 5)"
    expected_output: "3 x 5 = 15°\\n"
- 1 division:
    input: "(10 // 5)"
    expected_output: "10 ÷ 5 = 2°\\n"
- reuse result:
    input: "((3 * 5) + 1)"
    expected_output: "3 x 5 = 15°\\n15° + 1 = 16°\\n"
- multiple reuse result:
    input: "((3 * 5) + (4 * 10))"
    expected_output: "3 x 5 = 15°\\n4 x 10 = 40°\\n15° + 40° = 55°\\n"
- complex nested operations:
    input: "((((3 * 5) * 2) // 5) + (4 * 10))"
    expected_output: "3 x 5 = 15°\\n4 x 10 = 40°\\n15° x 2 = 30°\\n30° ÷ 5 = 6°\\n6° + 40° = 46°\\n"
"""


@parametrize_yaml(test_explain_data_yaml)
def test_explain(input, expected_output):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        solver.explain(input)
        assert output.getvalue() == expected_output


test_make_readable_for_ilyes_data_yaml = """
- addition / substraction:
    input: "(5 + 3 - 4)"
    expected_output: "5 + 3 - 4"
- multiplication:
    input: "(50 * 2)"
    expected_output: "50 x 2"
- division:
    input: "(50 // 2)"
    expected_output: "50 ÷ 2"
- missing ():
    input: "50 // 2"
    expected_output: "0 ÷ "
- random spacing:
    input: "(4+  50 *1            -1)"
    expected_output: "4+  50 x1            -1"
- other characters:
    input: "b~ % ¤ ° n<)"
    expected_output: "~ % ¤ ° n<"
"""


@parametrize_yaml(test_make_readable_for_ilyes_data_yaml)
def test_make_readable_for_ilyes(input, expected_output):
    assert solver.make_readable_for_ilyes(input) == expected_output


test_value_data_yaml = """
- int:
    input: "12"
    expected_output: 12
    error: False
- operation:
    input: "1 + 2"
    expected_output: 3
    error: False
- multiple operations:
    input: "5 * 9 // 3 + 2"
    expected_output: 17
    error: False
- no numerical result is an error:
    input: "bonjour"
    expected_output:
    error: True
- invalid operations:
    input: "( 5 * 1 + "
    expected_output:
    error: True
"""


@parametrize_yaml(test_value_data_yaml)
def test_value(input, expected_output, error):
    try:
        assert solver.value(input) == expected_output
        assert not error
    except Exception:
        assert error


test_add_solution_to_set_data_yaml = """
- empty set of solutions:
    input:
        solutions:
        candidate: (3 + 4)
    expected_output:
        - (3 + 4)
- solution matching length in set:
    input:
        solutions:
            - (1 + 6)
            - (2 + 5)
        candidate: (3 + 4)
    expected_output:
        - (1 + 6)
        - (2 + 5)
        - (3 + 4)
- solution with more tiles than those in set:
    input:
        solutions:
            - (1 + 6)
            - (2 + 5)
        candidate: (1 + 1 + 5)
    expected_output:
        - (1 + 6)
        - (2 + 5)
- solution with less tiles than those in set:
    input:
        solutions:
            - (1 + 6)
            - (2 + 5)
        candidate: (7)
    expected_output:
        - (7)
"""


@parametrize_yaml(test_add_solution_to_set_data_yaml)
def test_add_solution_to_set(input, expected_output):
    solutions = set() if not input["solutions"] else set(input["solutions"])
    solutions = solver.add_solution_to_set(input["candidate"], solutions)
    assert not solutions.symmetric_difference(set(expected_output))


test_loop_data_yaml = """
- easy 2 numbers:
    input:
        numbers:
            - "1"
            - "2"
        target: 3
    expected_output:
        - (1 + 2)
- 1 useless numbers:
    input:
        numbers:
            - "1"
            - "2"
            - "7"
        target: 3
    expected_output:
        - (1 + 2)
- 2 solutions:
    input:
        numbers:
            - "1"
            - "2"
            - "5"
        target: 3
    expected_output:
        - (1 + 2)
        - (5 - 2)
- 1 short solution:
    input:
        numbers:
            - "1"
            - "2"
            - "3"
            - "4"
            - "10"
            - "101"
        target: 100
    expected_output:
        - (101 - 1)
- multiple operations / possibles:
    input:
        numbers:
            - "7"
            - "5"
            - "2"
            - "3"
        target: 18
    expected_output:
        - (2 * ((7 - 3) + 5))
        - (2 * ((5 + 7) - 3))
        - (5 + ((2 * 3) + 7))
        - (3 * ((5 + 7) // 2))
        - ((5 - 3) * (2 + 7))
        - ((3 * 7) - (5 - 2))
        - (((2 + 3) * 5) - 7)
        - (2 + ((3 * 7) - 5))
        - ((3 * (5 + 7)) // 2)
        - (2 * ((5 - 3) + 7))
        - (((7 - 3) * 5) - 2)
        - ((2 + (3 * 7)) - 5)
        - ((2 * 3) + (5 + 7))
        - (7 + (5 + (2 * 3)))
        - (((5 - 2) * 7) - 3)
- impossible:
    input:
        numbers:
            - "1"
            - "4"
        target: 2
    expected_output:
"""


@parametrize_yaml(test_loop_data_yaml)
def test_loop(input, expected_output):
    expected_output = set(expected_output if expected_output else [])
    assert expected_output == solver.loop(input["numbers"], input["target"])
