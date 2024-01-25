import pandas as pd
import json


class JobsManager:
    def __init__(self, jobs_file="jobs.json"):
        self.jobs_file = jobs_file
        self.jobs = self.load_jobs()

    def load_jobs(self):
        try:
            with open(self.jobs_file, 'r') as file:
                jobs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            jobs = {}
            self.save_jobs()
        return jobs

    def save_jobs(self):
        try:
            with open(self.jobs_file, 'w') as file:
                json.dump(self.jobs, file)
        except Exception as e:
            print(f"Error saving jobs: {e}")

    def get_jobs(self):
        return self.jobs

    def add_job(self, job_code, job_name):
        self.jobs[job_code] = job_name
        self.save_jobs()

    def remove_job(self, job_code):
        if job_code in self.jobs:
            del self.jobs[job_code]

    def get_job_name(self, job_code):
        return self.jobs.get(job_code, job_code)

    def save_jobs_to_file(self):
        with open(self.jobs_file, 'w') as file:
            json.dump(self.jobs, file)