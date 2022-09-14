import shelve

from pyorthanc.client import Orthanc


class Cache:

    def __init__(self, orthanc: Orthanc, db_path: str):
        self.orthanc = orthanc
        self.db_path = db_path

        # Orthanc use index for each event
        self.last_checkup_index = 0

    def get_changes(self, since: int = None):
        result = self.orthanc.get_changes(params={'since': self.last_checkup_index})
        changes = {change['ResourceType']: {'ID': change['ID'], 'seq': change['Seq']} for change in result['Changes'] if 'New' in change['ChangeType']}

        self.last_checkup_index = result['Last']

        return changes

