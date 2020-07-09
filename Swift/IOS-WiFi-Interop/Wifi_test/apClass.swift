//
//  apClass.swift
//  Wifi_test
//
//  Created by Sierra on 2018-12-11.
//  Copyright © 2018 Sierra. All rights reserved.
//

import Foundation

public enum MCstatusID{
    
    case not_connected
    case connecting_Phase1
    case connecting_Phase2
    case connected
   
    
    case connecting_default_phase1
    case connecting_default_phase2
    case connected_default
}

public enum statusID{
    case not_connected
    case connecting_Phase1
    case connecting_Phase2
    case connected
}

class ApClass{
    
    public init() {
        self.SSID = ""
        self.username = ""
        self.password = ""
        self.type = ""
        self.status = .not_connected
    }
    public init(SSID:String, username:String, password:String, type:String, status:statusID) {
        self.SSID = SSID
        self.username = username
        self.password = password
        self.type = type
        self.status = status
    }
    
    var SSID : String
    var username : String
    var password : String
    var type : String
    var status : statusID
}

public func statusString_Convert(statusID:statusID) -> String{
    var statusString : String!
    if statusID == .not_connected{ statusString = "-"}
    else if statusID == .connecting_Phase1 || statusID == .connecting_Phase2{statusString = "Connecting..."}
    else if statusID == .connected{statusString = "Connected"}
    return statusString
}

public func stringStatus_Convert(statusString:String) -> statusID{
    var statusID : statusID!
    if statusString == "-" { statusID = .not_connected}
    else if statusString == "Connecting..." {statusID = .connecting_Phase1}
    else if statusString == "Connected" {statusID = .connected}
    return statusID
}
