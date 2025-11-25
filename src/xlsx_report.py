import xlwings as xw
import pandas as pd

def one_year_excel_report(
    number_students_report: dict[str:pd.DataFrame],
    YEAR,
    average_scores_data,
    subject_averages,
    pass_rates_report,
    average_attendance,
    avg_project_Scores,
    pass_fail_dict_results,
    pie_charts,
    normalized_pass_rates,
    corr,
    fig_pairplot,
    math_plots,
    average_scores_by_income_plots,
    average_scores_by_income,
    output_report_route
):
    wb = xw.Book()
    app = xw.apps.active
    app.api.ActiveWindow.DisplayGridlines = False

    sheet1 = wb.sheets[0]
    """
    2. Track-Level Summary Statistics 
    Compute and present: 
    - Total number of students per track 
    - Average subject scores - Average attendance and project scores 
    - Pass rates based on the designated "Passed (Y/N)" column
    """

    sheet1.range('B1:K1').merge()
    sheet1.range("B1").value = f"{YEAR} EDHEC Summary Report"
    sheet1.range("B1").font.bold = True
    sheet1.range("B1").font.size = 20

    sheet1['B2'].value = '2.1 Total number of students'
    sheet1['B2'].api.Font.Bold = True
    sheet1['B3'].value = number_students_report

    sheet1['F2'].value = '2.2 Average grades'
    sheet1['F2'].api.Font.Bold = True
    sheet1['F3'].value = subject_averages

    sheet1['L2'].value = '2.3 Average subject scores; Fall Semester'
    sheet1['L2'].api.Font.Bold = True
    sheet1['L3'].value = average_scores_data['Fall']

    sheet1['R2'].value = '2.4 Average subject scores; Spring Semester'
    sheet1['R2'].api.Font.Bold = True
    sheet1['R3'].value = average_scores_data['Spring']

    sheet1['W2'].value = '2.5 Average Attendance'
    sheet1['W2'].api.Font.Bold = True
    sheet1['W3'].value = average_attendance

    sheet1['AA2'].value = '2.6 Average Project Scores by term'
    sheet1['AA2'].api.Font.Bold = True
    sheet1['AA3'].value = avg_project_Scores

    sheet1['AE2'].value = '2.7 Average Pass Rates'
    sheet1['AE2'].api.Font.Bold = True
    sheet1['AE3'].value = pass_rates_report

    ##########
    # pass_fail_dict_results

    ##########
    sheet1['B11'].value = '3.3 Correlation between attendance and project scores'
    sheet1['B11'].api.Font.Bold = True
    sheet1['B12'].value = 'Fall'
    sheet1['B12'].api.Font.Bold = True
    sheet1['B13'].value = corr['Fall']['Attendance (%)']

    sheet1['F12'].value = 'Fall'
    sheet1['F12'].api.Font.Bold = True
    sheet1['F13'].value = corr['Spring']['Attendance (%)']


    pairplot = sheet1.pictures.add(
            fig_pairplot,
            name='Pairplot',
            update=True,
            left=sheet1.range(f'B21').left,
            top=sheet1.range(f'B21').top
        )
    pairplot.width = 250
    pairplot.height = 250


    sheet1['L11'].value = '3.2 Average scores; History'
    sheet1['L11'].api.Font.Bold = True
    history_scores_fall = sheet1.pictures.add(
            math_plots['History']['Fall'],
            name='history_scores_fall',
            update=True,
            left=sheet1.range(f'L12').left,
            top=sheet1.range(f'L12').top
        )
    history_scores_fall.width = 350
    history_scores_fall.height = 250
    history_scores_spring = sheet1.pictures.add(
            math_plots['History']['Spring'],
            name='history_scores_spring',
            update=True,
            left=sheet1.range(f'L29').left,
            top=sheet1.range(f'L29').top
        )
    history_scores_spring.width = 350
    history_scores_spring.height = 250

    sheet1['V11'].value = '3.3 Average scores; Math'
    sheet1['V11'].api.Font.Bold = True
    math_scores_fall = sheet1.pictures.add(
            math_plots['Math']['Fall'],
            name='math_scores_fall',
            update=True,
            left=sheet1.range(f'V12').left,
            top=sheet1.range(f'V12').top
        )
    math_scores_fall.width = 350
    math_scores_fall.height = 250
    math_scores_spring = sheet1.pictures.add(
            math_plots['Math']['Spring'],
            name='math_scores_spring',
            update=True,
            left=sheet1.range(f'V29').left,
            top=sheet1.range(f'V29').top
        )
    math_scores_spring.width = 350
    math_scores_spring.height = 250
    ##########

    ##########

    ##########
    sheet1['B46'].value = '4.1 Passing Rates by track'
    sheet1['B46'].api.Font.Bold = True
    sheet1['B47'].value = normalized_pass_rates

    pie1 = sheet1.pictures.add(
        pie_charts['Fall'],
        name='Pie plot',
        update=True,
        left=sheet1.range(f'B59').left,
        top=sheet1.range(f'B59').top
    )
    pie1.width = 400
    pie1.height = 200


    pie2 = sheet1.pictures.add(
        pie_charts['Spring'],
        name='Pie plot 2',
        update=True,
        left=sheet1.range(f'B72').left,
        top=sheet1.range(f'B72').top
    )
    pie2.width = 400
    pie2.height = 200

    sheet1['O46'].value = '4.2 Average Grades by track'
    sheet1['O46'].api.Font.Bold = True
    avg_scores_fall = sheet1.pictures.add(
            average_scores_by_income_plots['Fall'],
            name='avg_scores_fall',
            update=True,
            left=sheet1.range(f'O47').left,
            top=sheet1.range(f'O47').top
        )
    avg_scores_fall.width = 350
    avg_scores_fall.height = 250

    avg_scores_spring = sheet1.pictures.add(
            average_scores_by_income_plots['Spring'],
            name='avg_scores_spring',
            update=True,
            left=sheet1.range(f'O65').left,
            top=sheet1.range(f'O65').top
        )
    avg_scores_spring.width = 350
    avg_scores_spring.height = 250

    sheet1['W47'].value = average_scores_by_income['Fall']
    sheet1['W65'].value = average_scores_by_income['Spring']

    wb.save(f'{output_report_route}/{YEAR}_summary_report.xlsx')

