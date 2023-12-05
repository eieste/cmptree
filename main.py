import helper
import components as cmp
from basecomponents import ElectricSignal as ES
import json
import plotly.express as px

# Ziel: Anzeige von ganzheitlichen "Netzen" with and without parent requirement

helper.show_tree_to_end(cmp.battery, "electric", ES.POWER_IN, )