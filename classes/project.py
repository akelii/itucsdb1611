class Project:
    def __init__(self, objectid, title, project_description, project_type, project_thesis_type, department, project_status_type, start_date, end_date, member_limit, team, created_by, manager):
        self.objectid = objectid
        self.title = title
        self.project_description = project_description
        self.project_type = project_type
        self.project_thesis_type = project_thesis_type
        self.department = department
        self.project_status_type = project_status_type
        self.start_date = start_date
        self.end_date = end_date
        self.member_limit = member_limit
        self.team = team
        self.created_by = created_by
        self.manager = manager
        self.deleted = 0
