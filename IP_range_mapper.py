import os

from data_processing import *
from excel_editor import *

class DataMapper:
    def __init__(self, pre_file, map_file):
        self.pre_file = pre_file
        self.map_file = map_file

        self.pre_ws = read_excel(self.pre_file)
        self.map_ws = read_excel(self.map_file)
        self.column_list = ['院別', '單位別', 'SDOL Group', 'SDOL admin', 'SDOL start', 'SDOL end', '備註']
        self.clean_ws = self.load_clean_file()

        self.IP_dict = {}
        self.match_data = []

        self.get_IP_dict()
        self.sort_IP_dict()
        self.map_IP()

    def load_clean_file(self):
        clean_data = create_clean_data_list(self.column_list)
        clean_file = os.path.join(os.getcwd(), 'clean_file.xlsx')
        clean_data = get_clean_data(self.pre_ws, clean_data)
        save_to_excel(clean_file, clean_data)
        clean_ws = read_excel(clean_file)
        return clean_ws
    
    def get_IP_dict(self):
        ''' 
        return: nested dict with IP prefix as key, and the sub-dict as value including suffix as key and row index as value
        return combination of IP '140.116.1.*' with row index 6 and IP '140.116.1.141' with row index 7, dict = {'140.116.1': {'*': 6, '141': 7}}
        '''
        for i, row in enumerate(iter_rows(self.clean_ws), 1):
            if i==1 or row[4]==None: 
                continue

            prefix = re.match(r'(\d+\.\d+\.\d+)', row[4]).group(1)
            suffix = int(re.match(r'\d+\.\d+\.\d+\.(.*)', row[4]).group(1))
            
            try:
                if self.IP_dict[prefix]:
                    sub_dict = {suffix: i}
                    self.IP_dict[prefix].update(sub_dict)

            except KeyError:
                self.IP_dict[prefix] = {suffix: i}
    
    def sort_IP_dict(self):
        sorted_IP_dict = self.IP_dict

        for key, sub_dict in self.IP_dict.items():
            sub_keys = list(sub_dict.keys())
            sub_keys.sort()
            sorted_sub_dict = {i: sub_dict[i] for i in sub_keys}
            sorted_IP_dict[key] = sorted_sub_dict

        self.IP_dict = sorted_IP_dict

    def map_IP(self):
        '''
        Get prefix and suffix of every IP in map_ws to map the IP in IP_dict
        '''
        for i, row in enumerate(iter_rows(self.map_ws)):
            if i == 0:
                self.match_data.append(list(row))
                continue
        
            try:
                prefix = re.match(r'(\d+\.\d+\.\d+)', str(row[0])).group(1) # row[0]: IP start
                prefix = '.'.join([str(int(x)) for x in prefix.split('.')])
                suffix = int(re.match(r'\d+\.\d+\.\d+\.(.*)', str(row[0])).group(1))
                index = None # index of the matching row in pre_file

            except AttributeError:
                continue 

            try:
                for key, value in self.IP_dict[prefix].items():
                    if key == 255:
                        index = value
                        break

                    elif suffix >= key:
                        index = value

                    else:
                        break
                
                match_row = list((self.pre_ws['D'][index-1].value, self.pre_ws['A'][index-1].value, self.pre_ws['B'][index-1].value, self.pre_ws['C'][index-1].value))
                # print("{} -> {}".format(from_ws['D'][index-1].value, row[2])) 
                

            except (KeyError, TypeError) as e:
                match_row = ['查無比對資料']

            new_row = [cell for cell in row[:9]] + match_row
            # print(new_row)
            self.match_data.append(new_row)