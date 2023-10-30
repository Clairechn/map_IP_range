from data_processing import *
from excel_editor import *
from IP_range_mapper import *

def test_iter_rows(test_ws):
    rows = list(iter_rows(test_ws))
    assert rows == [['院別', '單位別', 'SDOL Group', 'SDOL admin', 'SDOL start', 'SDOL end', '備註'], ['a', 'a1', 415690, '120.114.240.(2-255)', None, None, None], ['b', 'b1', 415691, '120.114.241.*-120.114.241.255', None, None, None], ['c', 'c1', 415692, '140.116.167.0\n140.116.167.(15-16)', None, None, None]], "test_iter_rows() failed"

def test_split_multi_IP():
    row = ['c', 'c1', 415692, '140.116.167.0\n140.116.167.(15-16)', None, None, None]
    rows = split_multi_IP(row)

def test_split_start_end_IP():
    row1 = ['a', 'a1', 415690, '120.114.240.(2-255)', None, None, None]
    row2 = ['b', 'b1', 415691, '120.114.241.*-120.114.241.255', None, None, None]

    clean_row1 = split_start_end_IP(row1)
    clean_row2 = split_start_end_IP(row2)

    assert clean_row1 == ['a', 'a1', 415690, '120.114.240.(2-255)', '120.114.240.2', '120.114.240.255', None] and clean_row2 == ['b', 'b1', 415691, '120.114.241.*-120.114.241.255', '120.114.241.255', '120.114.241.255', None]

def test_create_clean_data_list(test_column_list):
    test_clean_data = create_clean_data_list(test_column_list)
    assert test_clean_data == [['院別', '單位別', 'SDOL Group', 'SDOL admin', 'SDOL start', 'SDOL end', '備註']], "test_create_clean_data_list() failed"

def test_get_clean_data(test_ws, test_clean_data):
    clean_ws = get_clean_data(test_ws, test_clean_data)
    # print("clean_ws:", clean_ws)    

def test_data_mapper(test_file):
    mapper = DataMapper(test_file)

if __name__ == "__main__":
    # test iter_rows()
    test_ws = read_excel('test file.xlsx')
    test_iter_rows(test_ws)

    # test split_multi_IP()
    test_split_multi_IP()

    # test split_start_end_IP()
    test_split_start_end_IP()

    # test creat_clean_data_list()
    column_list = ['院別', '單位別', 'SDOL Group', 'SDOL admin', 'SDOL start', 'SDOL end', '備註']
    test_create_clean_data_list(column_list)

    # test get_clean_data()
    test_clean_data = create_clean_data_list(column_list)   
    test_get_clean_data(test_ws, test_clean_data)

    # test DataMapper()
    test_data_mapper('test file.xlsx')
