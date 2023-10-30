import openpyxl

def read_excel(filepath, ws_name=None):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    if ws_name is None:
        ws = wb.worksheets[0]
    else:
        ws = wb[ws_name]
    return ws

def save_to_excel(filepath, data_list):
    new_wb = openpyxl.Workbook()
    new_ws = new_wb.active

    for row in data_list:
        new_ws.append(row)

    new_wb.save(filepath)