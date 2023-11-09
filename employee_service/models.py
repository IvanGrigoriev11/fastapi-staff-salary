from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Employee:
    username: str
    salary: float
    salary_increase_date: date


@dataclass(frozen=True)
class SalaryResponse:
    salary: float
    salary_increase_date: date
