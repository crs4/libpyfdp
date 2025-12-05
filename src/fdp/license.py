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


class License:
    """
    Constants for all non-deprecated SPDX license identifiers.

    Each constant is named after the SPDX identifier, converted to uppercase,
    with dots and hyphens replaced by underscores.
    The value of each constant is the canonical SPDX license URL.

    Example:

    .. code-block:: python

        from fdp.catalog import Catalog
        from fdp.license import License

        myCatalog = Catalog()

        # refers to https://creativecommons.org/licenses/by/1.0/legalcode
        myCatalog.license = License.CC_BY_1_0

    .. warning::
           Only Creative Commons licenses are supported at the moment.

    """
    #: Creative Commons Zero v1.0 Universal license
    CC0_1_0 =             "https://creativecommons.org/publicdomain/zero/1.0/legalcode"
    #: Creative Commons Attribution 1.0 Generic license
    CC_BY_1_0 =           "https://creativecommons.org/licenses/by/1.0/legalcode"
    #: Creative Commons Attribution 2.0 Generic license
    CC_BY_2_0 =           "https://creativecommons.org/licenses/by/2.0/legalcode"
    #: Creative Commons Attribution 2.5 Generic license
    CC_BY_2_5 =           "https://creativecommons.org/licenses/by/2.5/legalcode"
    #: Creative Commons Attribution 2.5 Australia license
    CC_BY_2_5_AU =        "https://creativecommons.org/licenses/by/2.5/au/legalcode"
    #: Creative Commons Attribution 3.0 Unported license
    CC_BY_3_0 =           "https://creativecommons.org/licenses/by/3.0/legalcode"
    #: Creative Commons Attribution 3.0 Austria license
    CC_BY_3_0_AT =        "https://creativecommons.org/licenses/by/3.0/at/legalcode"
    #: Creative Commons Attribution 3.0 Australia license
    CC_BY_3_0_AU =        "https://creativecommons.org/licenses/by/3.0/au/legalcode"
    #: Creative Commons Attribution 3.0 Germany license
    CC_BY_3_0_DE =        "https://creativecommons.org/licenses/by/3.0/de/legalcode"
    #: Creative Commons Attribution 3.0 IGO license
    CC_BY_3_0_IGO =       "https://creativecommons.org/licenses/by/3.0/igo/legalcode"
    #: Creative Commons Attribution 3.0 Netherlands license
    CC_BY_3_0_NL =        "https://creativecommons.org/licenses/by/3.0/nl/legalcode"
    #: Creative Commons Attribution 3.0 United States license
    CC_BY_3_0_US =        "https://creativecommons.org/licenses/by/3.0/us/legalcode"
    #: Creative Commons Attribution 4.0 International license
    CC_BY_4_0 =           "https://creativecommons.org/licenses/by/4.0/legalcode"
    #: Creative Commons Attribution Non Commercial 1.0 Generic license
    CC_BY_NC_1_0 =        "https://creativecommons.org/licenses/by-nc/1.0/legalcode"
    #: Creative Commons Attribution Non Commercial 2.0 Generic license
    CC_BY_NC_2_0 =        "https://creativecommons.org/licenses/by-nc/2.0/legalcode"
    #: Creative Commons Attribution Non Commercial 2.5 Generic license
    CC_BY_NC_2_5 =        "https://creativecommons.org/licenses/by-nc/2.5/legalcode"
    #: Creative Commons Attribution Non Commercial 3.0 Unported license
    CC_BY_NC_3_0 =        "https://creativecommons.org/licenses/by-nc/3.0/legalcode"
    #: Creative Commons Attribution Non Commercial 3.0 Germany license
    CC_BY_NC_3_0_DE =     "https://creativecommons.org/licenses/by-nc/3.0/de/legalcode"
    #: Creative Commons Attribution Non Commercial 4.0 International license
    CC_BY_NC_4_0 =        "https://creativecommons.org/licenses/by-nc/4.0/legalcode"
    #: Creative Commons Attribution Non Commercial No Derivatives 1.0 Generic license
    CC_BY_NC_ND_1_0 =     "https://creativecommons.org/licenses/by-nd-nc/1.0/legalcode"
    #: Creative Commons Attribution Non Commercial No Derivatives 2.0 Generic license
    CC_BY_NC_ND_2_0 =     "https://creativecommons.org/licenses/by-nc-nd/2.0/legalcode"
    #: Creative Commons Attribution Non Commercial No Derivatives 2.5 Generic license
    CC_BY_NC_ND_2_5 =     "https://creativecommons.org/licenses/by-nc-nd/2.5/legalcode"
    #: Creative Commons Attribution Non Commercial No Derivatives 3.0 Unported license
    CC_BY_NC_ND_3_0 =     "https://creativecommons.org/licenses/by-nc-nd/3.0/legalcode"
    #: Creative Commons Attribution Non Commercial No Derivatives 3.0 Germany license
    CC_BY_NC_ND_3_0_DE =  "https://creativecommons.org/licenses/by-nc-nd/3.0/de/legalcode"
    #: Creative Commons Attribution Non Commercial No Derivatives 3.0 IGO license
    CC_BY_NC_ND_3_0_IGO = "https://creativecommons.org/licenses/by-nc-nd/3.0/igo/legalcode"
    #: Creative Commons Attribution Non Commercial No Derivatives 4.0 International license
    CC_BY_NC_ND_4_0 =     "https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 1.0 Generic license
    CC_BY_NC_SA_1_0 =     "https://creativecommons.org/licenses/by-nc-sa/1.0/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 2.0 Generic license
    CC_BY_NC_SA_2_0 =     "https://creativecommons.org/licenses/by-nc-sa/2.0/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 2.0 Germany license
    CC_BY_NC_SA_2_0_DE =  "https://creativecommons.org/licenses/by-nc-sa/2.0/de/legalcode"
    #: Creative Commons Attribution-NonCommercial-ShareAlike 2.0 France license
    CC_BY_NC_SA_2_0_FR =  "https://creativecommons.org/licenses/by-nc-sa/2.0/fr/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 2.0 England and Wales license
    CC_BY_NC_SA_2_0_UK =  "https://creativecommons.org/licenses/by-nc-sa/2.0/uk/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 2.5 Generic license
    CC_BY_NC_SA_2_5 =     "https://creativecommons.org/licenses/by-nc-sa/2.5/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 3.0 Unported license
    CC_BY_NC_SA_3_0 =     "https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 3.0 Germany license
    CC_BY_NC_SA_3_0_DE =  "https://creativecommons.org/licenses/by-nc-sa/3.0/de/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 3.0 IGO license
    CC_BY_NC_SA_3_0_IGO = "https://creativecommons.org/licenses/by-nc-sa/3.0/igo/legalcode"
    #: Creative Commons Attribution Non Commercial Share Alike 4.0 International license
    CC_BY_NC_SA_4_0 =     "https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode"
    #: Creative Commons Attribution No Derivatives 1.0 Generic license
    CC_BY_ND_1_0 =        "https://creativecommons.org/licenses/by-nd/1.0/legalcode"
    #: Creative Commons Attribution No Derivatives 2.0 Generic license
    CC_BY_ND_2_0 =        "https://creativecommons.org/licenses/by-nd/2.0/legalcode"
    #: Creative Commons Attribution No Derivatives 2.5 Generic license
    CC_BY_ND_2_5 =        "https://creativecommons.org/licenses/by-nd/2.5/legalcode"
    #: Creative Commons Attribution No Derivatives 3.0 Unported license
    CC_BY_ND_3_0 =        "https://creativecommons.org/licenses/by-nd/3.0/legalcode"
    #: Creative Commons Attribution No Derivatives 3.0 Germany license
    CC_BY_ND_3_0_DE =     "https://creativecommons.org/licenses/by-nd/3.0/de/legalcode"
    #: Creative Commons Attribution No Derivatives 4.0 International license
    CC_BY_ND_4_0 =        "https://creativecommons.org/licenses/by-nd/4.0/legalcode"
    #: Creative Commons Attribution Share Alike 1.0 Generic license
    CC_BY_SA_1_0 =        "https://creativecommons.org/licenses/by-sa/1.0/legalcode"
    #: Creative Commons Attribution Share Alike 2.0 Generic license
    CC_BY_SA_2_0 =        "https://creativecommons.org/licenses/by-sa/2.0/legalcode"
    #: Creative Commons Attribution Share Alike 2.0 England and Wales license
    CC_BY_SA_2_0_UK =     "https://creativecommons.org/licenses/by-sa/2.0/uk/legalcode"
    #: Creative Commons Attribution Share Alike 2.1 Japan license
    CC_BY_SA_2_1_JP =     "https://creativecommons.org/licenses/by-sa/2.1/jp/legalcode"
    #: Creative Commons Attribution Share Alike 2.5 Generic license
    CC_BY_SA_2_5 =        "https://creativecommons.org/licenses/by-sa/2.5/legalcode"
    #: Creative Commons Attribution Share Alike 3.0 Unported license
    CC_BY_SA_3_0 =        "https://creativecommons.org/licenses/by-sa/3.0/legalcode"
    #: Creative Commons Attribution Share Alike 3.0 Austria license
    CC_BY_SA_3_0_AT =     "https://creativecommons.org/licenses/by-sa/3.0/at/legalcode"
    #: Creative Commons Attribution Share Alike 3.0 Germany license
    CC_BY_SA_3_0_DE =     "https://creativecommons.org/licenses/by-sa/3.0/de/legalcode"
    #: Creative Commons Attribution-ShareAlike 3.0 IGO license
    CC_BY_SA_3_0_IGO =    "https://creativecommons.org/licenses/by-sa/3.0/igo/legalcode"
    #: Creative Commons Attribution Share Alike 4.0 International license
    CC_BY_SA_4_0 =        "https://creativecommons.org/licenses/by-sa/4.0/legalcode"
    #: Creative Commons Public Domain Dedication and Certification license
    CC_PDDC =             "https://creativecommons.org/licenses/publicdomain/"
    #: Creative    Commons Public Domain Mark 1.0 Universal license
    CC_PDM_1_0 =          "https://creativecommons.org/publicdomain/mark/1.0/"
    #: Creative Commons Share Alike 1.0 Generic license
    CC_SA_1_0 =           "https://creativecommons.org/licenses/sa/1.0/legalcode"
