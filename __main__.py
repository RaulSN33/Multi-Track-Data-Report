from src.report_initiator import report_initiator

input_route = 'Input'
output_data_route = 'Output/ConsolidatedData'
output_report_route = 'Output/SummaryReports'


report_initiator(
    input_route,
    output_data_route,
    output_report_route
)