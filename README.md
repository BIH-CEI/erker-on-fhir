# ERKER on FHIR

[![Docker](https://github.com/BIH-CEI/erker-on-fhir/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/BIH-CEI/erker-on-fhir/actions/workflows/docker-publish.yml)

## Workflow

Multiple parts:
* REDCap interface to request data using the REDCap API
    * using pycap
* Mapping from REDCap records to FHIR resources
    * dynamic specification from e.g. YAML file
* FHIR interface to provide read-access for resources
* Authentication (binding Charite AD)

@startuml
object REDCap
object REDCapInterface
object Mapping
object FHIRInterface

REDCap <- REDCapInterface
REDCapInterface <- Mapping
Mapping <- FHIRInterface
@enduml

## Start

### From Source

Start with 

```bash
uvicorn erkeronfhir.api:app --reload
```

### Using Docker

```bash
docker run --rm \
    -v $(pwd)/configs:/app/configs \
    -p 8765:8000 \
    [-e http_proxy=<proxy>] \
    [-e https_proxy=<proxy>] \
    ghcr.io/bih-cei/erker-on-fhir:main
```

## Package

Install this repository as Python package using

```bash
pip install git+https://github.com/BIH-CEI/erker-on-fhir#egg=erkeronfhir
```
