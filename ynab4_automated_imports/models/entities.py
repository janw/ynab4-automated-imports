from datetime import date
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, validator
from pydantic.types import condecimal

from ..enums import ClearedStatus, EntityType, PayeeStringConditionOperatorType

Amount = condecimal(decimal_places=2)


class FileMetaDataEntity(BaseModel):
    entityType = EntityType.fileMetaData
    currentKnowledge: str
    budgetDataVersion: str


class AccountEntity(BaseModel):
    onBudget: bool
    accountName: str
    lastReconciledDate: Optional[date]
    lastReconciledBalance: float
    hidden: bool
    entityVersion: str
    entityId: UUID
    accountType: str
    entityType: EntityType
    sortableIndex: int
    lastEnteredCheckNumber: int


class TransactionEntity(BaseModel):
    payeeId: UUID
    flag: Optional[str] = None
    importedPayee: Optional[str]
    YNABID: Optional[str]
    FITID: Optional[Any]
    amount: Amount
    date: date
    targetAccountId: Optional[UUID] = None
    transferTransactionId: Optional[UUID] = None
    accepted: bool = False
    categoryId: Optional[str]
    subTransactions: Any = None
    memo: Optional[str]
    matchedTransactions: Any = None
    isTombstone: bool = False
    entityVersion: str
    cleared: ClearedStatus = ClearedStatus.Uncleared
    madeWithKnowledge: Any = None
    source: str = "Imported"
    accountId: UUID
    parentTransactionIdIfMatched: Optional[str] = None
    dateEnteredFromSchedule: Any = None
    entityId: UUID
    entityType = EntityType.transaction
    isResolvedConflict: bool = False
    checkNumber: Any = None


class PayeeStringConditionEntity(BaseModel):
    operand: str
    parentPayeeId: UUID
    entityVersion: str
    entityId: UUID
    operator: PayeeStringConditionOperatorType
    entityType = EntityType.payeeStringCondition


class PayeeEntity(BaseModel):
    targetAccountId: Optional[UUID] = None
    autoFillCategoryId: Optional[str]
    enabled: bool = True
    autoFillAmount: Optional[Amount]
    autoFillMemo: Optional[str]
    isTombstone: bool = False
    madeWithKnowledge: Any = None
    entityVersion: str
    entityId: UUID
    isResolvedConflict: bool = False
    entityType = EntityType.payee
    renameConditions: Optional[List[PayeeStringConditionEntity]]
    name: str

    @validator("entityId", pre=True)
    def validate_entity_id(cls, value):
        if not isinstance(value, UUID):
            splits = value.split(":")
            if len(splits) > 1:
                value = splits[-1]
            return UUID(value)

        return value
