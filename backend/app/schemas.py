from datetime import datetime
from decimal import Decimal
import re
from pydantic import BaseModel, ConfigDict, Field, field_validator

class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=200)

class LoginResponse(BaseModel):
    accessToken: str
    tokenType: str
    expiresIn: int

class StoreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: str
    name: str
    city: str | None = None
    district: str | None = None
    branchCode: str | None = Field(default=None, validation_alias="branch_code", serialization_alias="branchCode")

class CatalogItemOut(BaseModel):
    id: str
    sku: str
    name: str
    nameAr: str | None = None
    description: str
    descriptionAr: str | None = None
    category: str
    categoryAr: str | None = None
    unitLabel: str
    active: bool
    availability: str
    price: Decimal | None
    currency: str | None
    priceLastSyncedAt: datetime | None
    stale: bool

class CategoryOut(BaseModel):
    value: str

class OrderItemRequest(BaseModel):
    productId: str
    quantity: int = Field(gt=0, le=200)
    clientUnitPrice: Decimal | None = Field(default=None, ge=0)

class CreateOrderRequest(BaseModel):
    storeId: str = Field(min_length=1, max_length=36)
    items: list[OrderItemRequest] = Field(min_length=1, max_length=100)
    note: str = Field(default="", max_length=500)
    customerPhone: str | None = Field(default=None, max_length=24)

    @field_validator("items")
    @classmethod
    def validate_unique_products(cls, value: list[OrderItemRequest]) -> list[OrderItemRequest]:
        product_ids = [item.productId for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Each product may appear only once in an order.")
        return value

    @field_validator("customerPhone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().replace(" ", "").replace("-", "")
        if not re.fullmatch(r"\+?[0-9]{7,20}", normalized):
            raise ValueError("customerPhone must contain 7-20 digits with an optional leading +.")
        return normalized

class OrderItemOut(BaseModel):
    productId: str
    productName: str
    quantity: int
    unitPrice: Decimal
    currency: str
    lineTotal: Decimal

class OrderOut(BaseModel):
    id: str
    publicOrderCode: str
    storeId: str
    state: str
    customerPhone: str | None = None
    totalAmount: Decimal
    currency: str
    version: int
    submittedAt: datetime
    items: list[OrderItemOut]

class ProductCreateRequest(BaseModel):
    storeId: str
    sku: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=140)
    nameAr: str | None = Field(default=None, max_length=140)
    description: str = Field(default="", max_length=2000)
    descriptionAr: str | None = Field(default=None, max_length=2000)
    category: str = Field(min_length=1, max_length=80)
    categoryAr: str | None = Field(default=None, max_length=80)
    unitLabel: str = Field(min_length=1, max_length=40)
    imageRef: str | None = Field(default=None, max_length=500)

class ProductPatchRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=140)
    nameAr: str | None = Field(default=None, min_length=1, max_length=140)
    description: str | None = Field(default=None, min_length=1, max_length=2000)
    descriptionAr: str | None = Field(default=None, min_length=1, max_length=2000)
    category: str | None = Field(default=None, min_length=1, max_length=80)
    categoryAr: str | None = Field(default=None, min_length=1, max_length=80)
    unitLabel: str | None = Field(default=None, min_length=1, max_length=40)
    imageRef: str | None = Field(default=None, max_length=500)
    active: bool | None = None

class PriceCreateRequest(BaseModel):
    amount: Decimal = Field(gt=0, le=999999999)
    currency: str = Field(min_length=1, max_length=8)

class AvailabilityRequest(BaseModel):
    state: str

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        if value not in {"AVAILABLE", "UNAVAILABLE"}:
            raise ValueError("Availability must be AVAILABLE or UNAVAILABLE.")
        return value

class MerchantMembershipOut(BaseModel):
    storeId: str
    storeName: str
    city: str | None = None
    district: str | None = None
    branchCode: str | None = None
    role: str

class MerchantMeOut(BaseModel):
    userId: str
    displayName: str
    memberships: list[MerchantMembershipOut]

class MerchantOrderListItem(BaseModel):
    id: str
    publicOrderCode: str
    storeId: str
    state: str
    itemCount: int
    totalAmount: Decimal
    currency: str
    version: int
    createdAt: datetime
