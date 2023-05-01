# -*- coding: utf-8 -*-

# Import necessary modules
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from loguru import logger
from sqlalchemy.exc import IntegrityError

from service.core.user_lib import encrypt_pass

# Import custom modules
from service.database.user_model import User
from service.models.users import DaysEnum, UserSchema, UserSerializer, UserUpdateSchema

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
    limit: Optional[int] = Query(None, ge=0, le=1000),
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
            "limit": limit,
            "offset": offset,
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
    """
    Get a user by ID.

    Args:
        id (str): The ID of the user to retrieve.

    Raises:
        HTTPException: If the user is not found.

    Returns:
        UserSerializer: The serialized user object.
    """

    # Log that we're attempting to retrieve a user with the provided ID.
    logger.info(f"Attempting to retrieve user with ID {id}")

    # Retrieve the user from the database using the provided ID.
    user = await User.get_id(id)

    # If the user is not found, raise an HTTPException with status code 404.
    if not user:
        # Log that the user was not found.
        logger.warning(f"User with ID {id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    # Serialize the user object using the UserSerializer and return it.
    user_data = UserSerializer.from_orm(user)
    # Log that we successfully retrieved the user.
    logger.info(f"Retrieved user with ID {id}: {user_data}")
    return user_data


# API Route located at /api/v1/user/
@router.post("/create", response_model=UserSerializer)
async def create_user(user: UserSchema):
    """
    Create a new user in the database.

    Args:
        user (UserSchema): A Pydantic model representing the user to be created.

    Returns:
        UserSerializer: A Pydantic model representing the newly created user.
    """

    # Extract values from the user model and log them for debugging purposes.
    values = user.dict()
    logger.debug(f"submitted values: {values}")

    # Normalize the username and email address to lowercase.
    values["user_name"] = str(values["user_name"]).lower()
    values["email"] = str(values["email"]).lower()

    # Hash the password using the encrypt_pass() function and remove the password_two field.
    hash_pwd = encrypt_pass(values["password"])
    values["password"] = hash_pwd
    values.pop("password_two")

    try:
        # Create a new user object in the database using the extracted values.
        user_obj = await User.create(**values)

        # Log a message indicating that the user was successfully created.
        logger.info(f"User created with email {user_obj.email}")
    except IntegrityError as e:
        # If an integrity error occurs (e.g. duplicate email address), log an error message and raise an HTTPException.
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail="Email address already exists")

    # Serialize the user object using the UserSerializer and return it.
    user_data = UserSerializer.from_orm(user_obj)
    return user_data


# API Route located at /api/v1/user/
@router.put("/id/{id}", response_model=UserSerializer)
async def update_user(id: str, user: UserUpdateSchema):
    """
    Update a user in the database.

    Args:
        id (str): The ID of the user to be updated.
        user (UserUpdateSchema): A Pydantic model representing the fields to be updated.

    Returns:
        UserSerializer: A Pydantic model representing the updated user.
    """

    # Attempt to retrieve the user from the database by ID.
    db_user = await User.get_or_none(id=id)

    if db_user is None:
        # If the user does not exist, raise an HTTPException with a 404 status code.
        logger.error(f"User with ID {id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    # Update the fields of the retrieved user object using the values from the user model.
    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)

    # Save the updated user object back to the database.
    await db_user.save()
    logger.info(f"User with ID {id} updated successfully")

    # Serialize the updated user object using the UserSerializer and return it.
    updated_user = UserSerializer.from_orm(db_user)
    return updated_user


# API Route located at /api/v1/user/
@router.delete("/id/{id}", response_model=bool)
async def delete_user(id: str):
    """
    Delete a user from the database by ID.

    Args:
        id (str): The ID of the user to be deleted.

    Returns:
        bool: True if the user was deleted successfully, False otherwise.
    """

    # Attempt to retrieve the user from the database by ID.
    db_user = await User.get_or_none(id=id)

    if db_user is None:
        # If the user does not exist, raise an HTTPException with a 404 status code.
        logger.error(f"User with ID {id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user from the database.
    num_deleted = await db_user.delete()
    logger.info(f"{num_deleted} rows deleted for user with ID {id}")

    # Return True if the delete operation was successful, False otherwise.
    return num_deleted > 0
