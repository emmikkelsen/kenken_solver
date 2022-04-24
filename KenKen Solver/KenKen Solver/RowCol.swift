//
//  RowCol.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/18/22.
//

import Foundation


protocol RowColProt {
    func contains(_ member: Int) -> Bool;
    @discardableResult mutating func remove(_ member: Int) -> Int?;
    @discardableResult mutating func insert(_ newMember: Int) -> (inserted: Bool, memberAfterInsert: Int);
}


struct RowCol1: RowColProt {
    
    private var arr: [Bool];
    init(_ size: Int) {
        self.arr = Array.init(repeating: false, count: size);
    }
    
    @inlinable func contains(_ value: Int) -> Bool {
        return self.arr[value-1] == true;
    }
    
    @inlinable mutating func insert(_ value: Int) -> (inserted: Bool, memberAfterInsert: Int) {
        self.arr[value-1] = true;
        return (inserted: true, memberAfterInsert: value);
    }
    
    @inlinable mutating func remove(_ value: Int) -> Int? {
        self.arr[value-1] = false;
        return nil;
    }
}

struct RowCol3: RowColProt {
    
    private var arr: [Bool];
    init(_ size: Int) {
        self.arr = Array.init(repeating: false, count: size);
    }
    
    func contains(_ value: Int) -> Bool {
        return self.arr[value-1] == true;
    }
    
    mutating func insert(_ value: Int) -> (inserted: Bool, memberAfterInsert: Int) {
        self.arr[value-1] = true;
        return (inserted: true, memberAfterInsert: value);
    }
    
    mutating func remove(_ value: Int) -> Int? {
        self.arr[value-1] = false;
        return nil;
    }
}


class RowCol2: RowColProt {
    private var arr: [Bool];
    init(_ size: Int) {
        self.arr = Array.init(repeating: false, count: size);
    }
    
    @inlinable func contains(_ value: Int) -> Bool {
        return self.arr[value-1] == true;
    }
    
    @inlinable func insert(_ value: Int) -> (inserted: Bool, memberAfterInsert: Int) {
        self.arr[value-1] = true;
        return (inserted: true, memberAfterInsert: value);
    }
    
    @inlinable func remove(_ value: Int) -> Int? {
        self.arr[value-1] = false;
        return nil;
    }
}


typealias RowColSet = Set<Int>;


extension Set: RowColProt where Element == Int {
    
}
