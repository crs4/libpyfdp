---
title: LibPyFDP
date: 2025-10-25
authors:
  - name: Massimo Gaggero
    affiliations:
      - CRS4 - Center for Advanced Studies, Research and Development in Sardinia
---

<h1>LibPyFDP</h1>

::::{grid}
:reverse:
:gutter: 2 1 1 1
:margin: 4 4 1 1

:::{grid-item}
:columns: 4

```{image} ./_static/logo.png
:width: 200px
```
:::

:::{grid-item}
:columns: 8
:class: sd-fs-3

A Python library for DCAT metadata management in Fair Data Points

:::

::::

![GitHub branch check runs](https://img.shields.io/github/check-runs/crs4/libpyfdp/develop)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/crs4/libpyfdp/docs.yaml?label=docs)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fcrs4%2Flibpyfdp%2Frefs%2Fheads%2Fdevelop%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/crs4/libpyfdp)
![Coverage](https://crs4.github.io/libpyfdp/badges/coverage.svg)

The LibPyFDP library simplifies the process of creating, searching, and managing dataset metadata compliant with the DCAT (Data Catalog Vocabulary) standard for insertion into Fair Data Points. It is designed specifically for data scientists and data analysts who need to make their research data FAIR (Findable, Accessible, Interoperable, and Reusable).

<h2>Key Features</h2>

* **Easy DCAT creation**: Programmatically create DCAT Catalogs, Datasets, Dataset Series, and Distributions
* **FDP integration**: Seamless insertion of metadata into Fair Data Points
* **Search and retrieve**: Query existing metadata from FDP instances
* **Pythonic API**: Intuitive interface designed for data professionals

<h2>Getting Help</h2>

- **GitHub Issues:** [https://github.com/crs4/libpyfdp/issues](https://github.com/crs4/libpyfdp/issues)  
- **Documentation:** [https://crs4.github.io/libpyfdp](https://crs4.github.io/libpyfdp)

<h2>License</h2>

This library is released under the **[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)**. See LICENSE file for details.

---

# Documentation
```{toctree}
:maxdepth: 1

tutorials
```

```{toctree}
:maxdepth: 1
:caption: Reference

dcat
fdp

foaf
```
