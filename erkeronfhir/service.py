from datetime import date
from pathlib import Path
from typing import List

from fasadeonfhir.config import config
from fasadeonfhir.redcap.provider import RedcapProvider
from fasadeonfhir.service import Service

from erkeronfhir.capability import rest_capabilities


class ErkerService(Service):
    __app_name__ = "ERKER on FHIR"
    __capabilities_rest__ = rest_capabilities
    __capabilities_date__ = date.fromtimestamp(
        Path("erkeronfhir/capability.py").stat().st_mtime
    ).isoformat()

    def __init__(self) -> None:
        super().__init__()

        self.provider = RedcapProvider(config.redcap.api_url, config.redcap.api_token)

    def get_patients(self):
        return self._get_resources(resource_filter=["Patient"])

    def get_observations(self):
        return self._get_resources(resource_filter=["Observation"])

    def _get_resources(self, resource_filter: List[str] = None):
        records = self.provider.get_records()
        return self.mapper.create_from_list(records, resource_filter=resource_filter)
