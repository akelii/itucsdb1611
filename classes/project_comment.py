class ProjectComment:
    def __init__(self, ObjectId, PersonId, CommentedProjectId, Comment):
        self.ObjectId = ObjectId
        self.PersonId = PersonId
        self.CommentedProjectId = CommentedProjectId
        self.Comment = Comment
        self.Deleted = 0