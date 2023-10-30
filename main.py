from IP_range_mapper import DataMapper
from excel_editor import save_to_excel
import os

def main():
    pre_file = os.path.join(os.getcwd(), 'test file.xlsx')
    mapper = DataMapper(pre_file)
    save_to_excel('match_file.xlsx', mapper.match_data)
    
if __name__ == "__main__":
    main()