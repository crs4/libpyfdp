# Getting started

Welcome to the **LibPyFDP** library tutorial! This guide will help you get started with creating and managing DCAT metadata in Fair Data Points (FDP).

```{contents}
:local:
:depth: 2
```

---

## Installation

### Prerequisites

Before installing the library, ensure you have:

- Python 3.11 or higher  
- pip package manager  
- Access credentials for your Fair Data Point (if applicable)

### Install via pip

Install the latest stable version from PyPI:

```{code-block} bash
pip install libpyfdp
```

### Install from source

For the latest development version:

```{code-block} bash
git clone https://github.com/crs4/libpyfdp.git
cd libpyfdp
pip install -e .
```

### Verify Installation

Verify the installation by importing the library:

```{code-block} python
import fdp
print(fdp.__version__)
```

## Basic Usage

### Retrieving Catalogs from the Fair Data Point

To retrieve **all public** Catalogs from the Fair Data Point:

```{code-block} python
from fdp.fairdatapoint import FairDataPoint

myfdp = FairDataPoint("http://fdp")

# 'find_catalogs()' returns a list of all catalogs available to the user
for catalog in myfdp.find_catalogs():
    print(catalog)
```

To retrieve **all public and draft (non-public)** Catalogs from the Fair Data Point, a *token* must first be obtained.
From the shell, if credentials are available, the token can be acquired with the following command:

```{code-block} bash
export FDP_TOKEN=$(curl -s -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
    -d "{\"email\": \"<user_email>\", \"<user_password>\": \"password\"}" http://fdp/tokens | jq -r .token)
```

For the official Fair Data Point Docker container image, using the default credentials:

```{code-block} bash
export FDP_TOKEN=$(curl -s -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
    -d "{\"email\": \"albert.einstein@example.com\", \"password\": \"password\"}" http://fdp/tokens | jq -r .token)
```

```{code-block} python
import os

from fdp.fairdatapoint import FairDataPoint

myfdp = FairDataPoint("http://fdp", token=os.environ.get('FDP_TOKEN'))

for catalog in myfdp.find_catalogs():
    print(catalog)
```

### Inspecting a Catalog

```{code-block} python
from pprint import pprint

mycatalog = myfdp.find_catalogs()[0]

# 'properties' is the list of the available Catalog's properties
print(mycatalog.properties)

# 'inspects()' returns the available Catalog's properties and their values as a dictionary
pprint(mycatalog.inspect())

# a prettier print
for property in mycatalog.properties:
    print(f"{property.upper()} => \n\t{getattr(mycatalog, property)}")
```

### Creating a DCAT Catalog

A Catalog is the top level container for datasets in DCAT:

```{code-block} python
import fdp
from fdp.catalog import Catalog
from fdp.foaf import FOAFOrganization

catalog = Catalog(
    title="My Research Data Catalog",
    description="Collection of datasets from our research project",
    publisher=FOAFOrganization(
        name="Research Institution",
        homepage="https://www.example.com/research_institution",
    ),
    language="en",
    license="https://creativecommons.org/licenses/by/4.0/"
)
```
