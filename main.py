import json

import pandas as pd

from delta_repository import DeltaRepository

# from elastic_search import ElasticSearch

# es = ElasticSearch(host="http://127.0.0.1:9200", username="", password="")

# print(es.ping())

# mappings = {
#     "properties": {
#         "name": {"type": "text"},
#         "age": {
#             "type": "integer",
#         },
#     }
# }

# body = {
#     "track_total_hits": True,
#     "_source": ["name"],
#     "query": {
#         "terms": {"name": ["arpeet", "piyush", "prabhat", "aniket"]},
#     },
# }

# query = {
#     "query": {"terms": {"name": ["arpeet", "piyush", "prabhat", "aniket"]}},
#     "script": {
#         "source": "if (params.names.contains(ctx._source.name)) { ctx._source.age = params.age; } else { ctx.op = 'noop'; }",
#         "params": {
#             "names": ["arpeet", "piyush", "prabhat", "aniket"],
#             "age": 100000,
#         },
#     },
# }


# print(es.create_index(index="users", mappings=mappings))
# print(
#     es.bulk_index(
#         index="users",
#         documents=[
#             {"name": "Maya Patel", "age": 24},
#             {"name": "Liam Brooks", "age": 31},
#             {"name": "Nina Rao", "age": 42},
#             {"name": "Owen Chen", "age": 28},
#             {"name": "Sara Malik", "age": 35},
#             {"name": "Leo Santos", "age": 19},
#             {"name": "Iris Morgan", "age": 56},
#             {"name": "Avery Kim", "age": 63},
#         ],
#     )
# )

# print(es.search(index="users", body=body))

# delta_repo = DeltaRepository(es=es)
# records = delta_repo.get_summary("2026-01-01", duration_in_days=2)


with open("delta_events_sample.json", "r") as file:
    records = json.load(file)

df = pd.DataFrame(records)

print(df)