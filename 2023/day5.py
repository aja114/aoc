import dataclasses
import math
from typing import TypeAlias


@dataclasses.dataclass
class MapElement:
    """Get from one range of resource to another."""
    source_range_min: int
    source_range_len: int
    destination_range_min: int
    
    def __post_init__(self):
        self.shift = self.destination_range_min - self.source_range_min
        self.source_range_max = self.source_range_min + self.source_range_len
    
    def in_range(self, element: int) -> bool:
        return self.source_range_min <= element < self.source_range_max

    def map(self, element: int) -> int:
        return element + self.shift


@dataclasses.dataclass
class Mapper:
    """Maps between one resource and another."""
    source_resource: str
    destination_resource: str
    mappers: list[MapElement]

    def __post_init__(self):
        self.mappers = sorted(
            self.mappers, key=lambda x: x.source_range_min
        )
    
    def map(self, element: int) -> int:
        if (mapper := self.find_mapper(element)) is not None:
            return mapper.map(element)
        return element
        
    def find_mapper(self, element: int) -> MapElement | None:
        mapper_ranges = [
            (mapper.source_range_min, mapper.source_range_max)
            for mapper in self.mappers
        ]
        i = in_sorted_ranges(element, mapper_ranges)
        if i is not None:
            return self.mappers[i]
        return None

        
MapperGraph: TypeAlias = dict[str, Mapper]


def in_sorted_ranges(element: int, ranges: list[tuple[int, int]]) -> int | None:
    for i, (s, e) in enumerate(ranges):
        if element < s:
            return None
        if s <= element < e:
            return i
    return None
    

def get_input(file: str) -> tuple[list[int], MapperGraph]:
    with open(file, "r") as f:
        seed_str, *maps_str = f.read().strip().split("\n\n")
    
    _, *seeds = seed_str.strip().split(" ")
    seeds = [int(s) for s in seeds]
    
    mapper_graph: MapperGraph = {}
    for map_str in maps_str:
        map_title, *map_values = map_str.strip().split("\n")
        map_source = map_title.split(" ")[0].split("-")[0]
        map_destination = map_title.split(" ")[0].split("-")[2]
        mapper_list = [
            MapElement(
                destination_range_min=int(value.split(" ")[0]),
                source_range_min=int(value.split(" ")[1]),
                source_range_len=int(value.split(" ")[2]),
            )
            for value in map_values
        ]
        mapper = Mapper(
            source_resource=map_source,
            destination_resource=map_destination,
            mappers=mapper_list
        )
        mapper_graph[map_source] = mapper
    return seeds, mapper_graph


def get_input_rev(file: str) -> tuple[list[int], MapperGraph]:
    with open(file, "r") as f:
        seed_str, *maps_str = f.read().strip().split("\n\n")

    _, *seeds = seed_str.strip().split(" ")
    seeds = [int(s) for s in seeds]

    mapper_graph: MapperGraph = {}
    for map_str in maps_str:
        map_title, *map_values = map_str.strip().split("\n")
        map_source = map_title.split(" ")[0].split("-")[2]
        map_destination = map_title.split(" ")[0].split("-")[0]
        mapper_list = [
            MapElement(
                destination_range_min=int(value.split(" ")[1]),
                source_range_min=int(value.split(" ")[0]),
                source_range_len=int(value.split(" ")[2]),
            )
            for value in map_values
        ]
        mapper = Mapper(
            source_resource=map_source,
            destination_resource=map_destination,
            mappers=mapper_list
        )
        mapper_graph[map_source] = mapper
    return seeds, mapper_graph


def part1(seeds: list[int], mapper_graph: MapperGraph):
    locations = []
    for seed in seeds:
        resource = "seed"
        resource_id = seed
        while resource != "location":
            map = mapper_graph.get(resource)
            resource = map.destination_resource
            resource_id = map.map(resource_id)
        locations.append(resource_id)
    return min(locations)


def part2(seeds: list[int], mapper_graph: MapperGraph) -> int:
    seed_pairs = list(sorted(
        ((seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)),
        key=lambda x: x[0]
    ))
    i = 0
    while True:
        if i % 50000 == 0:
            print(i)
        resource = "location"
        resource_id = i
        while resource != "seed":
            map = mapper_graph.get(resource)
            resource = map.destination_resource
            resource_id = map.map(resource_id)
        if in_sorted_ranges(resource_id, seed_pairs):
            return resource_id
        i += 1


if __name__ == "__main__":
    print(part1(*get_input("day5-input.txt")))
    print(part2(*get_input_rev("day5-input.txt")))
