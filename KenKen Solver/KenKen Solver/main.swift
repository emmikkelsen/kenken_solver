//
//  main.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

//import Foundation

let N = 9
var board = Board(size: N)


extension StringProtocol {
    subscript(offset: Int) -> Character {
        self[index(startIndex, offsetBy: offset)]
    }
}

print("Running Main");

func add(locationString: String, operation: Operation, result: Int) {
    var locations: [(Int, Int)] = [];
    for x in stride(from: 0, to: locationString.count, by: 2) {
        let h = Int(locationString[x].asciiValue! - 97);
        let v = Int(String(locationString[x + 1]))! - 1;
        locations.append((h, v));
    }
    board.addGroup(locations: locations, operation: operation, result: result)
}


add(locationString: "a1b1", operation: Operation.subtract, result: 1)
add(locationString: "c1d1", operation: Operation.subtract, result: 3)
add(locationString: "e1", operation: Operation.add, result: 7)
add(locationString: "f1g1", operation: Operation.add, result: 14)
add(locationString: "h1", operation: Operation.add, result: 1)
add(locationString: "i1i2", operation: Operation.subtract, result: 7)

add(locationString: "a2b2c2d2", operation: Operation.add, result: 21)
add(locationString: "e2f2e3e4", operation: Operation.add, result: 14)
add(locationString: "g2g3", operation: Operation.add, result: 10)
add(locationString: "h2h3i3i4", operation: Operation.add, result: 19)

add(locationString: "a3b3", operation: Operation.add, result: 17)
add(locationString: "c3d3", operation: Operation.subtract, result: 3)
add(locationString: "f3f4", operation: Operation.subtract, result: 2)

add(locationString: "a4a5", operation: Operation.subtract, result: 1)
add(locationString: "b4c4", operation: Operation.subtract, result: 6)
add(locationString: "d4d5", operation: Operation.subtract, result: 1)
add(locationString: "g4g5f5", operation: Operation.add, result: 14)
add(locationString: "h4h5i5", operation: Operation.add, result: 16)

add(locationString: "b5", operation: Operation.add, result: 7)
add(locationString: "c5c6d6", operation: Operation.add, result: 8)
add(locationString: "e5e6e7", operation: Operation.add, result: 16)

add(locationString: "a6b6", operation: Operation.subtract, result: 5)
add(locationString: "f6f7", operation: Operation.subtract, result: 5)
add(locationString: "g6g7", operation: Operation.subtract, result: 4)
add(locationString: "h6h7", operation: Operation.subtract, result: 1)
add(locationString: "i6i7", operation: Operation.add, result: 14)

add(locationString: "a7", operation: Operation.add, result: 9)
add(locationString: "b7c7", operation: Operation.subtract, result: 5)
add(locationString: "d7d8", operation: Operation.add, result: 3)

add(locationString: "a8a9b9", operation: Operation.add, result: 13)
add(locationString: "b8c8", operation: Operation.add, result: 11)
add(locationString: "e8e9f8f9", operation: Operation.add, result: 27)
add(locationString: "g8g9", operation: Operation.add, result: 10)
add(locationString: "h8h9", operation: Operation.add, result: 10)
add(locationString: "i8i9", operation: Operation.subtract, result: 4)

add(locationString: "c9d9", operation: Operation.add, result: 8)

print("Added Groups");


board.addPermutations();

print("Added Permutations");


var iteration = 0;


func t(g: Int, p: Int) -> (Bool, [(Int, Int)]) {
    iteration += 1;
    
    if board.tryPermutation(i_g: g, i_p: p) {
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


let solution = t(g: 0, p: 0);
print("Found valid board in", iteration, "tries");
print(board);
print(board.isValid());
print(board.allValid());
