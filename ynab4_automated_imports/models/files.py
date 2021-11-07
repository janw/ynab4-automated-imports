from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel

from ..utils import ynab_style_json_dumps
from .entities import AccountEntity, FileMetaDataEntity, PayeeEntity, TransactionEntity


class DiffFile(BaseModel):
    startVersion: str  # endVersion of the previous Diff
    endVersion: str  # last item's entityVersion

    publishTime: datetime
    dataVersion: str
    items: List[Union[TransactionEntity, PayeeEntity]]
    shortDeviceId: str
    deviceGUID: UUID

    formatVersion: Optional[str]
    budgetDataGUID: Optional[UUID]


class BudgetMetaFile(BaseModel):
    TED: int
    formatVersion: str
    relativeDataFolderName: str


class YDeviceFile(BaseModel):
    deviceType: str
    formatVersion: str
    lastDataVersionFullyKnown: str

    YNABVersion: str
    highestDataVersionImported: Optional[str]

    friendlyName: str
    shortDeviceId: str
    deviceGUID: str

    # the latest (diff) knowledge that this device has
    knowledge: str
    # the latest knowledge that this devices has in its full budget file
    knowledgeInFullBudgetFile: str
    # if the device has the highest diff/full knowledge version?
    hasFullKnowledge: bool


class BudgetFullFile(BaseModel):
    monthlyBudgets: List[Any]
    masterCategories: List[Any]
    scheduledTransactions: List[Any]
    fileMetaData: FileMetaDataEntity
    accountMappings: List[Any]
    payees: List[PayeeEntity]
    accounts: List[AccountEntity]
    budgetMetaData: Dict[str, Any]
    transactions: List[TransactionEntity]

    class Config:
        json_dumps = ynab_style_json_dumps
