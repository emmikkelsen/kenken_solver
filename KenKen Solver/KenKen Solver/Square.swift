//
//  Square.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

class Square {
    private let location: (Int, Int);
    private var value: Int;

    init(location: (Int, Int)) {
        self.location = location;
        self.value = 0;
    }
    
    func setValue(value: Int) {
        self.value = value;
    }
    
    func getValue() -> Int {
        return self.value;
    }
    
    func getLocation() -> (Int, Int) {
        return self.location;
    }
}
