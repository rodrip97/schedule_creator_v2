from fpdf import FPDF
import pandas as pd
import os


def export_to_pdf(df, filename, selected_date_option):
    selected_date = selected_date_option

    # Check if the DataFrame is empty
    if df.empty:
        print("DataFrame is empty. No data to export to PDF.")
        return

    # Sort the DataFrame first by 'Task_x' and then by 'LastFirst'
    df = df.sort_values(by=['Task_x', 'LastFirst','StartDate'])

    total_rows = len(df)
    df_with_total = pd.concat(
        [df, pd.DataFrame(
            [{'LastFirst': 'Total', 'StartDate': '', 'Task_x': '', 'Job_x': '', 'CostCenter2_x': total_rows}])],
        ignore_index=True)
    df_with_total['Task_x'] = df_with_total['Task_x'].astype(str)
    df_with_total = df_with_total.sort_values('Task_x')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=10)

    pdf.cell(100, 5, f'Schedule for {selected_date}')
    pdf.ln()
    pdf.ln()

    job_stage = df['CostCenter2_x'].iloc[0]
    job_address = df['Job_x'].iloc[0]

    pdf.cell(60, 5, str(f'Job Stage: {job_stage}'), border=0)
    pdf.cell(100, 5, str(f'Job Address: {job_address}'), border=0)
    pdf.ln()

    pdf.cell(60, 5, str('Name'), border=1)
    pdf.cell(25, 5, str('Start Time'), border=1)
    pdf.cell(30, 5, str('Task'), border=1)
    pdf.cell(20, 5, str('Time In'), border=1)
    pdf.cell(20, 5, str('Sign'), border=1)
    pdf.cell(20, 5, str('Time Out'), border=1)
    pdf.cell(20, 5, str('Sign'), border=1)

    pdf.ln()

    for index, row in df.iterrows():
        pdf.cell(60, 10, str(row['LastFirst']), border=1)

        start_time = pd.to_datetime(row['StartDate']).strftime('%I:%M%p')
        pdf.cell(25, 10, str(start_time), border=1)
        pdf.cell(30, 10, str(row['Task_x']), border=1)
        pdf.cell(20, 10, '', border=1)
        pdf.cell(20, 10, '', border=1)
        pdf.cell(20, 10, '', border=1)
        pdf.cell(20, 10, '', border=1)
        pdf.ln()

    pdf.set_font('Arial', size=10, style='B')
    pdf.cell(60, 10, str(df_with_total.loc[df_with_total['LastFirst'] == 'Total', 'LastFirst'].values[0]), border=1)
    pdf.cell(25, 10, '', border=1)
    pdf.cell(30, 10, '', border=1)
    pdf.cell(20, 10, '', border=1)
    pdf.cell(20, 10, '', border=1)
    pdf.cell(20, 10, '', border=1)
    pdf.cell(20, 10, str(total_rows), border=1)
    pdf.ln()

    folder_path = os.path.join(os.getcwd(), 'schedules')
    os.makedirs(folder_path, exist_ok=True)

    pdf.output(os.path.join(folder_path, filename))
