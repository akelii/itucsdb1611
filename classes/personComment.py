class PersonComment:
    def __init__(self, objectId, personId, commentedPersonId, comment, createDate, updateDate):
        self.ObjectId = objectId
        self.PersonId = personId
        self.CommentedPersonId = commentedPersonId
        self.Comment = comment
        self.CreateDate = createDate
        self.UpdateDate = updateDate
        self.Deleted = 0