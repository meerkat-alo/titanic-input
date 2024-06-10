#asset_[step_name].py
 
# -*- coding: utf-8 -*-
import os
import sys
from alolib.asset import Asset
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd 
 
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
        sub_dir = os.listdir(base_input_path)
        assert len(sub_dir) == 1
        input_path = base_input_path + sub_dir[0] + '/'
        for idx, input_file in enumerate(os.listdir(input_path)):
            df = pd.read_csv(input_path + input_file)
            self.data[f'dataframe{idx}'] = df
            self.asset.save_info(f"Loaded dataframe{idx}") # info logging

        self.config['x_columns'] = self.args['x_columns']
        self.config['y_column'] = self.args['y_column']
            
        self.asset.save_data(self.data) # to next asset
        self.asset.save_config(self.config) # to next asset
 
#--------------------------------------------------------------------------------------------------------------------------
#    MAIN
#--------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    envs, argv, data, config = {}, {}, {}, {}
    ua = UserAsset(envs, argv, data, config)
    ua.run()
