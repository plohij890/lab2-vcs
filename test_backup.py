from backup_system import LocalBackup, S3Backup, BackupManager

def test_local_backup_save_and_restore():
    """Тестируем сохранение и восстановление в LocalBackup."""
    local = LocalBackup("C:/TestBackups")
    test_data = "Секретные данные ЛР1"

    backup_id = local.save(test_data)
    assert backup_id is not None
    
    restored_data = local.restore(backup_id)
    assert restored_data == test_data

def test_s3_backup_save_and_restore():
    """Тестируем сохранение и восстановление в S3Backup."""
    s3 = S3Backup("test-bucket-123")
    test_data = "Данные для облака"
    
    backup_id = s3.save(test_data)
    restored_data = s3.restore(backup_id)
    
    assert restored_data == test_data

def test_backup_manager_initialization():
    """Проверяем, что менеджер корректно инициализируется со списком хранилищ."""
    local = LocalBackup("C:/Backups")
    s3 = S3Backup("my-bucket")
    
    manager = BackupManager([local, s3])
    
    assert len(manager._destinations) == 2