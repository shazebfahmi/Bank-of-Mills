class account:
    def __init__(self,c_id,accnt_id,accnt_type,accnt_status,message,last_update):
        self.customer_id=c_id
        self.account_id=accnt_id
        self.account_type=accnt_type
        self.account_status=accnt_status
        self.messages=message
        self.last_updated=last_update