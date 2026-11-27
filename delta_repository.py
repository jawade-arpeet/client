from datetime import date, datetime, time, timedelta, timezone
from enum import Enum

from elastic_search import ElasticSearch


class DeltaStatus(Enum):
    GENERATED = "GENERATED"
    PROCESSED = "PROCESSED"
    SKIPPED = "SKIPPED"


class DeltaEventType:
    INGESTED = "INGESTED"
    ROLLED_BACK = "ROLLED_BACK"


class Env(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class DeltaRepository:
    def __init__(self, es: ElasticSearch) -> None:
        self.__es = es

    def create_delta_record(
        self,
        delta_id,
        country_code,
        content_type,
        generated_at,
        engineer_username,
        engineer_user_id,
        researcher_username,
        researcher_user_id,
    ):
        doc = {
            "delta_id": delta_id,
            "country_code": country_code,
            "content_type": content_type,
            "status": DeltaStatus.GENERATED,
            "generated_at": generated_at,
            "researcher": {
                "id": researcher_user_id,
                "name": researcher_username,
            },
            "engineer": {
                "id": engineer_user_id,
                "name": engineer_username,
            },
        }

        return self.__es.index(index="deltas", document=doc)

    def get_summary(self, start_date, duration_in_days):
        start = datetime.combine(date.fromisoformat(start_date), time.min, timezone.utc)
        end = start + timedelta(days=duration_in_days)

        body = {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "occurred_at": {
                                    "gte": start.isoformat(),
                                    "lt": end.isoformat(),
                                }
                            }
                        }
                    ]
                }
            }
        }

        return [
            hit["_source"] for hit in self.__es.scan(index="delta_events", body=body)
        ]

    def create_delta_event_record(
        self,
        event_id,
        delta_id,
        country_code,
        content_type,
        env,
        event_type,
        occurred_at,
        engineer_username,
        engineer_user_id,
        researcher_username,
        researcher_user_id,
    ):
        doc = {
            "event_id": event_id,
            "delta_id": delta_id,
            "country_code": country_code,
            "content_type": content_type,
            "env": env,
            "event_type": event_type,
            "occurred_at": occurred_at,
            "researcher": {
                "id": researcher_user_id,
                "name": researcher_username,
            },
            "engineer": {
                "id": engineer_user_id,
                "name": engineer_username,
            },
        }

        return self.__es.index(index="delta_events", document=doc)
