//
//  Board.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

class Group {
    private let members: [Location];
    private let operation: Operation;
    private let result: Int;
    private var permutations: [Permutation];
    
    init(members: [Location], operation: Operation, result: Int) {
        self.members = members;
        self.operation = operation;
        self.result = result;
        self.permutations = [];
    }

    func isValid<T: RowColProt>(board: Board<T>) -> Bool {
        if self.operation == Operation.add {
            return board.getValues(group: self).reduce(0, +) == self.result;
        } else if self.operation == Operation.multiply {
            return board.getValues(group: self).reduce(0, *) == self.result;
        } else if self.operation == Operation.subtract {
            return board.getValues(group: self).reduce(0, max) - board.getValues(group: self).reduce(0, min) == self.result;
        } else if self.operation == Operation.divide {
            return board.getValues(group: self).reduce(0, max) / board.getValues(group: self).reduce(0, min) == self.result;
        }
        return false;
    }
    
    func getResult() -> Int {
        return self.result
    }
    
    func getOperation() -> Operation {
        return self.operation;
    }
    
    func addPermutation(permutation: Permutation) {
        self.permutations.append(permutation);
    }
    
    func getPermutation(idx: Int) -> Permutation {
        return self.permutations[idx];
    }
    
    var permutationCount: Int {
        return self.permutations.count;
    }
    
    func getSize() -> Int {
        return self.members.count;
    }
    
    func getLocations() -> [Location] {
        return self.members;
    }
}
