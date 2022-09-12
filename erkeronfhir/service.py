from typing import List

import fhir.resources
from fasadeonfhir.config import config
from fasadeonfhir.redcap.provider import RedcapProvider
from fasadeonfhir.service import Service
from fhir.resources.capabilitystatement import CapabilityStatement


class ErkerService(Service):
    __app_name__ = "ERKER on FHIR"
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

    def get_capability(self):
        definition = {
            "software": {"name": self.__app_name__},
            "fhirVersion": fhir.resources.__fhir_version__,
            "status": "active",
            "kind": "capability",
            "date": "2022-08-30",
            "format": ["json"],
            "rest": [
                {
                    "mode": "server",
                    "resource": [
                        {"type": "Patient", "interaction": [{"code": "read"}]},
                        {"type": "Observation", "interaction": [{"code": "read"}]},
                    ],
                },
            ],
        }

        return CapabilityStatement(**definition)
