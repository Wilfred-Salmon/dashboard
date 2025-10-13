import requests
from typing import List, Dict
from csv import DictReader
from src.ResourceCacher import ResourceCacher


class Cycle_Point_Status:
    num_standard_bikes: int
    num_ebikes: int
    total_slots: int

    def __init__(self, num_standard_bikes: str, num_ebikes: str, total_slots: str) -> None:
        self.num_standard_bikes = int(num_standard_bikes)
        self.num_ebikes = int(num_ebikes)
        self.total_slots = int(total_slots)

    def get_free_slots(self) -> int:
        return self.total_slots - self.num_standard_bikes - self.num_ebikes


class Cycle_Point(ResourceCacher[Cycle_Point_Status]):
    display_name: str

    TFL_BASE_URL = "https://api.tfl.gov.uk/BikePoint"
    USEFUL_KEYS = {"NbStandardBikes", "NbDocks", "NbEBikes"}
    KEY_MAPPING = {"NbStandardBikes" : "num_standard_bikes", "NbDocks": "total_slots", "NbEBikes": "num_ebikes"}

    def __init__(self, id: str, display_name: str) -> None:
        self.id = id
        self.display_name = display_name
        super().__init__()

    def get_cycle_point_status(self) -> Cycle_Point_Status:
        return self.get_cache()
    
    def get_resource_to_cache(self) -> Cycle_Point_Status:
        url = f'{self.TFL_BASE_URL}/{self.id}'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch status for cycle point {self.id}. Error code: {response.status_code}")
        
        bike_point_info = response.json()["additionalProperties"]
        trimmed_response = {self.KEY_MAPPING[dict["key"]]: dict["value"] for dict in bike_point_info if dict["key"] in self.USEFUL_KEYS}

        return(Cycle_Point_Status(**trimmed_response))
    
def get_cycles_list() -> List[Dict[str, str]]:
    with open('./data/bikes.csv', 'r') as csvfile:
        reader = DictReader(csvfile, delimiter=',')
        return list(reader)