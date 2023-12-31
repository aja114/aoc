import dataclasses


@dataclasses.dataclass
class Part:
    x: int
    m: int
    a: int
    s: int
    
    def val(self):
        return self.x+self.m+self.a+self.s


@dataclasses.dataclass
class Interval:
    min: int
    max: int
    
    def range(self) -> int: 
        return (self.max - self.min) + 1


@dataclasses.dataclass
class PartInterv:
    x: Interval
    m: Interval
    a: Interval
    s: Interval

    def val(self):
        return self.x.range()*self.m.range()*self.a.range()*self.s.range()


@dataclasses.dataclass
class Rule:
    axis: str
    val: int
    comp: str
  
    def apply(self, p: Part) -> bool:
        if self.comp == ">":
            return p.__getattribute__(self.axis) > self.val
        elif self.comp == "<":
            return p.__getattribute__(self.axis) < self.val
        else:
            raise ValueError(f"Unknown comp {self.comp}")

    def apply_interval(self, p: PartInterv) -> tuple[PartInterv | None, PartInterv | None]:
        interv = p.__getattribute__(self.axis)
        other_intervals = {
            k: Interval(**v)
            for k, v in dataclasses.asdict(p).items()
            if k != self.axis
        }
        if self.comp == ">":
            if interv.max <= self.val:
                return p, None
            if interv.min > self.val:
                return None, p
            if interv.min <= self.val < interv.max:
                true_interv = {
                    **other_intervals,
                    self.axis: Interval(min=interv.min, max=self.val)
                }
                false_interv = {
                    **other_intervals,
                    self.axis: Interval(min=self.val+1, max=interv.max)
                }
                return PartInterv(**false_interv), PartInterv(**true_interv)
        if self.comp == "<":
            if interv.max < self.val:
                return None, p
            if interv.min >= self.val:
                return p, None
            if interv.min < self.val <= interv.max:
                true_interv = {
                    **other_intervals,
                    self.axis: Interval(min=self.val, max=interv.max)
                }
                false_interv = {
                    **other_intervals,
                    self.axis: Interval(min=interv.min, max=self.val-1)
                }
                return PartInterv(**false_interv), PartInterv(**true_interv)


@dataclasses.dataclass
class Rules:
    rules: list[Rule]
    dest: list[str]
    default_dest: str
    
    def apply(self, p: Part) -> str:
        for r, d in zip(self.rules, self.dest):
            if r.apply(p):
                return d
        return self.default_dest
    
    def apply_interval(self, p: PartInterv) -> list[tuple[PartInterv, str]]:
        new_intervals = []
        for r, d in zip(self.rules, self.dest):
            true_p, false_p = r.apply_interval(p)
            if true_p is not None:
                new_intervals.append((true_p, d))
            if false_p is not None:
                p = false_p
        if p is not None:
            new_intervals.append((p, self.default_dest))
        return new_intervals


def get_input(file: str) -> tuple[dict[str, Rules], list[Part]]:
    def parse_rules(content: str) -> Rules:
        return Rules(
            rules=[
                Rule(
                    axis=r[0],
                    comp=r[1],
                    val=int(r.split(":")[0][2:])
                )
                for r in content[:-1].split(",")[:-1]
            ],
            dest=[r.split(":")[-1] for r in content[:-1].split(",")[:-1]],
            default_dest=content[:-1].split(",")[-1]
        )
    
    def parse_part(content: str) -> Part:
        part_attrs = {}
        for x in content.strip()[1:-1].split(","):
            part_attrs[x[0]] = int(x[2:])
        return Part(**part_attrs)
    
    with open(file, "r") as f:
        rule_str, part_str, *_ = f.read().strip().split("\n\n")

    rules = {}
    for x in rule_str.split("\n"):
        name, content, *_ = x.strip().split("{")
        rules[name] = parse_rules(content)
        
    parts = [parse_part(x) for x in part_str.split("\n")]
    
    return rules, parts


def part1(file: str) -> int:
    rules, parts = get_input(file)

    s = 0
    for part in parts:
        rule = rules["in"]
        while (dest := rule.apply(part)) not in ("R", "A"):
            rule = rules[dest]
        if dest == "A":
            s += part.val()
    return s
    

def part2(file: str) -> int:
    rules, _ = get_input(file)
    first_partinterv = PartInterv(
        x=Interval(min=1, max=4000),
        m=Interval(min=1, max=4000),
        a=Interval(min=1, max=4000),
        s=Interval(min=1, max=4000),
    )
    parts_rules = [(first_partinterv, "in")]
    res = []
    while parts_rules:
        p, r = parts_rules.pop(0)
        new_interv = rules[r].apply_interval(p)
        print(rules[r])
        print(p)
        for itv, d in new_interv:
            print(itv, d)
            if d == "R":
                continue
            if d == "A":
                res.append(itv)
            else:
                parts_rules.append((itv, d))
        print("-"*150)
    return sum(r.val() for r in res)


if __name__ == "__main__":
    print(part2("day19-input.txt"))
