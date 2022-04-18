//
//  Location.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/15/22.
//


struct Location: Equatable, Hashable, CustomStringConvertible {
    var x: Int, y: Int;
    
    init(_ x: Int, _ y: Int) {
        self.x = x;
        self.y = y;
    }
    
    var description: String {
        return "(\(x), \(y))";
    }
}
