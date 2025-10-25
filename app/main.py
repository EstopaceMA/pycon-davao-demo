from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# FastAPI app with enhanced Swagger UI configuration
app = FastAPI(
    title="PyCon Davao Membership API",
    description="""
## PyCon Davao Membership Management System

This API provides complete CRUD operations for managing PyCon Davao conference memberships.

### Features:
* **Create members** - Register new PyCon attendees
* **Read members** - View member details and list all members
* **Update members** - Modify member information
* **Delete members** - Remove member records

### Membership Types:
* `student` - Student attendees
* `professional` - Professional attendees
* `speaker` - Conference speakers

### Authentication:
Currently, this API does not require authentication (demo purposes).
    """,
    version="1.0.0",
    contact={
        "name": "PyCon Davao Team",
        "url": "https://pycon.ph",
        "email": "info@pycon.ph",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc alternative documentation
)


@app.get(
    "/",
    tags=["Root"],
    summary="API Health Check",
    response_description="Welcome message",
)
async def read_root():
    """
    ## Health Check Endpoint

    Returns a welcome message to verify the API is running.
    """
    return {"message": "Hello from PyCon Davao Membership API!"}


@app.post(
    "/members/",
    response_model=schemas.MemberResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Members"],
    summary="Create a new member",
    response_description="The created member",
)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    """
    ## Create a new PyCon member

    Register a new member with the following information:

    - **first_name**: Member's first name
    - **last_name**: Member's last name
    - **email**: Unique email address (will be validated)
    - **membership_type**: Type of membership (student, professional, speaker)
    - **is_active**: Whether the membership is active (default: true)

    ### Example Request:
    ```json
    {
        "first_name": "Juan",
        "last_name": "Dela Cruz",
        "email": "juan@pycon.ph",
        "membership_type": "professional",
        "is_active": true
    }
    ```

    ### Returns:
    The created member with auto-generated ID and timestamps.

    ### Errors:
    - **400**: Email already registered
    """
    db_member = crud.get_member_by_email(db, email=member.email)
    if db_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return crud.create_member(db=db, member=member)


@app.get(
    "/members/",
    response_model=List[schemas.MemberResponse],
    tags=["Members"],
    summary="Get all members",
    response_description="List of all members",
)
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ## Get all PyCon members

    Retrieve a list of all registered members with pagination support.

    ### Parameters:
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 100)

    ### Returns:
    List of members with their complete information.
    """
    members = crud.get_members(db, skip=skip, limit=limit)
    return members


@app.get(
    "/members/{member_id}",
    response_model=schemas.MemberResponse,
    tags=["Members"],
    summary="Get member by ID",
    response_description="Member details",
)
def read_member(member_id: int, db: Session = Depends(get_db)):
    """
    ## Get a specific PyCon member by ID

    Retrieve detailed information about a specific member.

    ### Parameters:
    - **member_id**: The unique ID of the member

    ### Returns:
    Complete member information including timestamps.

    ### Errors:
    - **404**: Member not found
    """
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )
    return db_member


@app.put(
    "/members/{member_id}",
    response_model=schemas.MemberResponse,
    tags=["Members"],
    summary="Update a member",
    response_description="Updated member details",
)
def update_member(
    member_id: int, member: schemas.MemberUpdate, db: Session = Depends(get_db)
):
    """
    ## Update a PyCon member

    Update one or more fields of an existing member. All fields are optional.

    ### Parameters:
    - **member_id**: The unique ID of the member to update

    ### Request Body (all fields optional):
    - **first_name**: New first name
    - **last_name**: New last name
    - **email**: New email address
    - **membership_type**: New membership type
    - **is_active**: New active status

    ### Example Request:
    ```json
    {
        "membership_type": "speaker",
        "is_active": true
    }
    ```

    ### Returns:
    The updated member with modified `updated_at` timestamp.

    ### Errors:
    - **404**: Member not found
    """
    db_member = crud.update_member(db, member_id=member_id, member_update=member)
    if db_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )
    return db_member
