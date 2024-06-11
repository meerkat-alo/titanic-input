#asset_[step_name].py
 
# -*- coding: utf-8 -*-
import os
import sys
from alolib.asset import Asset
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd  
from pathlib import Path
#--------------------------------------------------------------------------------------------------------------------------
#    CLASS
#--------------------------------------------------------------------------------------------------------------------------
class UserAsset(Asset):
    def __init__(self, asset_structure):
        super().__init__(asset_structure)
        self.args       = self.asset.load_args() # experimental_plan.yaml args
        self.config     = self.asset.load_config() # asset - asset interface config
        self.data       = {} # asset - asset interface data
 
    @Asset.decorator_run
    def run(self):
        # alolib API : self.asset.~~~() 
        base_input_path = self.asset.get_input_path() 
        csv_list = find_csv_files(base_input_path)
        assert len(csv_list) == 1
        self.asset.save_info(f'input csv files: {csv_list}')        
        for idx, input_file in enumerate(csv_list):
            df = pd.read_csv(input_file)
            self.data[f'dataframe{idx}'] = df
            self.asset.save_info(f"Loaded dataframe{idx}") # info logging
            self.asset.save_info(f'read dataframe from <<< {input_file}')
        self.config['x_columns'] = self.args['x_columns']
        self.config['y_column'] = self.args['y_column']
            
        self.asset.save_data(self.data) # to next asset
        self.asset.save_config(self.config) # to next asset

def find_csv_files(root_dir):
    root_path = Path(root_dir)
    return list(root_path.rglob('*.csv'))

#--------------------------------------------------------------------------------------------------------------------------
#    MAIN
#--------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    envs, argv, data, config = {}, {}, {}, {}
    ua = UserAsset(envs, argv, data, config)
    ua.run()
