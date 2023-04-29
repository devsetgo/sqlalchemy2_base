# -*- coding: utf-8 -*-

# Import necessary modules
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


# Import custom modules
from datetime import datetime
from enum import Enum


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
