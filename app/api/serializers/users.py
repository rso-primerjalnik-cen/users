from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UpdateUserProfile(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[datetime]
    phone: Optional[str]
    email: Optional[str]
