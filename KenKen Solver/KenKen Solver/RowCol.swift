//
//  RowCol.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/18/22.
//

import Foundation


protocol RowColProt {
    func contains(_ value: Int) -> Bool;
    mutating func remove(_ value: Int);
    mutating func insert(_ value: Int);
}


struct RowCol1: RowColProt {
    private var arr: [Bool];
    init(_ size: Int) {
        self.arr = Array.init(repeating: false, count: size);
    }
    
    func contains(_ value: Int) -> Bool {
        return self.arr[value-1] == true;
    }
    
    mutating func insert(_ value: Int) {
        self.arr[value-1] = true;
    }
    
    mutating func remove(_ value: Int) {
        self.arr[value-1] = false;
    }
}


class RowCol2: RowColProt {
    private var arr: [Bool];
    init(_ size: Int) {
        self.arr = Array.init(repeating: false, count: size);
    }
    
    func contains(_ value: Int) -> Bool {
        return self.arr[value-1] == true;
    }
    
    func insert(_ value: Int) {
        self.arr[value-1] = true;
    }
    
    func remove(_ value: Int) {
        self.arr[value-1] = false;
    }
}


typealias RowCol3 = Set<Int>;
