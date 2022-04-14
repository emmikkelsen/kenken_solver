//
//  Board.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

class Group {
    private let members: [Square];
    private let operation: Operation;
    private let result: Int;
    private var permutations: [[Int]];
    
    init(members: [Square], operation: Operation, result: Int) {
        self.members = members;
        self.operation = operation;
        self.result = result;
        self.permutations = [];
    }

    func isValid() -> Bool {
        if self.operation == Operation.add {
            return self.values().reduce(0, +) == self.result;
        } else if self.operation == Operation.multiply {
            return self.values().reduce(0, *) == self.result;
        } else if self.operation == Operation.subtract {
            return self.values().reduce(0, max) - self.values().reduce(0, min) == self.result
        } else if self.operation == Operation.divide {
            return self.values().reduce(0, max) / self.values().reduce(0, min) == self.result
        }
        return false;
    }
    
    private func values() -> [Int] {
        return self.members.map { $0.getValue() };
    }
    
    func getResult() -> Int {
        return self.result
    }
    
    func getOperation() -> Operation {
        return self.operation;
    }
    
    func addPermutation(permutation: [Int]) {
        self.permutations.append(permutation);
    }
    
    func getPermutation(idx: Int) -> [Int] {
        return self.permutations[idx];
    }
    
    var permutationCount: Int {
        return self.permutations.count;
    }
    
    func getSize() -> Int {
        return self.members.count;
    }
    
    func getLocations() -> [(Int, Int)] {
        return self.members.map { $0.getLocation() };
    }
    
    func getMembers() -> [Square] {
        return self.members;
    }
    
    func reset() {
        for member in members {
            member.setValue(value:  0);
        }
    }
}
