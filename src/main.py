import pandas as pd
import re
from pathlib import Path

file_loc = Path.cwd() / 'data' / 'sample-report.txt'

def parser(file_loc):
    with open(file_loc, 'r') as file:
        content = list(file)
    
    def levels(level):
        try:
            row_text = row[curr_val_start:curr_val_end].strip()
            d[key][f'current_{level}_price'] = float(row_text)
        except ValueError:
            if row_text != '':
                print(f'exception for current {level} price in {key, row_text}')
            pass
        d[key][f'current_{level}_basis'] = row[curr_basis_start:curr_basis_end]
        try:
            row_text = row[curr_mult_start:curr_mult_end].strip()
            d[key][f'current_{level}_mult'] = float(row_text)
        except ValueError:
            if row_text != '':
                print(f'exception for current {level} mult in {key, row_text}')
            pass
        try:
            row_text = row[sugg_val_start:sugg_val_end].strip()
            d[key][f'sugg_{level}_price'] = float(row_text)
        except ValueError:
            if row_text != '':
                print(f'exception for suggested {level} price in {key, row_text}')
            pass
        d[key][f'sugg_{level}_basis'] = row[sugg_basis_start:sugg_basis_end]
        try:
            row_text = row[sugg_mult_start:sugg_mult_end].strip()
            d[key][f'sugg_{level}_mult'] = float(row_text)
        except ValueError:
            if row_text != '':
                print(f'exception for suggested {level} mult in {key, row_text}')
            pass  
    
    
    d = {}

    # define the start and stop file_locations in the row where the hard coded values reside for all price points
    curr_val_start = 46
    curr_val_end = 56
    curr_basis_start = 33
    curr_basis_end = 35
    curr_mult_start = 35
    curr_mult_end = 46

    sugg_val_start = 92
    sugg_val_end = 102
    sugg_basis_start = 79
    sugg_basis_end = 81
    sugg_mult_start = 81
    sugg_mult_end = 92


    for row in content:
        if re.search('Item:', row):
            # capture the item num from the row
            item_num = row[6:27].strip()
            # capture the item description for the row
            item_desc = row[27:58].strip()
            # capture effective date for the row
            eff_dte = row[67:75]

            # populate dictionary entry
            key = item_num

            d[key] = {'item_desc':item_desc, 'eff_dte':eff_dte}     

        elif re.search('List Price', row):
            d[key]['current_list_price'] = float(row[curr_val_start:curr_val_end].strip())
            d[key]['sugg_list_price'] = float(row[sugg_val_start:sugg_val_end].strip())   

        elif re.search('Manual Cost', row):
            d[key]['current_manual_cost'] = float(row[curr_val_start:curr_val_end].strip())
            d[key]['sugg_manual_cost'] = float(row[sugg_val_start:sugg_val_end].strip())

        elif re.search('Standard Price', row):
            try:
                row_text = row[curr_val_start:curr_val_end].strip()
                d[key]['current_standard_price'] = float(row_text)     
            except ValueError:
                if row_text != '':
                    print(f'exception for current standard price in {key, row_text}')
                pass
            d[key]['current_basis'] = row[curr_basis_start:curr_basis_end]
            try:
                row_text = row[curr_mult_start:curr_mult_end].strip()
                d[key]['current_mult'] = float(row_text)
            except ValueError:
                if row_text != '':
                    print(f'exception for current multiplier in {key, row_text}')
                pass
            d[key]['sugg_standard_price'] = float(row[sugg_val_start:sugg_val_end].strip())
            d[key]['sugg_basis'] = row[sugg_basis_start:sugg_basis_end]
            try:
                row_text = row[sugg_mult_start:sugg_mult_end].strip()
                d[key]['sugg_mult'] = float(row_text)
            except ValueError:
                if row_text != '':
                    print(f'exception for suggested multiplier in {key, row_text}')
                pass


        elif re.search('Price Level 1', row):
            levels('l1')

        elif re.search('                  2              ', row):
            levels('l2')

        elif re.search('                  3              ', row):
            levels('l3')

        elif re.search('                  4              ', row):
            levels('l4')

        elif re.search('                  5              ', row):
            levels('l5')

        elif re.search('                  6              ', row):
            levels('l6')

    # translate to dataframe
    df = pd.DataFrame().from_dict(d, orient='index').reset_index()
    
    return df

if __name__ == '__main__':
    parser(file_loc)