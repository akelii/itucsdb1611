class Team:
    def __init__(self, objectId, projectId, memberId, duty):
        self.ObjectId = objectId
        self.ProjectId = projectId
        self.MemberId = memberId
        self.Duty = duty
        self.Deleted = 0