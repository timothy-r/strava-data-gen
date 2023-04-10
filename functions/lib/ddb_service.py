import json

"""
    Service to encapsulate reading & writing to DDB table
"""
class DDBService:
    
    def __init__(self, logger, ddb_client, table_name:str) -> None:
        """
            initialise instance variables
        """
        self._logger = logger
        self._ddb_client = ddb_client
        self._table_name = table_name
        return None

    def generate_key(self, item:dict):
        """
            return the unique key string for this item
        """
        # activity:{id}:athlete:{athlete.id}
        return "activity:{}:athlete:{}".format(item['id'], item['athlete']['id'])
    
    def ensure_table_exists(self):
        """
            create a table, if it doesn't exist
        """
        try:
            table = self._ddb_client.describe_table(TableName=self._table_name)
            if table:
                return True
        except:
            # ResourceNotFoundException 
            self._logger.info("DDB table not found: {}".format(self._table_name))
                   
        self._ddb_client.create_table(
            TableName=self._table_name,
            KeySchema=[
                {
                    'AttributeName': 'Id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 25,
                'WriteCapacityUnits': 25
            }
        )
        
        waiter = self._ddb_client.get_waiter('table_exists')
        waiter.wait(
           TableName=self._table_name,
            WaiterConfig={
                'Delay': 2,
                'MaxAttempts': 50
            }
        )

        return True
        
    
    def store_item(self, key:str, item:dict) -> bool:
        """
            put this item with the specified key
        """
        item_data = json.dumps(item)
        
        data_to_write = {
            'Id': {"S": key},
            'Activity': {"S": item_data}
        }
        
        self._ddb_client.put_item(
            TableName=self._table_name,
            Item=data_to_write
        )