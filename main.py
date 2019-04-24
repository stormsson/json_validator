import json
from validator.schema import Schema

schema_obj = None
with open("data/simple_schema.json") as f:
    schema_obj = json.load(f)

s = Schema(schema_obj)

with open("data/simple.json") as f:
    js_obj = json.load(f)

    print(s.validate(js_obj))