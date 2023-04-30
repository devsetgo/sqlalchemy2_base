# -*- coding: utf-8 -*-

# Import necessary modules
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Query, Body
from loguru import logger
from sqlalchemy.exc import IntegrityError

from service.core.user_lib import encrypt_pass
# Import custom modules
from service.database.user_model import User
from service.models.users import DaysEnum, UserSchema, UserSerializer, UserUpdateSchema,UserQuery

# Create an instance of APIRouter
router = APIRouter()


# API Route located at /api/v1/user/
@router.get("/list", response_model=dict)
async def get_all_users(
    user_name: Optional[str] = Query(None),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    notes: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_approved: Optional[bool] = Query(None),
    created_days: Optional[DaysEnum] = Query(None),
    updated_days: Optional[DaysEnum] = Query(None),
    limit: Optional[int] = Query(None, ge=0,le=1000),
    offset: Optional[int] = Query(None, ge=0, le=1000000000),
):
    """
    Retrieve a list of users based on the provided filters.

    Args:
        user_name (Optional[str]): The username to filter by.
        first_name (Optional[str]): The first name to filter by.
        last_name (Optional[str]): The last name to filter by.
        email (Optional[str]): The email address to filter by.
        notes (Optional[str]): Notes to filter by.
        is_active (Optional[bool]): Whether the user is active or not.
        is_approved (Optional[bool]): Whether the user is approved or not.
        created_days (Optional[DaysEnum]): The number of days since the user was created.
        updated_days (Optional[DaysEnum]): The number of days since the user was last updated.
        limit (Optional[int]): The maximum number of results to return.
        offset (Optional[int]): The number of results to skip before returning.

    Returns:
        dict: A dictionary containing the total count of users and the filtered list of users.

    Example:
        To retrieve all users with the first name "John" and the last name "Doe", make a GET request to "/?first_name=John&last_name=Doe".
    """

    # Create an empty dictionary to hold the filters
    filters = {}

    # Add filters to the dictionary if they are provided
    if user_name is not None:
        filters["user_name"] = user_name
    if first_name is not None:
        filters["first_name"] = first_name
    if last_name is not None:
        filters["last_name"] = last_name
    if email is not None:
        filters["email"] = email
    if notes is not None:
        filters["notes"] = notes
    if is_active is not None:
        filters["is_active"] = is_active
    if is_approved is not None:
        filters["is_approved"] = is_approved

    # Add a filter for date created within the specified number of days
    if created_days is not None:
        try:
            days_ago = datetime.utcnow() - timedelta(days=int(created_days.value))
            filters["date_created"] = days_ago
        except ValueError:
            logger.error("Invalid value for 'created_days'")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid value for 'created_days'",
            )
    # Add a filter for date updated within the specified number of days
    if updated_days is not None:
        try:
            days_ago = datetime.utcnow() - timedelta(days=int(updated_days.value))
            filters["date_updated"] = days_ago
        except ValueError:
            logger.error("Invalid value for 'updated_days'")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid value for 'updated_days'",
            )

    if offset is None:
        offset = 0
    if limit is None:
        limit = 500

    # Retrieve users based on the provided filters
    users = await User.list_all(filters=filters, limit=limit, offset=offset)

    # Retrieve the total count of users
    total_user = await User.count_all(filters=filters)

    # Create a dictionary containing the total count of users and the filtered list of users
    results = {
        "query_data": {
            "total_count": total_user,
            "result_count": len(users),
            "limit":limit,"offset":offset,
            "filters": filters,
        },
        "users": users,
    }

    # Log the number of users retrieved and the filters used
    logger.info(f"Retrieved {len(users)} users with filters: {filters}")

    # Return the results
    return results

# API Route located at /api/v1/user/
@router.get("/id/{id}", response_model=UserSerializer)
async def get_user(id: str):
    user = await User.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# API Route located at /api/v1/user/
@router.post("/create", response_model=UserSerializer)
async def create_user(user: UserSchema):
    values = user.dict()
    values["user_name"] = str(values["user_name"]).lower()
    hash_pwd = encrypt_pass(values["password"])
    values["password"] = hash_pwd
    values.pop("password_two")
    values["email"] = str(values["email"]).lower()

    try:
        user = await User.create(**values)
        return user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email address already exists")


# API Route located at /api/v1/user/
@router.put("/id/{id}", response_model=UserSerializer)
async def update(id: str, user: UserUpdateSchema):
    user = await User.update(id, **user.dict())
    return user


# /api/v1/user/
@router.delete("/id/{id}", response_model=bool)
async def delete_user(id: str):
    return await User.delete(id)
