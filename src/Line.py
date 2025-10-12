import requests
from enum import Enum
from src.ResourceCacher import ResourceCacher
from typing import List, Dict, Self, cast
from csv import DictReader

class LineStatus(str, Enum):
    SPECIAL_SERVICE = "Special Service"
    CLOSED = "Closed"
    SUSPENDED = "Suspended"
    PART_SUSPENDED = "Part Suspended"
    PLANNED_CLOSURE = "Planned Closure"
    PART_CLOSURE = "Part Closure"
    SEVERE_DELAYS = "Severe Delays"
    REDUCED_SERVICE = "Reduced Service"
    BUS_SERVICE = "Bus Service"
    MINOR_DELAYS = "Minor Delays"
    GOOD_SERIVICE = "Good Service"
    PART_CLOSED = "Part Closed"
    EXIT_ONLY = "Exit Only"
    NO_STEP_FREE_ACCESS = "No Step Free Access"
    CHANGE_OF_FREQUENCY = "Change of Frequency"
    DIVERTED = "Diverted"
    NOT_RUNNING = "Not Running"
    ISSUES_REPORTED = "Issues Reported"
    NO_ISSUES = "No Issues"
    INFORMATION = "Information"
    SERVICE_CLOSED = "Service Closed"
    UNKNOWN = "Unknown"

    @classmethod
    def parse_string(cls, string: str) -> Self:
        try:
            return cls(string)
        except ValueError:
            return cast(Self, cls.UNKNOWN)

class Line(ResourceCacher[List[LineStatus]]):
    line_id: str
    display_name: str

    TFL_BASE_URL = "https://api.tfl.gov.uk/Line"
    TFL_STATUS_URL = "Status"
    GOOD_STATUSES = [LineStatus.GOOD_SERIVICE, LineStatus.NO_ISSUES]
    GOOD_COLOUR = "green"
    BAD_COLOUR = "red"

    def __init__(self, line_id: str, display_name: str) -> None:
        self.line_id = line_id
        self.display_name = display_name
        super().__init__()
    
    def get_status(self) -> List[LineStatus]:
        return self.get_cache()
    
    def get_indicator_colour(self) -> str:        
        colour = self.GOOD_COLOUR

        for status in self.get_cache():
            if status not in self.GOOD_STATUSES:
                colour = self.BAD_COLOUR
                break

        return colour
    
    def get_resource_to_cache(self) -> List[LineStatus]:
        url = f'{self.TFL_BASE_URL}/{self.line_id}/{self.TFL_STATUS_URL}'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch status for line {self.line_id}. Error code: {response.status_code}")
        
        data = response.json()
        line_statuses = data[0]['lineStatuses']
        statuses = [LineStatus.parse_string(status['statusSeverityDescription']) for status in line_statuses]

        return statuses

def get_lines_list() -> List[Dict[str, str]]:
    with open('./data/lines.csv', 'r') as csvfile:
        reader = DictReader(csvfile, delimiter=',')
        return list(reader)