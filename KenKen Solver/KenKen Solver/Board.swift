//
//  Board.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

import Darwin


class Board<T: RowColProt> {
    let size: Int;
    private var board: Dictionary<Location, Square>;
    private var groups: [Group];
    private var row_sets: [T];
    private var col_sets: [T];
    private var active: [(Int, Int)];
    private var initializer: () -> T;

    init(size: Int, initializer: @escaping () -> T) {
        self.size = size;
        
        var board: Dictionary<Location, Square> = Dictionary();
        for x in 0..<size**2 {
            board[Location(x/size, x%size)] = Square();
        }
        self.board = board;
        self.groups = [];
        self.initializer = initializer;
        
        self.row_sets = Array(repeating: initializer(), count: size);
        self.col_sets = Array(repeating: initializer(), count: size);
        self.active = [];
    }
    
    var groupCount: Int {
        return self.groups.count;
    }
    
    func tryPermutation(i_g: Int, i_p: Int) -> Bool {
        let group = self.groups[i_g];
        let permutation = group.getPermutation(idx: i_p);
        let locations = group.getLocations();
        
        for (location, value) in zip(locations, permutation) {
            if (self.row_sets[location.x].contains(value) || self.col_sets[location.y].contains(value)) {
                return false;
            }
        }
        
        for (location, value) in zip(locations, permutation) {
            self.row_sets[location.x].insert(value);
            self.col_sets[location.y].insert(value);
        }
        self.active.append((i_g, i_p));
        
        return true;
    }
    
    @inlinable func addPermutationIfPossible(idx_g: Int, idx_p: Int) -> Bool {
        let group = self.groups[idx_g];
        let permutation = group.getPermutation(idx: idx_p);
        
        let added = self.addPermutationIfPossible(group: group, permutation: permutation);
        if added {
            self.active.append((idx_g, idx_p));
        }
        
        return added;
    }
    
    func addPermutationIfPossible(group: Group, permutation: Permutation) -> Bool {
        let locations = group.getLocations();
        if self.valuesPossible(zip(locations, permutation)) {
            self.addValues(zip(locations, permutation));
            return true;
        }
        return false;
    }
    
    @inlinable func valuesPossible(_ locationsValues: Zip2Sequence<[Location], [Int]>) -> Bool {
        for (location, value) in locationsValues {
            if (self.row_sets[location.x].contains(value)) {
                return false;
            }
            if (self.col_sets[location.x].contains(value)) {
                return false;
            }
        }
        return true;
    }
    
    func removePermutation(group: Group, permutation: Permutation) {
        let locations = group.getLocations();
        
        self.removeValues(zip(locations, permutation));
    }
    
    @inlinable func removeValues(_ locationsValues: Zip2Sequence<[Location], [Int]>) {
        for (location, value) in locationsValues {
            self.row_sets[location.x].remove(value);
            self.col_sets[location.y].remove(value);
        }
    }
    
    @inlinable func addValues(_ locationsValues: Zip2Sequence<[Location], [Int]>) {
        for (location, value) in locationsValues {
            self.row_sets[location.x].insert(value);
            self.col_sets[location.y].insert(value);
        }
    }
    
    func getSquares(group: Group) -> [Square] {
        return self.getSquares(locations: group.getLocations());
    }
    
    func getSquares(locations: [Location]) -> [Square] {
        return locations.map({ self.board[$0]! });
    }
    
    func getValues(group: Group) -> [Int] {
        return self.getSquares(group: group).map({ $0.value });
    }
    
    func getValues(locations: [Location]) -> [Int] {
        return self.getSquares(locations: locations).map({ $0.value });

    }
    
    func resetBoard() {
        self.board.filter({ $1.value != 0 }).forEach({
            self.board[$0.key]?.value = 0;
        })
        
        self.active = [];
        self.row_sets = Array(repeating: self.initializer(), count: self.size);
        self.col_sets = Array(repeating: self.initializer(), count: self.size);
    }
    
    func resetLast() {
        let v: (Int, Int) = self.active.popLast()!;
        let group = self.groups[v.0];
        let permutation = group.getPermutation(idx: v.1);
        
        self.removePermutation(group: group, permutation: permutation);
    }
    
    private func updateSquares() {
        for v in self.active {
            let group = self.groups[v.0];
            let permutation = group.getPermutation(idx: v.1);

            for (location, value) in zip(group.getLocations(), permutation) {
                self.board[location]!.value = value;
            }
        }
    }
    
    func allValid() -> Bool {
        self.updateSquares();
        for group in self.groups {
            if !group.isValid(board: self) {
                return false;
            }
        }
        return true;
    }
    
    @inlinable func getGroup(idx: Int) -> Group {
        return self.groups[idx];
    }
    
    func isValid() -> Bool {
        updateSquares();
        var boardList = base_set(size: self.size, value: 0);
        for location in self.board.keys {
            boardList[location.x][location.y] = self.board[location]!.value;
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
    
    private func atLocation(location: Location) -> Square {
        return self.board[location]!;
    }
    
    func addGroup(locations: [Location], operation: Operation, result: Int) {
        self.groups.append(Group(members: locations, operation: operation, result: result));
    }            
    
    func addPermutations() {
        for group in self.groups {
            let locations = group.getLocations();
            
            let permutations = permutations(boardSize: self.size, groupSize: group.getSize(), operation: group.getOperation(), result: group.getResult());
            var i = 0;
            for permutation in permutations {
                for x in 0..<group.getSize() {
                    self.board[locations[x]]!.value = permutation[x];
                }
                if (self.isValid()) {
                    i += 1;
                    group.addPermutation(permutation: permutation);
                }
                self.resetBoard();
            }
            assert(i > 0, "No permutation added!");
        }
        //self.groups.sort(by: { $0.permutationCount > $1.permutationCount });
        self.groups.sort(by: { $0.permutationCount < $1.permutationCount })
        
        var locations: [Location] = [];
        for group in self.groups {
            locations.append(contentsOf: group.getLocations());
        }
        for x in 0..<self.size {
            for y in 0..<self.size {
                assert(locations.contains(Location(x, y)));
            }
        }
    }
}

func base_set<T>(size: Int, value: T) -> [[T]] {
    return Array(repeating: Array(repeating: value, count: size), count: size);
}
