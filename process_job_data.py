from export_to_pdf import export_to_pdf

def process_job_data(df, selected_date_option, jobs_manager):
    grouped_job = df.groupby('Job_x')
    for job, group in grouped_job:
        total_rows = len(group) - 1  # Subtract 1 to exclude the 'Total' row
        group.loc['Total', 'LastFirst'] = ''
        group.loc['Total', 'StartDate'] = ''
        group.loc['Total', 'Job_x'] = ''
        group.loc['Total', 'CostCenter2_x'] = ''
        group.loc['Total', 'Task_x'] = total_rows

        pdf_filename = f"{jobs_manager.get_job_name(job)}.pdf"
        filtered_group = group[['LastFirst', 'StartDate', 'Job_x', 'Task_x', 'CostCenter2_x']].copy()
        export_to_pdf(filtered_group[:-1], pdf_filename, selected_date_option)
