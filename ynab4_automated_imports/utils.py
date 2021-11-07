from .models import (
    AccountEntity,
    PayeeEntity,
    YDeviceFile,
    BudgetFullFile,
    PayeeStringConditionOperatorType,
)
from pathlib import Path
from .constants import DEVICE_FILE_GLOB
from typing import List, Dict, Union
from uuid import UUID
import json


def ynab_style_json_dumps(v, *, default):
    return json.dumps(v, indent="\t", default=default)


def load_full_knowledge_device(devices_path: Path):
    # The following might have to be reverse sorted to get last full-knowledge device.
    # Hypothesis: adding a (dropbox-synced) device, adds it alphabetically (B.ydevice, C.ydevice, etc.)
    for dev_file in devices_path.glob(DEVICE_FILE_GLOB):
        device = YDeviceFile.parse_raw(dev_file.read_bytes())
        if device.hasFullKnowledge:
            return device, dev_file


def load_full_budget(budget_path):
    return BudgetFullFile.parse_raw((budget_path).read_bytes())


def _create_matcher(payee, operator, operand):
    def payee_matcher(name):
        if (
            (operator == PayeeStringConditionOperatorType.Is and operand == name)
            or (
                operator == PayeeStringConditionOperatorType.Contains
                and operand in name
            )
            or (
                operator == PayeeStringConditionOperatorType.StartsWith
                and name.startswith(operand)
            )
            or (
                operator == PayeeStringConditionOperatorType.EndsWith
                and name.endswith(operand)
            )
        ):
            return payee

    return payee_matcher


def load_payee_matchers(payees: List[PayeeEntity]):
    matchers = []
    for payee in payees:
        matcher = _create_matcher(
            payee,
            PayeeStringConditionOperatorType.Is,
            payee.name,
        )
        matchers.append(matcher)
        for renamer in payee.renameConditions or []:
            matcher = _create_matcher(
                payee,
                renamer.operator,
                renamer.operand,
            )
            matchers.append(matcher)

    return matchers


def load_accounts(
    accounts: List[AccountEntity],
) -> Dict[Union[str, UUID], AccountEntity]:
    account_dict = {}
    for account in accounts:
        account_dict.update(
            {
                account.accountName: account,
                account.entityId: account,
            }
        )

    return account_dict
