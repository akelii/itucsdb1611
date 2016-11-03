class WorkLog:
    def __init__(self, objectId, projectId, commitMessage, createDate, creatorPersonId, deleted):
        self.ObjectId = objectId
        self.ProjectId = projectId
        self.CommitMessage = commitMessage
        self.CreateDate = createDate
        self.CreatorPersonId = creatorPersonId
        self.Deleted = deleted