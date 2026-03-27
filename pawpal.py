from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    name: str
    animal: str  # e.g. "dog", "cat", "other"


@dataclass
class Task:
    title: str
    time_to_complete: int   # minutes
    priority: str           # "low", "medium", "high"

    def set_time(self, minutes: int):
        self.time_to_complete = minutes

    def set_priority(self, priority: str):
        self.priority = priority


@dataclass
class Owner:
    name: str
    preferences: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def delete_pet(self, pet_name: str):
        self.pets = [p for p in self.pets if p.name != pet_name]


@dataclass
class Schedule:
    tasks: List[Task] = field(default_factory=list)

    def generate_schedule(self) -> List[Task]:
        # TODO: implement scheduling logic (sort by priority, time, etc.)
        pass

    def delete_schedule(self):
        self.tasks = []
