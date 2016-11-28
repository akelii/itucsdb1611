
class Experience:
    def __init__(self, objectId, cvId, description,companyName,startDate,endDate, experiencePosition):
        self.ObjectId = objectId
        self.CVId = cvId
        self.ExperiencePosition = experiencePosition
        self.CompanyName=companyName
        self.Description = description
        self.StartDate = startDate
        self.EndDate = endDate
        self.Deleted = '0'

