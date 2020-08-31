import openpyxl

id_columns = 'b9', 'b9'
compare_column = 'I9', 'I9'

wb = openpyxl.load_workbook(filename='оборотно-сальдовая_июнь.xlsx')
sheet = wb['Report']
vals = [
    sheet['i8'].value,
    # sheet['i8'].value,
    '|',
    # sheet['i9'].value,
    sheet['i9'].value
]

print(vals)

# import xlrd, xlwt

# открываем файл
# rb = xlrd.open_workbook('оборотно-сальдовая_июнь.xlsx', formatting_info=True)

# выбираем активный лист
# sheet = rb.sheet_by_index(0)
