# ApplicantProfile & ApplicationDetail tables

from .database import execute_query, fetch_all

def create_tables():
    pass

def insert_applicant_profile(name: str, email: str, phone: str):
    pass

def insert_application_detail(applicant_id: int, job_id: int, status: str):
    pass

def fetch_all_cvs():
    pass

def fetch_applicant_by_id(applicant_id: int):
    pass