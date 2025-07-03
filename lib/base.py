from dataclasses import dataclass
from select import select
import toml

@dataclass
class Base:
    config_location = "lib/configs"
    base_configs = toml.load(f"{config_location}/configs.toml")
    output_file = "testing.py"
    ## all the columns that are available
    ## and that is to be added here
    all_cols = ["None", 'close', 'open', 'high', 'low', 'volume']

    hashtag = '######################'

    ## selected indicators
    ## all values are stored here
    indicators_all_values = {}
    
    ## selected indicators
    ## only names are stored here
    indicators_names = {}

    ## input cols list
    ## high low close volume open
    ## only saved here
    input_col_list = []

    ## selected indicators libraries
    indicators_lib = []
    
    ## selected charting library
    charting_lib = None

    
