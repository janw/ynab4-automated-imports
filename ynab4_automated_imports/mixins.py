from datetime import datetime, timezone
import shutil
from .constants import BUDGET_FULL_FILENAME


class BackupMixin:
    def backup_full_file(self):
        now = datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d_%H%M%S_%fZ")
        full_file_backup_path = self.full_budget_file.with_suffix(
            self.full_budget_file.suffix + f".backup_{now}"
        )
        device_backup_path = self.device_file.with_suffix(
            self.device_file.suffix + f".backup_{now}"
        )

        shutil.copy(
            str(self.full_budget_file),
            str(full_file_backup_path),
        )
        shutil.copy(
            str(self.devices_path),
            str(device_backup_path),
        )

    def restore_full_file(self, rewind_by=1):
        backups_glob = self.full_budget_file.parent.glob(
            BUDGET_FULL_FILENAME + ".backup_*"
        )

        rewound = 0
        full_file_backup_path = None
        for full_file_backup_path in sorted(backups_glob, reverse=True):
            rewound += 1
            if rewind_by == rewound:
                break
        if not full_file_backup_path:
            raise ValueError("No backup to restore")

        backup_suffix = full_file_backup_path.suffix[8:]
        device_backup_path = self.device_file.with_suffix(
            self.device_file.suffix + f".backup_{backup_suffix}"
        )

        shutil.copy(
            str(full_file_backup_path),
            str(self.full_budget_file),
        )
        shutil.copy(
            str(device_backup_path),
            str(self.device_file),
        )
