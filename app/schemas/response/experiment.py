from pydantic import BaseModel, Field
from uuid import UUID

class GetExperimentSchema(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id: UUID =  Field(UUID)
    creator_id: UUID = Field(UUID)
    name: str = Field(str)
    description: str = Field(str)
    versions_num: int = Field(int)
    
    class Config: 
        from_attributes = True
    
