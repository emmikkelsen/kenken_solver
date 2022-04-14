//
//  Board.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

import Darwin

struct Board {
    let size: Int;
    private let board: [Square];
    private var groups: [Group];
    private var row_sets: [[Bool]];
    private var col_sets: [[Bool]];
    private var active: [(Int, Int)];

    init(size: Int) {
        self.size = size;
        
        var board: [Square] = [];
        for x in 0..<size^2 {
            board.append(Square(location: (x/size, x%size)));
        }
        self.board = board;
        self.groups = [];
        
        self.row_sets = base_set(size: size);
        self.col_sets = base_set(size: size);
        self.active = [];
    }
    
    mutating func tryPermutation(i_g: Int, i_p: Int) -> Bool {
        let group = self.groups[i_g];
        let permutation = group.getPermutation(idx: i_p);
        let locations = group.getLocations();
        
        for (location, value) in zip(locations, permutation) {
            if (self.row_sets[location.0][value-1] || self.col_sets[location.1][value-1]) {
                return false;
            }
        }
        
        for (location, value) in zip(locations, permutation) {
            self.row_sets[location.0][value-1] = true;
            self.col_sets[location.1][value-1] = true;
        }
        self.active.append((i_g, i_p));
        
        return true;
    }
    
    mutating func resetBoard() {
        for var square in self.board {
            square.setValue(value: 0);
        }
        
        self.active = [];
        self.row_sets = base_set(size: self.size);
        self.col_sets = base_set(size: self.size);
    }
    
    mutating func resetLast() {
        let v: (Int, Int) = self.active.popLast()!;
        let group = self.groups[v.0];
        let permutation = group.getPermutation(idx: v.1);
        
        let locations = group.getLocations();
        
        for (location, value) in zip(locations, permutation) {
            self.row_sets[location.0][value-1] = false;
            self.col_sets[location.1][value-1] = false;
        }
    }
    
    func allValid() -> Bool {
        for v in self.active {
            let group = self.groups[v.0];
            let permutation = group.getPermutation(idx: v.1);

            for (location, value) in zip(group.getLocations(), permutation) {
                for var square in self.board {
                    if square.getLocation() == location {
                        square.setValue(value: value);
                    }
                }
            }
        }
        for group in self.groups {
            if !group.isValid() {
                return false;
            }
        }
        return true;
    }
    
    mutating func addPermutations() {
        for group in self.groups {
            let permutations = permutations(boardSize: self.size, groupSize: group.getSize(), operation: group.getOperation(), result: group.getResult());
            
            for permutation in permutations {
                for x in 0..<group.getSize() {
                    
                }
            }
        }
    }
}

func base_set(size: Int) -> [[Bool]] {
    return Array(repeating: Array(repeating: false, count: size), count: size);
}
