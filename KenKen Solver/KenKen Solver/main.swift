//
//  main.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

//import Foundation


extension StringProtocol {
    subscript(offset: Int) -> Character {
        self[index(startIndex, offsetBy: offset)]
    }
}

print("Running Main");

func add<T: RowColProt>(board: Board<T>, locationString: String, operation: Operation, result: Int) {
    var locations: [Location] = [];
    for x in stride(from: 0, to: locationString.count, by: 2) {
        let h = Int(locationString[x].asciiValue! - 97);
        let v = Int(String(locationString[x + 1]))! - 1;
        locations.append(Location(h, v));
    }
    board.addGroup(locations: locations, operation: operation, result: result)
}

func initializeBoard<T: RowColProt>(board: Board<T>) {
    
    add(board: board, locationString: "a1b1", operation: Operation.subtract, result: 1)
    add(board: board, locationString: "c1d1", operation: Operation.subtract, result: 3)
    add(board: board, locationString: "e1", operation: Operation.add, result: 7)
    add(board: board, locationString: "f1g1", operation: Operation.add, result: 14)
    add(board: board, locationString: "h1", operation: Operation.add, result: 1)
    add(board: board, locationString: "i1i2", operation: Operation.subtract, result: 7)

    add(board: board, locationString: "a2b2c2d2", operation: Operation.add, result: 21)
    add(board: board, locationString: "e2f2e3e4", operation: Operation.add, result: 14)
    add(board: board, locationString: "g2g3", operation: Operation.add, result: 10)
    add(board: board, locationString: "h2h3i3i4", operation: Operation.add, result: 19)

    add(board: board, locationString: "a3b3", operation: Operation.add, result: 17)
    add(board: board, locationString: "c3d3", operation: Operation.subtract, result: 3)
    add(board: board, locationString: "f3f4", operation: Operation.subtract, result: 2)

    add(board: board, locationString: "a4a5", operation: Operation.subtract, result: 1)
    add(board: board, locationString: "b4c4", operation: Operation.subtract, result: 6)
    add(board: board, locationString: "d4d5", operation: Operation.subtract, result: 1)
    add(board: board, locationString: "g4g5f5", operation: Operation.add, result: 14)
    add(board: board, locationString: "h4h5i5", operation: Operation.add, result: 16)

    add(board: board, locationString: "b5", operation: Operation.add, result: 7)
    add(board: board, locationString: "c5c6d6", operation: Operation.add, result: 8)
    add(board: board, locationString: "e5e6e7", operation: Operation.add, result: 16)

    add(board: board, locationString: "a6b6", operation: Operation.subtract, result: 5)
    add(board: board, locationString: "f6f7", operation: Operation.subtract, result: 5)
    add(board: board, locationString: "g6g7", operation: Operation.subtract, result: 4)
    add(board: board, locationString: "h6h7", operation: Operation.subtract, result: 1)
    add(board: board, locationString: "i6i7", operation: Operation.add, result: 14)

    add(board: board, locationString: "a7", operation: Operation.add, result: 9)
    add(board: board, locationString: "b7c7", operation: Operation.subtract, result: 5)
    add(board: board, locationString: "d7d8", operation: Operation.add, result: 3)

    add(board: board, locationString: "a8a9b9", operation: Operation.add, result: 13)
    add(board: board, locationString: "b8c8", operation: Operation.add, result: 11)
    add(board: board, locationString: "e8e9f8f9", operation: Operation.add, result: 27)
    add(board: board, locationString: "g8g9", operation: Operation.add, result: 10)
    add(board: board, locationString: "h8h9", operation: Operation.add, result: 10)
    add(board: board, locationString: "i8i9", operation: Operation.subtract, result: 4)

    add(board: board, locationString: "c9d9", operation: Operation.add, result: 8)
    print("Added Groups");

    board.addPermutations();

    print("Added Permutations");
}




var iteration = 0;


func t(g: Int, p: Int) -> (Bool, [(Int, Int)]) {
    iteration += 1;
    
    if (iteration % 1000000 == 0) {
        print(iteration);
    }
    
    if board.addPermutationIfPossible(idx_g: g, idx_p: p) {
        if (g == board.groupCount - 1) {
            return (true, [(g, p)]);
        }
        var (worked, nextGroup): (Bool, [(Int, Int)]) = t(g: g+1, p: 0);
        if (worked) {
            nextGroup.append((g, p));
            return (true, nextGroup);
        } else {
            board.resetLast();
        }
    }
    if (p == board.getGroup(idx: g).permutationCount - 1) {
        return (false, []);
    }
    return t(g: g, p: p + 1);
}

func t2<T>(_ board: Board<T>) -> ([(Int, Int)], Int) {
    var iteration = 0;
    var g = 0;
    var p = 0;
    
    var solved = false;
    var active: [(Int, Int)] = [];
    
    while (!solved) {
        if (!solved && p == board.getGroup(idx: g).permutationCount) {
            let last = active.popLast();
            g = last!.0;
            p = last!.1 + 1;
            board.resetLast();
            continue;
        }
        
        iteration += 1;
        
        if (iteration % 1000000 == 0) {
            print(iteration);
        }
        
        let pValid = board.addPermutationIfPossible(idx_g: g, idx_p: p);
        if pValid {
            active.append((g, p));
            if g == board.groupCount - 1 {
                solved = true;
            } else {
                g += 1;
                p = 0;
            }
        } else {
            p += 1;
        }
    }
    return (active, iteration);
}

func t3<T>(_ board: Board<T>) -> ([(Int, Int)], Int) {
    var iteration = 0;
    var g = 0;
    var p = 0;
    
    var solved = false;
    var active: [(Int, Int)] = [];
    
    while (!solved) {
        if (!solved && p == board.getGroup(idx: g).permutationCount) {
            let last = active.popLast()!;
            board.removePermutation(group: board.getGroup(idx: last.0), permutation: board.getGroup(idx: last.0).getPermutation(idx: last.1));

            g = last.0;
            p = last.1 + 1;
            continue;
        }
        
        iteration += 1;
        
        if (iteration % 1000000 == 0) {
            print(iteration);
        }
        
        let group = board.getGroup(idx: g);
        let permutation = group.getPermutation(idx: p)
        
        let pValid = board.addPermutationIfPossible(group: group, permutation: permutation);
        if pValid {
            active.append((g, p));
            if g == board.groupCount - 1 {
                solved = true;
            } else {
                g += 1;
                p = 0;
            }
        } else {
            p += 1;
        }
    }
    return (active, iteration);
}


let N = 9
var board = Board<Set<Int>>(size: N, initializer: { Set<Int>() });
initializeBoard(board: board);

let solution = t(g: 0, p: 0);
print("Fosund valid board", solution.1, "in", iteration, "tries");

//board.resetBoard();

//var s = t2(board);
//print("Found valid board", s.0, "in", s.1, "tries");

board.resetBoard();
var s = t3(board);
print("Found valid board", s.0, "in", s.1, "tries");

guard var board1: Board<RowCol1> = Optional(Board<RowCol1>(size: N, initializer: { RowCol1(N) })) else { fatalError() };
initializeBoard(board: board1);
s = t2(board1);
print("Found valid board", s.0, "in", s.1, "tries");

print(board);
print(board.isValid());
print(board.allValid());
