import xlwings as xw
import pandas as pd

def create_excel_report(
    number_students_report: dict[str:pd.DataFrame],
    average_scores_data,
    pass_rates_report,
    pass_fail_dict_results,
    pie_charts
):
    n_rows = average_scores_data.shape[0]
    start_cell = 6
    end_row = start_cell + n_rows

    wb = xw.Book()
    app = xw.apps.active
    app.api.ActiveWindow.DisplayGridlines = False
    # try:
    #     sheet1 = wb.sheets['Hoja1']
    # except:
    #     sheet1 = wb.sheets['Sheet1']
    sheet1 = wb.add_worksheet('Summary Stats')
    # sheet1.set_tab_color('#E7E6E6')

    """
    2. Track-Level Summary Statistics 
    Compute and present: 
    - Total number of students per track 
    - Average subject scores - Average attendance and project scores 
    - Pass rates based on the designated "Passed (Y/N)" column
    """
    sheet1['E3'].value = number_students_report

    sheet1['E7'].value = average_scores_data['Fall']
    sheet1['E11'].value = average_scores_data['Spring']

    sheet1['K3'].value = pass_rates_report

    sheet1['E18'].value = pass_fail_dict_results

    pie1 = sheet1.pictures.add(
        pie_charts['Fall'],
        name='Pie plot',
        update=True,
        left=sheet1.range(f'E19').left,
        top=sheet1.range(f'E19').top
    )
    pie1.width = 400
    pie1.height = 400

    pie2 = sheet1.pictures.add(
        pie_charts['Spring'],
        name='Pie plot',
        update=True,
        left=sheet1.range(f'E30').left,
        top=sheet1.range(f'30').top
    )
    pie2.width = 400
    pie2.height = 400






