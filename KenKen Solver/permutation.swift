//
//  permutation.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//


func permutations(boardSize: Int, groupSize: Int, operation: Operation, result: Int) -> [[Int]] {
    if (operation == Operation.divide) {
        var maxes: [Int] = [];
        var mins: [Int] = [];
        
        for x in 1..<boardSize+1 {
            if (x % result == 0) {
                maxes.append(x);
                mins.append(x / result);
            }
        }
        
        var p: [[Int]] = [];
        
        for (ma, mi) in zip(maxes, mins) {
            p.append([ma, mi]);
            p.append([mi, ma]);
        }
        
        return p;
    }
    
    if (operation == Operation.subtract) {
        var maxes: [Int] = [];
        var mins: [Int] = [];
        
        for x in 1..<boardSize+1 {
            if (x > result) {
                maxes.append(x);
                mins.append(x - result);
            }
        }
        var p: [[Int]] = [];
        for (ma, mi) in zip(maxes, mins) {
            p.append([ma, mi]);
            p.append([mi, ma]);
        }
        return p;
    }
    
    if (operation == Operation.add) {
        return peAdd(boardSize: boardSize, result: result, groupSize: groupSize);
    }
        
    return peMultiply(boardSize: boardSize, result: result, groupSize: groupSize);
}


func peAdd(boardSize: Int, result: Int, groupSize: Int) -> [[Int]] {
    if (groupSize == 1) {
        return [[result]];
    }
    var t: [[Int]] = [];
    for x in 1..<boardSize+1 {
        if ((result - x) / (groupSize - 1) <= boardSize && result - x >= groupSize - 1) {
            for ss in peAdd(boardSize: boardSize, result: result - x, groupSize: groupSize - 1) {
                t.append(ss + [x])
            }
        }
    }
    
    return t;
}
    

func peMultiply(boardSize: Int, result: Int, groupSize: Int) -> [[Int]] {
    if (groupSize == 1) {
        return [[result]];
    }
    var t: [[Int]] = [];
    var factors: [Int] = [];
    for x in 1..<boardSize+1 {
        if (result % x == 0) {
            factors.append(x);
        }
    }
    for x in factors {
        if (result / x) <= boardSize^(groupSize - 1) {
            for ss in peMultiply(boardSize: boardSize, result: result / x, groupSize: groupSize - 1) {
                t.append(ss + [x])
            }
        }
    }
    
    return t;
}
  
