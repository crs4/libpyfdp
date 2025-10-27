===============
Getting started
===============

Welcome to the LibPyFDP library tutorial! This guide will help you get started with creating and managing DCAT metadata for Fair Data Points (FDP).

.. contents:: Table of Contents
   :depth: 3
   :local:

Installation
============

Prerequisites
-------------

Before installing the library, ensure you have:

* Python 3.11 or higher
* pip package manager
* Access credentials for your Fair Data Point (if applicable)

Install via pip
---------------

Install the latest stable version from PyPI:

.. code-block:: bash

   pip install libpyfdp

Install from source
-------------------

For the latest development version:

.. code-block:: bash

   git clone https://github.com/crs4/libpyfdp.git
   cd libpyfdp
   pip install -e .

Verify Installation
-------------------

Verify the installation by importing the library:

.. code-block:: python

  import fdp
  print(fdp.__version__)

Basic Usage
===========

..
        Connecting to a Fair Data Point
        --------------------------------
        
        First, establish a connection to your FDP instance:
        
        .. code-block:: python
        
           import fdp
        
           # Initialize the FDP client
           client = fdp.faidatapoint.FairDataPoint(
               base_url="https://your-fdp-instance.org",
               username="your_username",
               password="your_password"
           )
        
           # Verify connection
           print(client.get_status())

Creating a DCAT Catalog
------------------------

A Catalog is the top-level container for datasets in DCAT:

.. code-block:: python

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

Getting Help
------------

* GitHub Issues: https://github.com/crs4/libpyfdp/issues
* Documentation: https://libpyfdp.readthedocs.io
