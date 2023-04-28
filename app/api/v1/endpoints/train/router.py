from fastapi import APIRouter

from app.api.v1.endpoints.train.customer import view as views_customer

router_module = APIRouter()

router_module.include_router(
    router=views_customer.router, prefix="/user", tags=["[User]"]
)
