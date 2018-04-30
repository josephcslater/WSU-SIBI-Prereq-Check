#! /opt/local/bin/python

import pandas as pd
import numpy as np
import math
import os.path
import time
import sys
import re
import os

# check_report is the function that can be fed a filename and prereqdict
# to print out prereq test results.


# Course prerequisites are defined in one of three ways that handles all cases
# All course names must be in parentheses (sorry!) ans with no spaces
# Requirements are added per examples below as
# Course definitions are inside parentheses
# Definitions of requirements are made by adding a line of the form
# Course name: (definitions),
# The comma is necessary, as are the parentheses
#
# Definitions:
# A single course definition required is simply listed, for example
#       "ME2700"
# A list of multiple required courses is in square brackets, for example
#       ["ME1020", "ME2120"]
# Multiple methods of satisfying the requirement are created by multiple
# lists, each in square brackets.
# For instance, consider a situation where both ME1010 and ME 2120 are
# required for ME 2700. This is listed as
#       "ME2700":(["CHM1210","PHY2400"]),
# On the other hand, if either is sufficient, then they are listed instead as
#       "ME2700":(["CHM1210"],["PHY2400"]),
# Here the code will go through each list to see if is is satisfied.
# In the scenario where prerequisites can be satisfied by a single course or
# Two other courses, they must be definined as two separate lists, even though
# one of the lists is a list of length 1.
# Let's consider a complicated example, ME2120. In that case, the prerequisites
# are (EGR1010 or MTH2310) and ME1040 and PHY2400
# This construc really means that there are two possible solutions,
# EGR1010, ME1040 and PHY2400 or MTH2310, ME1040 and PHY2400
# This is written as:
#       "ME2120":(["EGR1010", "ME1040", "PHY2400"],["MTH2310", "ME1040", "PHY2400"]),

# print('capstone design')
# print('ME 1040 and ME 3600 and MTH 2320 and PHY 2410 and PHY 2410L and ((ME 3210 and ME 3310 and ME 3360 and ME 4140) or (ME 3760 and ME 4620 (ME 4620 (with concurrency) and ME 4720))')

prereqdict = {"ME1020": (["EGR1010"], ["MTH2300", "MTH2310"]),
              "ME2120": (["EGR1010", "ME1040", "PHY2400"], ["EGR1010", "ME2020", "PHY2400"], ["MTH2310", "ME1040", "PHY2400"], ["MTH2310", "ME2020", "PHY2400"]),
              "ME2210": (["ME1020", "ME2120"]),  # Verified Aug-15-2016
              # This is a pre or co requisite. How to code? I think this works now.
              "ME2600": ("ME2700c"),  # Recitation is a co-requisite
              "ME2700": (["CHM1210", "PHY2400"]),
              "ME3120": (["ME1020", "ME2120"]),  # Verified Aug-15-2016
              "ME3210": (["EE2010", "ME2210", "ME3120", "ME3350", "MTH2350"],["EE2010", "ME2210", "ME3120", "ME3350", "MTH2350"]),  # Verified Aug-16-2016
              "ME3310": (["EGR1010", "PHY2400"], ["MTH2310c", "PHY2400"]),
              "ME3320": (["ME1020", "ME3310"]),  # Verified Aug-16-2016
              "ME3350": (["ME2210", "ME3310"]),  # Verified Aug-16-2016
              "ME3360": (["ME3350", "MTH2350"],["ME3350", "MTH2350"]),  # Verified Aug-15-2016
              "ME3600": (["EE2010", "EGR3350", "ME2120", "MTH2350"],["EE2010", "EGR3350", "ME2120", "MTH2330", "MTH2530"]),
              "ME3750": ("ME2700"),  # Verified Aug-15-2016
              "ME3760": ("ME3750"),  # Verified Aug-15-2016
              "ME4010": (["ME3360", "ME3210"]),  # Verified Aug-15-2016
              "ME4080": (["MTH2350", "ME3210"], ["MTH2330", "MTH2530", "ME3210"]),  # Verified Aug-16-2016
              "ME4120": (["MTH2320", "MTH2350", "ME3120"], ["MTH2320", "MTH2330", "MTH2530", "ME3120"]),
              "ME4140": (["ME2700", "ME3120"]),  # Verified Aug-16-2016
              "ME4150": ("ME4140"),  # Verified Aug-16-2016
              "ME4160": (["ME2020", "ME2210", "ME3120"], ["ME1040", "ME2210", "ME3120"]),
              "ME4180": ("ME2700"),  # Verified Aug-16-2016
              "ME4190": (["MTH2350", "MTH2320", "ME3350"], ["MTH2330", "MTH2530", "MTH2320", "ME3350"]),
              "ME4210": ("ME3210"),  # Verified Aug-16-2016
              "ME4220": ("ME3210"),
              "ME4240": ("ME2210"),  # Verified Aug-16-2016
              "ME4250": ("ME2210"),  # Verified Aug-16-2016
              "ME4260": (["MTH2350"], ["MTH2530", "MTH2530"]),
              "ME4330": ("ME3350"),  # Verified Aug-16-2016
              "ME4340": ("ME3360"),  # Verified Aug-16-2016
              "ME4350": ("ME3350"),  # Verified Aug-16-2016
              "ME4360": (["ME3320", "ME3350", "MTH2350"], ["ME3320", "ME3350", "MTH2530","MTH2330"]),
              "ME4430": ("ME3350"),  # Verified Aug-16-2016
              "ME4440": ("ME3350"),  # Verified Aug-16-2016
              "ME4490": ("ME3120"),  # Verified Aug-16-2016
              "ME4520": ("ME3350"),  # Verified Aug-16-2016
              "ME4530": ("ME3310"),  # Verified Aug-16-2016
              "ME4540": ("ME3360"),  # Verified Aug-16-2016
              "ME4550": ("ME3360"),  # Verified Aug-16-2016
              "ME4560": ("ME3350"),  # Verified Aug-16-2016
              "ME4570": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4580": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4590": ("ME3360"),  # Verified Aug-16-2016
              "ME4610": (["ME3360", "ME3600"]),  # Verified Aug-16-2016
              "ME4620": (["ME2700", "ME3120", "ME3600"]),
              "ME4680": (["CHM1210", "PHY2410"], ["CHM1210", "PHY1120"]),
              "ME4700": (["ME2700", "MTH2320", "MTH2350"],["ME2700", "MTH2320", "MTH2330", "MTH2530"]),
              "ME4720": ("ME2700"),  # Verified Aug-16-2016
              "ME4730": ("ME2700"),  # Verified Aug-16-2016
              "ME4740": (["ME2700", "ME3120", "ME4620c"]),
              "ME4750": (["ME2600", "ME2700"]),  # Verified Aug-16-2016
              "ME4770": (["ME2700", "ME3120"]),  # Verified Aug-16-2016
              "ME4820": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4830": ("ME2700"),  # Verified Aug-16-2016
              "ME4840": (["ME2700", "ME3120"]),  # Verified Aug-16-2016
              "ME4850": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4860": (["ME2700", "ME3120"]),  # Verified Aug-16-2016
              "ME4870": (["ME2210"], ["BME3212"], ["ISE3212"]),
              "ME4880": (["ME2700", "ME3310"], ["ME2700", "ME3750"]),
              "ME4910": (
              ["ME2020", "EGR3350", "MTH2320", "MTH2350", "PHY2410", "EE2010", "ME2210", "ME2700", "ME3120", "ME3310",
               "ME4620c"],["ME2020", "EGR3350", "MTH2320", "MTH2330", "MTH2530", "PHY2410", "EE2010", "ME2210", "ME2700", "ME3120", "ME3310",
               "ME4620c"]),
              "ME7060": (["ME6120", "ME7100"],["ME4120", "ME7100"]),
              "ME7080": (["ME6120", "ME7100"],["ME4120", "ME7100"]),
              "ME7120": ("ME4120","ME6120"),
              "ME7140": (["ME6120", "ME7100"],["ME4120", "ME7100"]),
              "ME7160": (["ME6120", "ME7100"],["ME4120", "ME7100"]),
#              "ME7200": ("ME5120"),
              "ME7210": ("ME4210","ME6210"),
#              "ME7250": ("ME5210"),
#              "ME7300": ("ME5350"),
              "ME7330": (),#"ME5360"
              "ME7340": ("ME4010","ME6010"),
#              "ME7350": ("ME5360"),
              "ME7390": ("ME7500"),
              "ME7400": ("ME4330","ME6330"),
              "ME7500": (),# ["ME5320", "ME5750"]
#              "ME7520": (["ME5310", "ME5750"]),
              "ME7550": ("ME7500"),
              "ME7690": ("ME4210","ME6210"),
              "ME7720": ("ME4720","ME6720"),#, "ME5750"
              "ME7730": ("ME4700","ME6700"),
              "ME7740": (),
              "ME7750": ("ME4700","ME6700"),
#              "ME7760": ("ME5760"),
              "ME7780": ("ME6730")}

#print(prereqdict)
import collections
#print(collections.OrderedDict(sorted(prereqdict.items())))
prereqdict = collections.OrderedDict(sorted(prereqdict.items()))

majordict = {"ME4910": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME2700": ['Engineering - IECS', 'Materials Sci + Egr - BSMSE', 'Materials Sci + Egr - IECS',
                        'Materials Sci + Egr - Pre',
                        'Mathematics - BS', 'Mech Engineering - BSME', 'Mech Engineering - IECS',
                        'Mech Engineering - Pre'],
             "ME3210": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME3320": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME3350": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME3360": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME3600": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME3610": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME3750": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME3760": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME3150": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4010": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4080": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4120": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4140": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4150": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4160": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4180": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4190": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4210": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4220": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4240": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4250": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4260": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4330": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4340": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4350": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4360": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4430": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4440": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4490": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4520": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4530": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4540": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4550": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4560": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4570": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4580": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4590": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4610": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4620": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4680": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4700": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4720": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4730": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4740": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE", 'Materials Sci + Egr - Pre'],
             "ME4750": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE",
                        'Materials Sci + Egr - Pre'],
             "ME4860": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE",
                        'Materials Sci + Egr - Pre'],
             "ME3870": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE",
                        'Materials Sci + Egr - Pre'],
             "ME4880": ["Mech Engineering - BSME", "Mech Engineering - Pre", "Materials Sci + Egr - BSMSE",
                        'Materials Sci + Egr - Pre']}
