from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class SalaryRecord(BaseModel):

    company: str

    company_slug: str

    role: str

    level_standardized: Literal[
        "L3",
        "L4",
        "L5",
        "L6",
        "SDE-I",
        "SDE-II",
        "SDE-III",
        "Staff",
        "Principal",
        "IC4",
        "IC5",
        "Unknown"
    ]

    location: str

    currency: Literal[
        "INR",
        "USD",
        "GBP",
        "EUR"
    ]

    experience_years: float

    base_salary: int

    bonus: int = 0

    stock: int = 0

    source: Literal[
        "SCRAPED",
        "CONTRIBUTOR",
        "AI_INFERRED"
    ]

    confidence_score: float = Field(
        ge=0.0,
        le=1.0
    )

    

    @field_validator("company")
    @classmethod
    def validate_company(cls, value):

        if len(value.strip()) < 2:
            raise ValueError(
                "Company must contain at least 2 characters."
            )

        return value

    @field_validator("experience_years")
    @classmethod
    def validate_experience(cls, value):

        if value < 0 or value > 50:
            raise ValueError(
                "Experience must be between 0 and 50."
            )

        return value

    @field_validator("base_salary")
    @classmethod
    def validate_salary(cls, value):

        if value <= 0:
            raise ValueError(
                "Base salary must be positive."
            )

        return value