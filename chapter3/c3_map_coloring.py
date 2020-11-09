from util_csp import Constraint, CSP
from typing import Dict, List, Optional

class MapColoringContraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2
    
    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        
        return assignment[self.place1] != assignment[self.place2]

if __name__ == "__main__":
    variables: List[str] = ['Western Australia', 'Northern Territory', 'South Australia',
                            'Queensland', 'New South Wales', 'Victoria', 'Tasmania']
    domains: Dict[str, List[str]] = {}

    for variable in variables:
        domains[variable] = ['red', 'green', 'blue']
    
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(MapColoringContraint('Western Australia', 'Northern Territory'))
    csp.add_constraint(MapColoringContraint('Western Australia', 'South Australia'))
    csp.add_constraint(MapColoringContraint('South Australia', 'Northern Territory'))
    csp.add_constraint(MapColoringContraint('Queensland', 'Northern Territory'))
    csp.add_constraint(MapColoringContraint('Queensland', 'South Australia'))
    csp.add_constraint(MapColoringContraint('Queensland', 'New South Wales'))
    csp.add_constraint(MapColoringContraint('New South Wales', 'South Australia'))
    csp.add_constraint(MapColoringContraint('Victoria', 'South Australia'))
    csp.add_constraint(MapColoringContraint('Victoria', 'New South Wales'))
    csp.add_constraint(MapColoringContraint('Victoria', 'Tasmania'))

    solution: Optional[Dict[str, str]] = csp.backtracking_search()

    if solution is None:
        print('No Solution found!')
    else:
        print(solution)