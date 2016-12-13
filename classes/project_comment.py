class ProjectComment:
    def __init__(self, ObjectId, PersonId, CommentedProjectId, Comment, CreateDate, UpdateDate):
        self.ObjectId = ObjectId
        self.PersonId = PersonId
        self.CommentedProjectId = CommentedProjectId
        self.Comment = Comment
        self.CreateDate = CreateDate
        self.UpdateDate = UpdateDate
        self.Deleted = 0