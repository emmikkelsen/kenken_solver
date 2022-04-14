//
//  Board.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

struct Group {
    private let members: [Square];
    private let operation: Operation;
    private let result: Int;
    private var permutations: [[Int]];

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
    
    mutating func addPermutations(permutation: [Int]) {
        self.permutations.append(permutation);
    }
    
    func getPermutation(idx: Int) -> [Int] {
        return self.permutations[idx];
    }
    
    func getSize() -> Int {
        return self.members.count;
    }
    
    func getLocations() -> [(Int, Int)] {
        return self.members.map { $0.getLocation() };
    }
    
    mutating func reset() {
        for var member in members {
            member.setValue(value:  0);
        }
    }
}
