
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)

router = APIRouter(prefix="/customers", tags=["Customers"])



@router.get("/", response_model=list[CustomerResponse])
def list_customers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Customer]:
    statement = (
        select(Customer)
        .where(Customer.owner_id == current_user.id)
        .order_by(Customer.id)
    )

    return list(db.scalars(statement).all())




@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    customer_data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Customer:
    customer = Customer(
        name=customer_data.name,
        email=str(customer_data.email),
        owner_id=current_user.id,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Customer:
    update_data = customer_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field must be provided",
        )

    statement = select(Customer).where(
        Customer.id == customer_id,
        Customer.owner_id == current_user.id,
    )
    customer = db.scalar(statement)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    for field, value in update_data.items():
        if value is not None:
            setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer




@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    statement = select(Customer).where(
        Customer.id == customer_id,
        Customer.owner_id == current_user.id,
    )

    customer = db.scalar(statement)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    db.delete(customer)
    db.commit()
