from datetime import date
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union
from uuid import UUID, uuid4

from .budget_version import BudgetVersion
from .constants import BUDGET_FULL_FILENAME, BUDGET_META_FILENAME
from .mixins import BackupMixin
from .models import (
    AccountEntity,
    BudgetFullFile,
    BudgetMetaFile,
    PayeeEntity,
    TransactionEntity,
)
from .utils import (
    load_accounts,
    load_full_budget,
    load_full_knowledge_device,
    load_payee_matchers,
)


class Budget(BackupMixin):
    full_budget: BudgetFullFile
    version: BudgetVersion
    payee_matchers: List[Callable]
    accounts: Dict[Union[str, UUID], AccountEntity]

    full_budget_file: Path
    device_file: Path

    def __init__(self, budget_path, load=True):
        self.budget_path = budget_path
        meta_file = self.budget_path / BUDGET_META_FILENAME
        budget_meta = BudgetMetaFile.parse_raw(meta_file.read_bytes())
        data_folder_name = budget_meta.relativeDataFolderName
        self.devices_path = self.budget_path / data_folder_name / "devices"

        self.load_device()
        self.full_budget_file = (
            self.budget_path
            / data_folder_name
            / self.device.deviceGUID
            / BUDGET_FULL_FILENAME
        )

        if load:
            self.load_full_file()

    def __str__(self):
        return f"{self.budget_path.stem}"

    def __repr__(self):
        return f"Budget({self} at {self.version})"

    @property
    def is_uptodate(self):
        return self.version == self.device.knowledge

    def load_device(self):
        self.device, self.device_file = load_full_knowledge_device(
            devices_path=self.devices_path
        )

    def load_full_file(self):
        self.full_budget = load_full_budget(self.full_budget_file)
        self.version = BudgetVersion(self.full_budget.fileMetaData.currentKnowledge)

        if not self.is_uptodate:
            raise RuntimeError(
                "Full budget is not up to date. Save a version in YNAB, close it, and"
                " call load_full_file again."
            )

        self.payee_matchers = load_payee_matchers(self.full_budget.payees)
        self.accounts = load_accounts(self.full_budget.accounts)

    def update_file_object(self):
        self.full_budget.fileMetaData.currentKnowledge = str(self.version)

    def dump_full_file(self, backup=True):
        self.update_file_object()
        if backup:
            self.backup_full_file()

        self.full_budget_file.write_text(self.full_budget.json())

        self.device.knowledge = str(self.version)
        self.device.knowledgeInFullBudgetFile = str(self.version)
        self.device_file.write_text(self.device.json())

    def get_account(self, account_name_or_id) -> AccountEntity:
        return self.accounts[account_name_or_id]

    def get_or_create_payee(self, payee_name) -> PayeeEntity:
        return self.get_payee(payee_name) or self.create_payee(payee_name)

    def get_payee(self, payee_name) -> Optional[PayeeEntity]:
        for matcher in self.payee_matchers:
            if found_payee := matcher(payee_name):
                return found_payee

    def create_payee(self, payee_name):
        payee = PayeeEntity(
            name=payee_name,
            entityId=uuid4(),
            entityVersion=self.version.bump(),
        )
        self.full_budget.payees.append(payee)
        return payee

    def create_transaction(
        self,
        payee: str,
        account: str,
        amount: float,
        date: date,
        memo: str,
    ):
        payee_obj = self.get_or_create_payee(payee)
        account_obj = self.get_account(account)
        transaction = TransactionEntity(
            payeeId=payee_obj.entityId,
            categoryId=payee_obj.autoFillCategoryId,
            accountId=account_obj.entityId,
            entityVersion=self.version.bump(),
            entityId=uuid4(),
            amount=amount,
            date=date,
            memo=memo,
        )

        self.full_budget.transactions.append(transaction)
        return transaction
