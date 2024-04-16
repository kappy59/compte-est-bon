import yaml
import pytest


def parametrize_yaml(yaml_str: str):
    args = yaml.safe_load(yaml_str)
    ids = list(map(lambda arg: list(arg.keys())[0], args))
    datas = list(map(lambda arg: list(arg.values())[0].values(), args))
    params = set(map(lambda arg: tuple(list(arg.values())[0].keys()), args))
    assert len(params) == 1
    return pytest.mark.parametrize(",".join(list(params)[0]), datas, ids=ids)


def parametrize_yaml_from_file(yaml_file: str):
    with open(yaml_file, mode="rt", encoding="utf-8") as yaml_str:
        args = yaml.safe_load(yaml_str)
        ids = list(map(lambda arg: list(arg.keys())[0], args))
        datas = list(map(lambda arg: list(arg.values())[0].values(), args))
        params = set(map(lambda arg: tuple(list(arg.values())[0].keys()), args))
        assert len(params) == 1
        return pytest.mark.parametrize(",".join(list(params)[0]), datas, ids=ids)
