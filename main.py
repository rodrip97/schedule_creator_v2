import os
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from tkcalendar import DateEntry
from api_calls import get_all_schedules, get_active_employees
from export_to_pdf import export_to_pdf
from jobs import JobsManager
from process_job_data import process_job_data


def main():
    jobs_manager = JobsManager(jobs_file='jobs.json')
    jobs_manager.load_jobs()
    delete_button = None

    # UI Functions
    def filter_and_export_df(df, task_filter, filename, selected_date_option):
        filtered_df = df.loc[
            (df['Job_x'].notnull()) &
            (df['CostCenter2_x'].notnull()) &
            (df['StartDate'].notnull()) &
            (df['Task_x'].isin(task_filter)),
            ['LastFirst', 'StartDate', 'Job_x', 'Task_x', 'CostCenter2_x']
        ]
        export_to_pdf(filtered_df, filename, selected_date_option)

    def generate_reports_clicked():
        selected_date_option = selected_date.get_date().strftime('%m-%d-%Y')
        today_schedule = get_all_schedules(selected_date_option)

        active_employees = get_active_employees()
        print(f"active_employees -> {active_employees}")
        today_schedule['unique'] = today_schedule.apply(lambda x: f"{x['EmployeeNumber']}<%%>{x['division_id']}", axis=1)
        active_employees['unique'] = active_employees.apply(lambda x: f"{x['EmployeeNumber']}<%%>{x['division_id']}",
                                                            axis=1)
        merged_df = pd.merge(today_schedule, active_employees, on='unique', how='inner')

        process_job_data(merged_df, selected_date_option, jobs_manager)

        # Show pop-up message
        messagebox.showinfo("Reports Generated",
                            "Reports have been generated successfully! \n Please check Schedules folder.")

    def open_schedule_directory():
        schedule_directory = os.path.join(os.getcwd(), 'schedules')
        os.makedirs(schedule_directory, exist_ok=True)
        os.startfile(schedule_directory)

    def show_jobs():
        global delete_button
        jobs = jobs_manager.get_jobs()
        job_list_var.set(list(jobs.items()))

        paned_window = ttk.Panedwindow(root, orient=HORIZONTAL)
        paned_window.grid(row=0, column=0, padx=10, pady=10, sticky=N + S)

        list_frame = ttk.Frame(paned_window, width=200)
        list_box = Listbox(list_frame, selectmode=MULTIPLE, listvariable=job_list_var)

        for (job_code, job_name) in jobs.items():
            list_box.insert(END, f"{job_code}: {job_name}")

        list_box.pack(expand=YES, fill=BOTH)
        paned_window.add(list_frame)

        select_all_button = ttk.Button(root, text="Select All", command=lambda: list_box.selection_set(0, END))
        select_all_button.grid(row=1, column=0, padx=10, pady=5, sticky=N)

        select_none_button = ttk.Button(root, text='Unselect All', command=lambda: list_box.selection_clear(0, END))
        select_none_button.grid(row=2, column=0, padx=10, pady=5, sticky=N)

        delete_button = ttk.Button(root, text='Delete', command=delete_selected_jobs)
        delete_button.grid(row=3, column=0, padx=10, pady=5, sticky=N)
        delete_button.config(state=NORMAL if jobs else DISABLED)

        return list_box

    def add_job():
        job_code = simpledialog.askstring('Add Job', 'Enter Job Code:')
        if job_code:
            job_name = simpledialog.askstring("Job Name", "Add Job Name")
            if job_name:
                jobs_manager.add_job(job_code, job_name)
                messagebox.showinfo('Success', 'Job Added.')
                # Trigger a refresh after adding a job
                refresh_job_list()

    def delete_selected_jobs():
        selected_items = list_box.curselection()
        if selected_items:
            for index in selected_items[::-1]:
                item = list_box.get(index)
                if isinstance(item, tuple):
                    item_text = item[0]
                else:
                    item_text = item

                # Split item_text only if ':' is present
                if ':' in item_text:
                    job_code, job_name = item_text.split(':', 1)
                    jobs_manager.remove_job(job_code)

            refresh_job_list()

    def refresh_job_list():
        list_box.delete(0, END)
        for job_code, job_name in jobs_manager.get_jobs().items():
            list_box.insert(END, f"{job_code}: {job_name}")

        # Save the updated job list to the JSON file
        jobs_manager.save_jobs_to_file()

    # Tkinter UI setup
    root = Tk()
    root.title("Employee Schedule Reports")
    root.geometry("350x300")

    job_list_var = StringVar(root)

    # Frame for job list
    job_frame = ttk.Frame(root)
    job_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N)

    # Label for the job list
    job_list_label = ttk.Label(job_frame, text="Job List:")
    job_list_label.grid(row=0, column=0, padx=10, pady=5, sticky=W, columnspan=2)

    # Display job list
    list_box = show_jobs()
    job_list_var.set(list(jobs_manager.get_jobs().items()))

    # Frame for date selection and buttons
    control_frame = ttk.Frame(root)
    control_frame.grid(row=0, column=1, padx=10, pady=10, sticky=N,columnspan=2)

    # Label for selecting date
    selected_date_label = ttk.Label(control_frame, text="Select Date:")
    selected_date_label.grid(row=0, column=0, pady=5, sticky=W)

    # DateEntry for date selection
    selected_date = DateEntry(control_frame, width=12, background='darkblue', foreground='white', borderwidth=2, dropdown=False)
    selected_date.grid(row=0, column=1, pady=5, sticky=W)

    # Button to generate reports
    generate_reports_button = ttk.Button(control_frame, text="Generate Reports", command=generate_reports_clicked)
    generate_reports_button.grid(row=1, column=1, columnspan=2, pady=5)

    # Button to add jobs
    add_job_button = ttk.Button(control_frame, text='Add Job', command=add_job)
    add_job_button.grid(row=2, column=1, pady=5, sticky=W)

    # Button to open schedule directory
    open_directory_button = ttk.Button(control_frame, text='View Schedule', command=open_schedule_directory)
    open_directory_button.grid(row=3, column=1, pady=5,  sticky=W)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()


