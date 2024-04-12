from datetime import date

class InvalidBugTitle(Exception):
    pass

class InvalidBugSummary(Exception):
    pass

class InvalidPriority(Exception):
    pass


class Bug:
    def __init__(self, bug_id, user_id, date, bug_title, bug_summary, priority, notify):
        self.bug_id = bug_id
        self.user_id = user_id
        self.date = date
        self.bug_title = bug_title
        self.bug_summary = bug_summary
        self.priority = priority
        self.notify = notify
    
    def values(self):
        return (self.bug_id, self.user_id, self.date, self.bug_title, self.bug_summary, self.priority, self.notify)

def make_new_bugs(rForm, uID):
    return Bug(None, uID, date.today(), rForm.get("bug_title"), rForm.get("bug_info"), rForm.get("options"), 0).values()

def make_new_bugs_complete(rForm, uID):
    if not rForm.get("bug_title"):
        raise InvalidBugTitle
    if not rForm.get("bug_info"):
        raise InvalidBugSummary
    if not rForm.get("options"):
        raise InvalidPriority
    
    return Bug(None, uID, date.today(), rForm.get("bug_title"), rForm.get("bug_info"), rForm.get("options"), 0).values()
        