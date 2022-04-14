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
        for x in 0..<size**2 {
            board.append(Square(location: (x/size, x%size)));
        }
        self.board = board;
        self.groups = [];
        
        self.row_sets = base_set(size: size, value: false);
        self.col_sets = base_set(size: size, value: false);
        self.active = [];
    }
    
    var groupCount: Int {
        return self.groups.count;
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
        for square in self.board {
            square.setValue(value: 0);
        }
        
        self.active = [];
        self.row_sets = base_set(size: self.size, value: false);
        self.col_sets = base_set(size: self.size, value: false);
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
    
    private func updateSquares() {
        for v in self.active {
            let group = self.groups[v.0];
            let permutation = group.getPermutation(idx: v.1);

            for (location, value) in zip(group.getLocations(), permutation) {
                for square in self.board {
                    if square.getLocation() == location {
                        square.setValue(value: value);
                    }
                }
            }
        }
    }
    
    func allValid() -> Bool {
        self.updateSquares();
        for group in self.groups {
            if !group.isValid() {
                return false;
            }
        }
        return true;
    }
    
    func getGroup(idx: Int) -> Group {
        return self.groups[idx];
    }
    
    func isValid() -> Bool {
        updateSquares();
        var boardList = base_set(size: self.size, value: 0);
        for square in self.board {
            boardList[square.getLocation().0][square.getLocation().1] = square.getValue();
        }
        
        for x in 0..<self.size {
            let row = boardList[x];
            if (!row.filter({ $0 > 0 }).isUnique) {
                return false;
            }
        }
        for y in 0..<self.size {
            var col: [Int] = [];
            for x in 0..<self.size {
                col.append(boardList[x][y]);
            }
            if (!col.filter({ $0 > 0 }).isUnique) {
                return false;
            }
        }
        return true;
    }
    
    private func atLocation(location: (Int, Int)) -> Square {
        let arr = self.board.filter({ $0.getLocation() == location });
        assert(arr.count == 1);
        return arr[0];
    }
    
    mutating func addGroup(locations: [(Int, Int)], operation: Operation, result: Int) {
        let members = locations.map(self.atLocation);
        self.groups.append(Group(members: members, operation: operation, result: result));
    }            
    
    mutating func addPermutations() {
        for group in self.groups {
            let members = group.getMembers();
            
            let permutations = permutations(boardSize: self.size, groupSize: group.getSize(), operation: group.getOperation(), result: group.getResult());
            
            for permutation in permutations {
                for x in 0..<group.getSize() {
                    members[x].setValue(value: permutation[x]);
                }
                if (self.isValid()) {
                    group.addPermutation(permutation: permutation);
                }
                self.resetBoard();
            }
        }
        self.groups.sort(by: { $0.permutationCount < $1.permutationCount });
        
        var locations: [(Int, Int)] = [];
        for group in self.groups {
            for member in group.getMembers() {
                locations.append(member.getLocation());
            }
        }
        for x in 0..<self.size {
            for y in 0..<self.size {
                assert(locations.contains(where: {
                    $0 == (x, y);
                }));
            }
        }
    }
}

func base_set<T>(size: Int, value: T) -> [[T]] {
    return Array(repeating: Array(repeating: value, count: size), count: size);
}

extension Array where Element: Hashable {
    var isUnique: Bool {
        var seen = Set<Element>()
        return allSatisfy { seen.insert($0).inserted }
    }
}
