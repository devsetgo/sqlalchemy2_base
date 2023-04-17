# -*- coding: utf-8 -*-

# Import necessary modules
import io
import tracemalloc
from datetime import date, datetime, timedelta
from typing import Dict, List, Union, Optional
from cpuinfo import get_cpu_info_json
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import ORJSONResponse
from loguru import logger
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List
from sqlalchemy.exc import IntegrityError

# Import custom modules
from service.core.http_codes import SYSTEM_INFO_CODE
from service.core.process_checks import get_processes
from service.settings import config_settings
from service.database.user_model import User
from service.core.user_lib import encrypt_pass, verify_pass
from datetime import datetime, timedelta
from enum import Enum


# Create an instance of APIRouter
router = APIRouter()


class UserSchema(BaseModel):
    """
    A Pydantic model representing a user.

    Attributes:
    -----------
    first_name : str
        The first name of the user.
    last_name : str
        The last name of the user.
    email : EmailStr
        The email address of the user.
    notes : str, optional
        Any additional notes about the user.
    password : str
        The password for the user's account.
    password_two : str
        A confirmation of the user's password.

    Methods:
    --------
    passwords_match(cls, v, values, **kwargs) -> str:
        A validator method that checks if the two password fields match.

    """

    # Define the attributes of the UserSchema model
    first_name: str = Field(
        ..., alias="firstName", min_length=1, max_length=50, example="John"
    )
    last_name: str = Field(
        ..., alias="lastName", min_length=1, max_length=50, example="Doe"
    )
    email: EmailStr = Field(..., alias="email", example="jdoe@example.com")
    notes: str = Field(None, alias="notes", max_length=5000, example="A bunch of words")
    password: str = Field(
        ..., alias="password", min_length=5, max_length=50, example="NotLetMeIn123"
    )
    password_two: str = Field(
        ..., alias="passwordTwo", min_length=5, max_length=50, example="NotLetMeIn1234"
    )

    @validator("password_two")
    def passwords_match(cls, v, values, **kwargs) -> str:
        """
        A Pydantic validator method that checks if the two password fields match.

        Parameters:
        -----------
        cls : UserSchema
            The UserSchema class.
        v : str
            The value of the password_two field.
        values : dict
            A dictionary containing all the field values of the model.
        **kwargs : Any
            Any additional keyword arguments.

        Returns:
        --------
        str
            The value of the password_two field if it matches the password field.

        Raises:
        -------
        ValueError
            If the password_two field does not match the password field.

        """

        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class UserSerializer(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    date_created: datetime
    date_updated: datetime

    # full_name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123",
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "full_name": "John Doe",
            }
        }



@router.post("/", response_model=UserSerializer)
async def create_user(user: UserSchema):
    values = user.dict()

    hash_pwd = encrypt_pass(values["password"])

    values["password"] = hash_pwd
    values.pop("password_two")
    values["email"] = str(values["email"]).lower()

    try:
        user = await User.create(**values)
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email address already exists")


@router.get("/{id}", response_model=UserSerializer)
async def get_user(id: str):
    user = await User.get(id)
    return user


class DaysEnum(str, Enum):
    """
    An enumeration of time periods in days.

    Attributes:
        LAST_7_DAYS (str): A string representation of 7 days.
        LAST_14_DAYS (str): A string representation of 14 days.
        LAST_30_DAYS (str): A string representation of 30 days.
        LAST_60_DAYS (str): A string representation of 60 days.
        LAST_90_DAYS (str): A string representation of 90 days.
        LAST_180_DAYS (str): A string representation of 180 days.
        LAST_365_DAYS (str): A string representation of 365 days.
        LAST_731_DAYS (str): A string representation of 731 days.
    """

    LAST_7_DAYS = "7"
    LAST_14_DAYS = "14"
    LAST_30_DAYS = "30"
    LAST_60_DAYS = "60"
    LAST_90_DAYS = "90"
    LAST_180_DAYS = "180"
    LAST_365_DAYS = "365"
    LAST_731_DAYS = "731"


# Example usage:
# You can use the enumeration values to represent time periods in your code.
# For example, if you want to filter data based on the last 30 days, you can use:
# DaysEnum.LAST_30_DAYS


@router.get("/", response_model=dict)
async def get_all_users(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    notes: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_approved: Optional[bool] = None,
    created_days: Optional[DaysEnum] = None,
    updated_days: Optional[DaysEnum] = None,
):
    """
    Retrieve a list of users based on the provided filters.

    Args:
        first_name (Optional[str]): Filter by first name.
        last_name (Optional[str]): Filter by last name.
        email (Optional[str]): Filter by email address.
        notes (Optional[str]): Filter by user notes.
        is_active (Optional[bool]): Filter by active status.
        is_approved (Optional[bool]): Filter by approval status.
        created_days (Optional[DaysEnum]): Filter by date created within the specified number of days.
        updated_days (Optional[DaysEnum]): Filter by date updated within the specified number of days.

    Returns:
        dict: A dictionary containing the total count of users and the filtered list of users.

    Example:
        To retrieve all users with the first name "John" and the last name "Doe", make a GET request to "/?first_name=John&last_name=Doe".
    """

    # Create an empty dictionary to hold the filters
    filters = {}

    # Add filters to the dictionary if they are provided
    if first_name:
        filters["first_name"] = first_name
    if last_name:
        filters["last_name"] = last_name
    if email:
        filters["email"] = email
    if notes:
        filters["notes"] = notes
    if is_active is not None:
        filters["is_active"] = is_active
    if is_approved is not None:
        filters["is_approved"] = is_approved

    # Add a filter for date created within the specified number of days
    if created_days:
        days_ago = datetime.utcnow() - timedelta(days=int(created_days.value))
        filters["date_created"] = days_ago

    # Add a filter for date updated within the specified number of days
    if updated_days:
        try:
            days_ago = datetime.utcnow() - timedelta(days=int(updated_days.value))
            filters["date_updated"] = days_ago
        except ValueError:
            logger.error("Invalid value for 'updated_days'")
            return {"error": "Invalid value for 'updated_days'"}

    # Retrieve users based on the provided filters
    users = await User.get_all(filters=filters)

    # Retrieve the total count of users
    total_user = await User.get_all()

    # Create a dictionary containing the total count of users and the filtered list of users
    results = {
        "parameters": {
            "total_count": len(total_user),
            "result_count": len(users),
            "filters": filters,
        },
        "users": users,
    }

    # Log the number of users retrieved and the filters used
    logger.info(f"Retrieved {len(users)} users with filters: {filters}")

    # Return the results
    return results


class UserUpdateSchema(BaseModel):
    # Define the attributes of the UserSchema model
    first_name: str = Field(
        ..., alias="firstName", min_length=1, max_length=50, example="John"
    )
    last_name: str = Field(
        ..., alias="lastName", min_length=1, max_length=50, example="Doe"
    )
    email: EmailStr = Field(..., alias="email", example="jdoe@example.com")
    notes: str = Field(None, alias="notes", max_length=5000, example="A bunch of words")

@router.put("/{id}", response_model=UserSerializer)
async def update(id: str, user: UserUpdateSchema):
    user = await User.update(id, **user.dict())
    return user


@router.delete("/{id}", response_model=bool)
async def delete_user(id: str):
    return await User.delete(id)
