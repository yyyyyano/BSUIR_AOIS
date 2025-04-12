import pytest
from AOIS.lab3.models.minimisation_methods import MinimisationMethods

@pytest.mark.parametrize("norm_formula, expected_implicants", [
    ("(A | B) & (A | !B) & (!A | B) & (!A | !B)", ["(A)", "(!A)"]),
])
def test_calc_method_sknf(capsys, norm_formula, expected_implicants):
    MinimisationMethods.calc_method_sknf(norm_formula)
    captured = capsys.readouterr()
    for imp in expected_implicants:
        assert imp in captured.out


@pytest.mark.parametrize("norm_formula, expected_implicants", [
    ("(A & B) | (A & !B) | (!A & B) | (!A & !B)", ["(A)", "(!A)"]),
])
def test_calc_method_sdnf(capsys, norm_formula, expected_implicants):
    MinimisationMethods.calc_method_sdnf(norm_formula)
    captured = capsys.readouterr()
    for imp in expected_implicants:
        assert imp in captured.out


@pytest.mark.parametrize("norm_formula, expected_implicants", [
    ("(A | B) & (A | !B) & (!A | B) & (!A | !B)", ["(A)", "(!A)"]),
])
def test_calc_table_method_sknf(capsys, norm_formula, expected_implicants):
    MinimisationMethods.calc_table_method_sknf(norm_formula)
    captured = capsys.readouterr()
    for imp in expected_implicants:
        assert imp in captured.out


@pytest.mark.parametrize("norm_formula, expected_implicants", [
    ("(A & B) | (A & !B) | (!A & B) | (!A & !B)", ["(A)", "(!A)"]),
])
def test_calc_table_method_sdnf(capsys, norm_formula, expected_implicants):
    MinimisationMethods.calc_table_method_sdnf(norm_formula)
    captured = capsys.readouterr()
    for imp in expected_implicants:
        assert imp in captured.out


@pytest.mark.parametrize("norm_formula", [
    ("(A | B)"),
])
def test_carno_sknf(capsys, norm_formula):
    expected_implicants=['A | B']
    MinimisationMethods.carno_sknf(norm_formula)
    captured = capsys.readouterr()
    for imp in expected_implicants:
        assert imp in captured.out


@pytest.mark.parametrize("norm_formula, expected_implicants", [
    ("(!A & B) | (A & !B) | (A & B)", ["(A)", "(B)"]),
])
def test_carno_sdnf(capsys, norm_formula, expected_implicants):
    MinimisationMethods.carno_sdnf(norm_formula)
    captured = capsys.readouterr()
    for imp in expected_implicants:
        assert imp in captured.out
