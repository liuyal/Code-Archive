//
//  ping.swift
//  Wifi_test
//
//  Created by Sierra on 2018-12-17.
//  Copyright © 2018 Sierra. All rights reserved.
//

import Foundation

extension timerView: SimplePingDelegate{

    /// Called by the table view selection delegate callback to start the ping.
    func PingStart() {
        NSLog("start")
        let pinger = SimplePing(hostName: self.hostName)
        self.pinger = pinger
        pinger.delegate = self
        pinger.start()
        return
    }
    /// Called by the table view selection delegate callback to stop the ping.
    func PingStop() {
        NSLog("stop")
        self.pinger?.stop()
        self.pinger = nil
        return
    }
    /// Sends a ping.
    /// Called to send a ping, both directly (as soon as the SimplePing object starts up) and
    /// via a timer (to continue sending pings periodically).
    func sendPing() {
        self.pinger!.send(with: nil)
    }
    
    // MARK: pinger delegate callback
    func simplePing(_ pinger: SimplePing, didStartWithAddress address: Data) {
        NSLog("pinging %@", timerView.displayAddressForAddress(address: address as NSData))
        self.sendPing()
    }
    func simplePing(_ pinger: SimplePing, didFailWithError error: Error) {
        NSLog("failed: %@", timerView.shortErrorFromError(error: error as NSError))
        self.pingRecevied = false
        self.PingStop()
    }
    func simplePing(_ pinger: SimplePing, didSendPacket packet: Data, sequenceNumber: UInt16) {
        sentTime = Date().timeIntervalSince1970
        self.pingRecevied = true
        NSLog("#%u sent", sequenceNumber)
    }
    func simplePing(_ pinger: SimplePing, didFailToSendPacket packet: Data, sequenceNumber: UInt16, error: Error) {
        self.pingRecevied = false
        NSLog("#%u send failed: %@", sequenceNumber, timerView.shortErrorFromError(error: error as NSError))
    }
    func simplePing(_ pinger: SimplePing, didReceivePingResponsePacket packet: Data, sequenceNumber: UInt16) {
        let some = Int(((Date().timeIntervalSince1970 - sentTime).truncatingRemainder(dividingBy: 1)) * 1000)
        self.pingRecevied = true
        NSLog("PING: \(some) MS")
        NSLog("#%u received, size=%zu", sequenceNumber, packet.count)
    }
    func simplePing(_ pinger: SimplePing, didReceiveUnexpectedPacket packet: Data) {
        NSLog("unexpected packet, size=%zu", packet.count)
    }
    
    // MARK: utilities
    /// Returns the string representation of the supplied address.
    /// - parameter address: Contains a `(struct sockaddr)` with the address to render.
    /// - returns: A string representation of that address.
    static func displayAddressForAddress(address: NSData) -> String {
        var hostStr = [Int8](repeating: 0, count: Int(NI_MAXHOST))
        let success = getnameinfo(address.bytes.assumingMemoryBound(to: sockaddr.self), socklen_t(address.length), &hostStr, socklen_t(hostStr.count),nil,0,NI_NUMERICHOST) == 0
        let result: String
        if success {result = String(cString: hostStr)}
        else {result = "?"}
        return result
    }
    
    /// Returns a short error string for the supplied error.
    /// - parameter error: The error to render.
    /// - returns: A short string representing that error.
    static func shortErrorFromError(error: NSError) -> String {
        if error.domain == kCFErrorDomainCFNetwork as String && error.code == Int(CFNetworkErrors.cfHostErrorUnknown.rawValue) {
            if let failureObj = error.userInfo[kCFGetAddrInfoFailureKey as String] {
                if let failureNum = failureObj as? NSNumber {
                    if failureNum.intValue != 0 {
                        let f = gai_strerror(Int32(failureNum.intValue))
                        if f != nil {return String(cString: f!)}
                    }
                }
            }
        }
        if let result = error.localizedFailureReason {return result}
        return error.localizedDescription
    }
}




extension DBView: SimplePingDelegate{
    
    /// Called by the table view selection delegate callback to start the ping.
    func PingStart() {
        NSLog("start")
        let pinger = SimplePing(hostName: self.hostName)
        self.pinger = pinger
        pinger.delegate = self
        pinger.start()
        return
    }
    /// Called by the table view selection delegate callback to stop the ping.
    func PingStop() {
        NSLog("stop")
        self.pinger?.stop()
        self.pinger = nil
        return
    }
    /// Sends a ping.
    /// Called to send a ping, both directly (as soon as the SimplePing object starts up) and
    /// via a timer (to continue sending pings periodically).
    func sendPing() {
        self.pinger!.send(with: nil)
    }
    
    // MARK: pinger delegate callback
    func simplePing(_ pinger: SimplePing, didStartWithAddress address: Data) {
        NSLog("pinging %@", timerView.displayAddressForAddress(address: address as NSData))
        self.sendPing()
    }
    func simplePing(_ pinger: SimplePing, didFailWithError error: Error) {
        NSLog("failed: %@", timerView.shortErrorFromError(error: error as NSError))
        self.pingRecevied = false
        self.PingStop()
    }
    func simplePing(_ pinger: SimplePing, didSendPacket packet: Data, sequenceNumber: UInt16) {
        sentTime = Date().timeIntervalSince1970
        self.pingRecevied = true
        NSLog("#%u sent", sequenceNumber)
    }
    func simplePing(_ pinger: SimplePing, didFailToSendPacket packet: Data, sequenceNumber: UInt16, error: Error) {
        self.pingRecevied = false
        NSLog("#%u send failed: %@", sequenceNumber, timerView.shortErrorFromError(error: error as NSError))
    }
    func simplePing(_ pinger: SimplePing, didReceivePingResponsePacket packet: Data, sequenceNumber: UInt16) {
        let some = Int(((Date().timeIntervalSince1970 - sentTime).truncatingRemainder(dividingBy: 1)) * 1000)
        self.pingRecevied = true
        NSLog("PING: \(some) MS")
        NSLog("#%u received, size=%zu", sequenceNumber, packet.count)
    }
    func simplePing(_ pinger: SimplePing, didReceiveUnexpectedPacket packet: Data) {
        NSLog("unexpected packet, size=%zu", packet.count)
    }
    
    // MARK: utilities
    /// Returns the string representation of the supplied address.
    /// - parameter address: Contains a `(struct sockaddr)` with the address to render.
    /// - returns: A string representation of that address.
    static func displayAddressForAddress(address: NSData) -> String {
        var hostStr = [Int8](repeating: 0, count: Int(NI_MAXHOST))
        let success = getnameinfo(address.bytes.assumingMemoryBound(to: sockaddr.self), socklen_t(address.length), &hostStr, socklen_t(hostStr.count),nil,0,NI_NUMERICHOST) == 0
        let result: String
        if success {result = String(cString: hostStr)}
        else {result = "?"}
        return result
    }
    
    /// Returns a short error string for the supplied error.
    /// - parameter error: The error to render.
    /// - returns: A short string representing that error.
    static func shortErrorFromError(error: NSError) -> String {
        if error.domain == kCFErrorDomainCFNetwork as String && error.code == Int(CFNetworkErrors.cfHostErrorUnknown.rawValue) {
            if let failureObj = error.userInfo[kCFGetAddrInfoFailureKey as String] {
                if let failureNum = failureObj as? NSNumber {
                    if failureNum.intValue != 0 {
                        let f = gai_strerror(Int32(failureNum.intValue))
                        if f != nil {return String(cString: f!)}
                    }
                }
            }
        }
        if let result = error.localizedFailureReason {return result}
        return error.localizedDescription
    }
}
