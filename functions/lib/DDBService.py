"""
    Service to encapsulate reading & writing to DDB table
"""
class DDBService:
    
    """
    """
    def __init__(self, logger, ddb_client, table_name:str) -> None:
        self._logger = logger
        self._ddb_client = ddb_client
        self._table_name = table_name
    
    """
        put this item with the specified key
    """
    def store_item(self, key, item) -> bool:
        pass