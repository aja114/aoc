import dataclasses
import enum


class Pulse(enum.Enum):
    HIGH = 1
    LOW = 0


class PulseProcessor:
    def process_pulse(self, s: str, p: Pulse) -> list[tuple[str, str, Pulse]]:
        raise NotImplementedError("Subclass and implement this.")


@dataclasses.dataclass
class FlipFlop(PulseProcessor):
    name: str
    dest: list[str]
    state: bool = dataclasses.field(default=False)
    
    def process_pulse(self, s: str, p: Pulse) -> list[tuple[str, str, Pulse]]:
        if p is Pulse.HIGH:
            return []
        if p is Pulse.LOW:
            pulse_to_send = Pulse.LOW if self.state else Pulse.HIGH
            self.state = not self.state
            return [(self.name, d, pulse_to_send) for d in self.dest]


@dataclasses.dataclass
class Conjunction(PulseProcessor):
    name: str
    dest: list[str]
    state: dict[str, Pulse] = dataclasses.field(default_factory=dict)

    def add_module(self, s: str):
        self.state[s] = Pulse.LOW

    def process_pulse(self, s: str, p: Pulse) -> list[tuple[str, str, Pulse]]:
        if s in self.state:
            self.state[s] = p
        if all(x is Pulse.HIGH for x in self.state.values()):
            return [(self.name, d, Pulse.LOW) for d in self.dest]
        return [(self.name, d, Pulse.HIGH) for d in self.dest]


@dataclasses.dataclass
class Broadcaster(PulseProcessor):
    name: str
    dest: list[str]

    def process_pulse(self, s: str, p: Pulse) -> list[tuple[str, str, Pulse]]:
        return [(self.name, d, p) for d in self.dest]


def get_input(file: str) -> dict[str, PulseProcessor]:
    processors = {}
    with open(file, "r") as f:
        processor_inputs = f.readlines()
        
    for processor_input in processor_inputs:
        processor_input = processor_input.strip()
        if processor_input[0] == "%":
            processor_input = processor_input[1:]
            pulse_proc_type = FlipFlop
        elif processor_input[0] == "&":
            processor_input = processor_input[1:]
            pulse_proc_type = Conjunction
        else:
            pulse_proc_type = Broadcaster
        name, dest = processor_input.split("->")
        processors[name.strip()] = pulse_proc_type(
            name=name.strip(),
            dest=[x.strip() for x in dest.strip().split(",")],
        )
    
    # add references to Conjuctions
    for proc in processors.values():
        for d in proc.dest:
            dest_proc = processors.get(d)
            if dest_proc and isinstance(dest_proc, Conjunction):
                dest_proc.add_module(proc.name)
    
    return processors


def part1(file: str):
    processors = get_input(file)
    pulses = []
    button_press = [("None", "broadcaster", Pulse.LOW)] * 1_000
    c = {
        Pulse.LOW: 0,
        Pulse.HIGH: 0,
    }
    while pulses or button_press:
        if not pulses:
            pulses = [button_press.pop()]
        for s, d, p in pulses:
            print(s, d, p)
        print("-"*150)
        new_pulses = []
        for source, dest, pulse in pulses:
            c[pulse] += 1
            proc = processors.get(dest)
            if proc:
                new_pulses += proc.process_pulse(source, pulse)
        pulses = new_pulses
    return c[Pulse.HIGH] * c[Pulse.LOW]


if __name__ == "__main__":
    print(part1("day20-input.txt"))
