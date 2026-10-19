from abc import ABC, abstractmethod
import uuid


# ============ АБСТРАКЦИЯ (центр сети) ============
class IBackupDestination(ABC):
    @abstractmethod
    def save(self, data: str) -> str: ...
    @abstractmethod
    def restore(self, backup_id: str) -> str: ...


# ============ КОНКРЕТНЫЕ УЗЛЫ СЕТИ ============
class LocalBackup(IBackupDestination):
    def __init__(self, root_path: str):
        self._root_path = root_path
        self._storage: dict[str, str] = {}

    def save(self, data: str) -> str:
        bid = uuid.uuid4().hex
        self._storage[bid] = data
        print(f"[LocalBackup] Сохранено в {self._root_path}, id={bid}: {data}")
        return bid

    def restore(self, backup_id: str) -> str:
        data = self._storage[backup_id]
        print(f"[LocalBackup] Восстановлено из {self._root_path}, id={backup_id}: {data}")
        return data


class S3Backup(IBackupDestination):
    def __init__(self, bucket: str):
        self._bucket = bucket
        self._storage: dict[str, str] = {}

    def save(self, data: str) -> str:
        bid = uuid.uuid4().hex
        self._storage[bid] = data
        print(f"[S3Backup] Сохранено в bucket {self._bucket}, id={bid}: {data}")
        return bid

    def restore(self, backup_id: str) -> str:
        data = self._storage[backup_id]
        print(f"[S3Backup] Восстановлено из bucket {self._bucket}, id={backup_id}: {data}")
        return data


class FtpBackup(IBackupDestination):
    def __init__(self, server: str):
        self._server = server
        self._storage: dict[str, str] = {}

    def save(self, data: str) -> str:
        bid = uuid.uuid4().hex
        self._storage[bid] = data
        print(f"[FtpBackup] Сохранено на FTP {self._server}, id={bid}: {data}")
        return bid

    def restore(self, backup_id: str) -> str:
        data = self._storage[backup_id]
        print(f"[FtpBackup] Восстановлено с FTP {self._server}, id={backup_id}: {data}")
        return data


# ============ ОСНОВНОЙ МОДУЛЬ ============
class BackupManager:
    def __init__(self, destinations: list[IBackupDestination]):
        self._destinations = destinations

    def create_backup(self, data: str) -> None:
        print(f"\n=== Создание резервной копии: {data} ===")
        for d in self._destinations:
            bid = d.save(data)
            print(f"  -> Backup id: {bid}")


# ============ НОВЫЙ УЗЕЛ (расширение без правок) ============
class NetworkFolderBackup(IBackupDestination):
    def __init__(self, folder_path: str):
        self._folder_path = folder_path
        self._storage: dict[str, str] = {}

    def save(self, data: str) -> str:
        bid = uuid.uuid4().hex
        self._storage[bid] = data
        print(f"[NetworkFolderBackup] Сохранено в сетевую папку "
              f"{self._folder_path}, id={bid}: {data}")
        return bid

    def restore(self, backup_id: str) -> str:
        data = self._storage[backup_id]
        print(f"[NetworkFolderBackup] Восстановлено из сетевой папки "
              f"{self._folder_path}, id={backup_id}: {data}")
        return data


# ============ ТОЧКА ВХОДА (композиция сети) ============
def main() -> None:
    local = LocalBackup(r"C:\Backups")
    s3 = S3Backup("my-backup-bucket")
    ftp = FtpBackup("ftp.example.com")

    destinations: list[IBackupDestination] = [local, s3, ftp]
    manager = BackupManager(destinations)

    manager.create_backup("Важные данные проекта")

    print("\n--- Восстановление из LocalBackup ---")
    saved_id = local.save("Тестовые данные")
    local.restore(saved_id)

    print("\n--- Добавляем новый канал (NetworkFolderBackup) ---")
    network = NetworkFolderBackup(r"\\server\backups")
    extended_manager = BackupManager(destinations + [network])
    extended_manager.create_backup("Данные после расширения")


if __name__ == "__main__":
    main()