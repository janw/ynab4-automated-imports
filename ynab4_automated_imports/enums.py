from enum import Enum


class ClearedStatus(str, Enum):
    Uncleared = "Uncleared"
    Cleared = "Cleared"
    Reconciled = "Reconciled"


class EntityType(str, Enum):
    category = "category"
    monthlyCategoryBudget = "monthlyCategoryBudget"
    payeeStringCondition = "payeeStringCondition"
    account = "account"
    accountMapping = "accountMapping"
    masterCategory = "masterCategory"
    monthlyBudget = "monthlyBudget"
    payee = "payee"
    scheduledTransaction = "scheduledTransaction"
    transaction = "transaction"
    budgetMetaData = "budgetMetaData"
    fileMetaData = "fileMetaData"


class PayeeStringConditionOperatorType(str, Enum):
    Is = "Is"
    Contains = "Contains"
    StartsWith = "StartsWith"
    EndsWith = "EndsWith"
