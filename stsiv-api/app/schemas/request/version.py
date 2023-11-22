"""
"""
from uuid import UUID
from typing import (
    Optional,
    List,
    Union
)

from pydantic import (
    BaseModel,
    Field,
)


class CreateVersionRequest(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    experiment_id: UUID = Field(UUID)
    name: Optional[str | None] = Field(Optional[str | None])
    description: str = Field(str, description="In this version we changed...")


class ListVersionRequest(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    experiment_id: UUID = Field(UUID)


class ParameterItem(BaseModel):
    id: str
    value: Union[int, float]


class Command(BaseModel):
    alias: str
    value: Union[int, str, List[int]]


class Parameters(BaseModel):
    alias: str
    blockFrequencyTestBlockLength: ParameterItem
    nonOverlappingTemplateTestBlockLength: ParameterItem
    overlappingTemplateTestBlockLength: ParameterItem
    approximateEntropyTestBlockLength: ParameterItem
    serialTestBlockLength: ParameterItem
    linearComplexityTestBlockLength: ParameterItem
    numberOfBitcountRuns: ParameterItem
    uniformityBins: ParameterItem
    bitsToProcessPerIteration: ParameterItem
    uniformityCutoffLevel: ParameterItem
    alphaConfidenceLevel: ParameterItem


class VersionParamsRequest(BaseModel):
    tests: Command
    parameters: Parameters
    iterations: Command
    createResultFiles: Command
    bitcount: Command
    numOfThreads: Command
