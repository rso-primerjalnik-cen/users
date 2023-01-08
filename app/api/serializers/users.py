from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UpdateUserProfile(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    date_of_birth: Optional[datetime]
    email: Optional[str]
