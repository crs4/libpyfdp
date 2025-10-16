# SPDX-License-Identifier: Apache-2.0
# Copyright 2024-2025 CRS4 - Center for Advanced Studies, Research and
# Development in Sardinia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from SPARQLWrapper import SPARQLWrapper, JSON

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class FairDataPointFinder():
    class TripleStore():
        def __init__(self, url: str, repository: str, token: str = None):
            self._url = url
            self._repository = repository
            self._token = token

        @property
        def endpoint(self) -> str:
            return f"{self._url}/repositories/{self._repository}"

    def __init__(self, fair_data_point):
        self._fair_data_point = fair_data_point
        self._get_fdp_config()
        self._sparql = SPARQLWrapper(self._triplestore.endpoint)
        self._sparql.setReturnFormat(JSON)

    def _get_fdp_config(self):
        logger.debug(
            "Retrieving repository settings from the Fair Data Point '%s'",
            self._fair_data_point.url
        )
        r = self._fair_data_point._rest_operator.get("settings")
        self._triplestore = self.TripleStore(
            r['content']['repository']['url'],
            r['content']['repository']['repository'],
        )

    def catalog(self):
        query = [
            "PREFIX dcat: <http://www.w3.org/ns/dcat#>",
            "PREFIX dct: <http://purl.org/dc/terms/>",
            "SELECT ?catalog ?title WHERE {",
            "  ?catalog a dcat:Catalog ;",
            "    dct:title ?title ."
            "}"]

        query = "\n".join(query)
        logger.debug("Querying the repository:\n%s", query)

        self._sparql.setQuery(query)

        result = []

        try:
            ret = self._sparql.queryAndConvert()

            for r in ret["results"]["bindings"]:
                result.append(r['catalog']['value'])
        except Exception as e:
            logger.error(e)

        return result

    def dataset(self,
                lazy: bool = True,
                exclude_series: bool = False):
        """Query the Triple Store used by the Fair Data Point for Dataset.

        Query the Triple Store used by the Fair Data Point for Dataset that
        satisfies the conditions.

        :param exclude_series: if True does not returns the DatasetSeries but
            only the Datasets
        :type exclude_series: bool

        :param lazy: if True the Dataset instances returned are empty (only the
            URI is set), otherwise the full metadata are retrieved from the
            Fair Data Point.
        :type lazy: bool

        :return: the list of the Dataset instances matching the requested
            criteria.
        :rtype: list
        """
        query = [
            "PREFIX dcat: <http://www.w3.org/ns/dcat#>",
            "PREFIX dct: <http://purl.org/dc/terms/>",
            "",
            "SELECT ?dataset ?title WHERE {",
            "  ?dataset a dcat:Dataset ;",
            "    dct:title ?title ."]

        if exclude_series:
            query.append(
                "  FILTER NOT EXISTS { ?dataset a dcat:DatasetSeries . }")
        query.append("}")

        query = "\n".join(query)
        logger.debug("Querying the repository:\n%s", query)

        self._sparql.setQuery(query)

        result = []

        try:
            ret = self._sparql.queryAndConvert()

            for r in ret["results"]["bindings"]:
                from fdp.dataset import Dataset
                print(r['dataset']['value'])
                # result.append(r['dataset']['value'])

                if lazy:
                    result.append(Dataset(uuid=r['dataset']['value']))
                else:
                    result.append(Dataset(
                        fair_data_point=self._fair_data_point
                    ).get(uuid=r['dataset']['value'], absolute=True))

        except Exception as e:
            logger.error(e)

        print(result)
        return result

    def datasetseries(self):
        """
        """
        query = [
            "PREFIX dcat: <http://www.w3.org/ns/dcat#>",
            "PREFIX dct: <http://purl.org/dc/terms/>",
            "",
            "SELECT ?datasetseries ?title WHERE {",
            "  ?datasetseries a dcat:DatasetSeries; ",
            "    dct:title ?title ."
            "}"]

        query = "\n".join(query)
        logger.debug("Querying the repository:\n%s", query)

        self._sparql.setQuery(query)

        result = []

        try:
            ret = self._sparql.queryAndConvert()

            for r in ret["results"]["bindings"]:
                result.append(r['datasetseries']['value'])
        except Exception as e:
            logger.error(e)

        return result
