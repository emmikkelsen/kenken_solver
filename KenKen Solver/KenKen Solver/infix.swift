//
//  infix.swift
//  KenKen Solver
//
//  Created by Emil Bach Mikkelsen on 4/14/22.
//

import Foundation;


precedencegroup PowerPrecedence { higherThan: MultiplicationPrecedence }
infix operator ** : PowerPrecedence
func ** (radix: Int, power: Int) -> Int {
    guard power > 0 else {
        return 0;
    }
    return Array(repeating: radix, count: power).reduce(1, *)
}
func ** (radix: Double, power: Double) -> Double {
    return pow(radix, power);
}
