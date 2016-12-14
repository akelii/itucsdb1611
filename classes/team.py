class Team:
    def __init__(self, objectId, projectId, memberId, duty):
        self.ObjectId = objectId
        self.MemberId = memberId
        self.ProjectId = projectId
        self.Duty = duty
        self.Deleted = 0