import pandas as pd

from api.get_info_from_fingercheck import api_call


def get_active_employees() -> pd.DataFrame:
    url_params = {
        'url': 'v1/Employees/GetAllActiveEmployees',
        'dtypes_': None,
        'add_division_id': 8048,
    }
    return api_call(url_params)


def get_all_schedules(selected_date_option) -> pd.DataFrame:
    selected_date = selected_date_option
    url_params = {
        'url': f'v1/Reports/GetSchedulesByDate?startDate={selected_date}&endDate={selected_date}',
        'dtypes_': None,
        'add_division_id': 8048,
    }
    return api_call(url_params)
