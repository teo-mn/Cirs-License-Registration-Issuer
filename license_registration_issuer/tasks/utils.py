from verify4py.json_utils import json_wrap
from verify4py.utils import calc_hash_str


def employee_data_convert(employee: dict):
    secret_hash = calc_hash_str(json_wrap({"regnum": employee["regnum"],
                                           "first_name": employee["first_name"],
                                           "last_name": employee["last_name"]}))
    info = json_wrap({"profession": employee["profession"], "degree": employee["degree"]})
    return secret_hash, info
