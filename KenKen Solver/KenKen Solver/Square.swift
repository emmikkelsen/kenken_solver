//
//  Square.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

struct Square: CustomStringConvertible {
    var value: Int;

    init() {
        self.value = 0;
    }
    
    var description: String {
        return "[\(self.value)]";
    }
}
