import requests
from enum import Enum
from typing import List, Self

class LineStatus(Enum):
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

    @classmethod
    def parse_string(cls, string: str) -> Self:
        try:
            return cls(string)
        except ValueError:
            raise ValueError(f"Unknown line status: {string}")


class Line:
    line_id: str
    _colour: str

    TFL_BASE_URL = "https://api.tfl.gov.uk/Line"
    TFL_STATUS_URL = "Status"
    GOOD_STATUSES = [LineStatus.GOOD_SERIVICE, LineStatus.NO_ISSUES]

    def __init__(self, line_id: str) -> None:
        self.line_id = line_id
    
    def get_status(self) -> List[LineStatus]:
        url = f'{self.TFL_BASE_URL}/{self.line_id}/{self.TFL_STATUS_URL}'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch status for line {self.line_id}. Error code: {response.status_code}")
        
        data = response.json()
        line_statuses = data[0]['lineStatuses']
        statuses = [LineStatus.parse_string(status['statusSeverityDescription']) for status in line_statuses]

        self._set_indicator_colour_from_statuses(statuses)
        
        return statuses
    
    def get_indicator_colour(self) -> str:
        if not self._colour:
            self.get_status()
        
        return self._colour
    
    def _set_indicator_colour_from_statuses(self, statuses: List[LineStatus]) -> None:
        colour = "green"

        for status in statuses:
            if status not in self.GOOD_STATUSES:
                colour = "red"
                break

        self._colour = colour



victoria_line = Line("victoria")