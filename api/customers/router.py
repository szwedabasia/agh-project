from fastapi import APIRouter, HTTPException, Query, Response, status, exception_handlers
from fastapi.encoders import jsonable_encoder

from .storage import get_customers_storage
from .schema import CustomerCreateSchema, CustomerUpdateSchema, Customer
from .validators import validate_phone_number, validate_email
router = APIRouter()

CUSTOMERS_STORAGE = get_customers_storage()


@router.get("/")
async def get_customers() -> list[Customer]:
    return list(get_customers_storage().values())


@router.get("/{customer_id}")
async def get_customer(customer_id: int) -> Customer:
    try:
        return CUSTOMERS_STORAGE[customer_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )


@router.patch("/{customer_id}", status_code=status.HTTP_200_OK)
async def update_customer(
        customer_id: int, updated_customer: CustomerUpdateSchema
) -> Customer:
    customer = CUSTOMERS_STORAGE.get(customer_id)
    if not customer:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )
    update_data = updated_customer.dict(exclude_unset=True)
    updated_item = customer.copy(update=update_data)
    CUSTOMERS_STORAGE[customer_id] = jsonable_encoder(updated_item)
    return updated_item


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int) -> None:
    try:
        del CUSTOMERS_STORAGE[customer_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID={customer_id} does not exist."
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreateSchema) -> Customer:
    customer.phone_number = validate_phone_number(str(customer.phone_number))
    customer.email = validate_email(customer.email)
    last_id = int(list(CUSTOMERS_STORAGE.keys())[-1]) if len(CUSTOMERS_STORAGE.keys()) > 0 else 0
    new_customer = Customer(**customer.dict(), id=last_id + 1)
    CUSTOMERS_STORAGE.update({last_id + 1: new_customer})
    return new_customer

