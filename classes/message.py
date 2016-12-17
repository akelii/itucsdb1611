

class Message:
    def __init__(self,objectId,senderId,ReceiverId,IsRead,MessageContent,SendDate, ReadDate):
        self.ObjectId=objectId
        self.SenderId=senderId
        self.ReceiverId=ReceiverId
        self.IsRead=IsRead
        self.MessageContent=MessageContent
        self.SendDate=SendDate
        self.ReadDate=ReadDate
        self.Deleted=0