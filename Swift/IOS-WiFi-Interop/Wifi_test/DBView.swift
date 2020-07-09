//
//  ViewController.swift
//  Wifi_test
//
//  Created by Sierra on 2018-12-11.
//  Copyright © 2018 Sierra. All rights reserved.
//

import UIKit
import Firebase
import NetworkExtension
import SystemConfiguration.CaptiveNetwork

class DBView: UIViewController {
    
    var ref: DatabaseReference!
    var MCstatus : MCstatusID! = .not_connected
    var Ap = ApClass()
    var DefaultAp = ApClass()
    var timer = Timer()
    
    var pinger: SimplePing?
    let hostName : String! = "google.com"
    var sentTime : TimeInterval = 0
    var pingRecevied : Bool! = false
    var failPingCount : Int! = 0
    let failCountMax = 5
    
    var timerString : String! = "00:00:00"
    var seconds : Int! = 0
    
    
    override func viewDidLoad() {super.viewDidLoad()}
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        self.UIreset()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        self.ref = Database.database().reference()
        self.UIreset()
        self.pingRecevied = false
        self.startButton.isUserInteractionEnabled = true
        
        self.DefaultAp = ApClass(SSID:"SWI-MOBILE", username:"", password:"@irPr1m3", type:"WPA2-Personal", status:.not_connected)
        self.defautSSIDLable.text = self.DefaultAp.SSID
        self.defautpwdLable.text = self.DefaultAp.password
    }
    
    @IBOutlet var timerLable: UILabel!
    @IBOutlet var sysStatus: UILabel!
    @IBOutlet var connectionLable: UILabel!
    @IBOutlet var ssidLable: UILabel!
    @IBOutlet var typeLable: UILabel!
    @IBOutlet var pwdLable: UILabel!
    @IBOutlet var statusLable: UILabel!
    @IBOutlet var defautSSIDLable: UILabel!
    @IBOutlet var defautpwdLable: UILabel!
    @IBOutlet var startButton: UIButton!
    
    @IBAction func start(_ sender: UIButton) {
        self.timer.invalidate()
        self.removeAllssid()
        self.failPingCount = 0
        self.seconds = 0
        let (h,m,s) = self.secondsToHoursMinutesSeconds(seconds:self.seconds)
        self.timerString = h + ":" + m + ":" + s
        self.timerLable.text = self.timerString
        
        self.DefaultAp.status = .not_connected
        self.Ap.status = .not_connected
        self.MCstatus = .connecting_default_phase1
        self.startButton.isUserInteractionEnabled = false
        self.timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.clock), userInfo: nil, repeats: true)
        RunLoop.main.add(self.timer, forMode: RunLoop.Mode.common)
    }
    
    @IBAction func stop(_ sender: UIButton) {
        self.UIreset()
    }
    
    @IBAction func clock() {
        
        if self.MCstatus == .connecting_default_phase1 {
            self.sysStatus.text = "Connecting to Default AP"
            let hotspotConfig = NEHotspotConfiguration(ssid: self.DefaultAp.SSID, passphrase: self.DefaultAp.password, isWEP: false)
            NEHotspotConfigurationManager.shared.apply(hotspotConfig) { (error) in
                if let error = error {print("error = ",error)}
                else {
                    self.log(input: "Connecting to Default AP")
                    self.DefaultAp.status = .connecting_Phase1
                    self.MCstatus = .connecting_default_phase2
                    self.failPingCount = 0
                }
            }
        }
        else if self.MCstatus == .connecting_default_phase2 {
            self.sysStatus.text = "Ping internet..."
            self.PingStart()
            if self.pingRecevied {
                self.sysStatus.text = "Ping Successful"
                self.PingStop()
                self.DefaultAp.status = .connected
                self.MCstatus = .connected_default
                self.failPingCount = 0
            }
            else{
                self.failPingCount += 1
                if self.failPingCount >= self.failCountMax {
                    self.sysStatus.text = "Max Ping failure reached, reconnecting to default."
                    self.PingStop()
                    self.removeAllssid()
                    self.DefaultAp.status = .not_connected
                    self.MCstatus = .connecting_default_phase1
                }
            }
        }
        else if self.MCstatus == .connected_default {
            self.sysStatus.text = "Loading Firebase Data"
            self.LoadData()
            if self.Ap.SSID == ""{
                self.MCstatus = .connected_default
            }
            else{
                self.removeAllssid()
                self.MCstatus = .not_connected
            }
        }
        else if self.MCstatus == .not_connected {
            self.sysStatus.text = "Disconnecting from default Ap"
            self.MCstatus = .connecting_Phase1
        }
        else if self.MCstatus == .connecting_Phase1 {
            self.sysStatus.text = "Connecting to Ap: " + self.Ap.SSID
            self.Ap.status = .connecting_Phase1
            
            let SSID = self.Ap.SSID
            let passphrase = self.Ap.password
            let username = self.Ap.username
            
            //https://developer.apple.com/documentation/networkextension/nehotspotconfiguration
            var  hotspotConfig = NEHotspotConfiguration(ssid: SSID, passphrase: passphrase, isWEP: false)
            
            if self.Ap.type == "OPEN"{hotspotConfig = NEHotspotConfiguration(ssid: SSID)}
            else if self.Ap.type == "EAP" {
                let eapSetting1 = NEHotspotEAPSettings()
                eapSetting1.username = username
                eapSetting1.password = passphrase
                eapSetting1.trustedServerNames  = ["sierrawireless.qa.server"]
                eapSetting1.supportedEAPTypes = [NEHotspotEAPSettings.EAPType.EAPPEAP.rawValue] as [NSNumber]
                hotspotConfig = NEHotspotConfiguration(ssid: SSID, eapSettings: eapSetting1)
            }
            
            NEHotspotConfigurationManager.shared.apply(hotspotConfig) { (error) in
                if let error = error {
                    if error.localizedDescription == "already associated."{self.MCstatus = .connecting_Phase2}
                    print("error = ",error)
                }
                else {
                    self.MCstatus = .connecting_Phase2
                    self.Ap.status = .connecting_Phase2
                    self.failPingCount = 0
                }
            }
        }
        else if self.MCstatus == .connecting_Phase2 {
            self.sysStatus.text = "Ping internet from Ap"
            self.PingStart()
            if self.pingRecevied {
                self.sysStatus.text = "Ping Successful"
                self.PingStop()
                self.Ap.status = .connected
                self.MCstatus = .connected
                self.failPingCount = 0
            }
            else{
                self.failPingCount += 1
                if self.failPingCount >= self.failCountMax {
                    self.sysStatus.text = "Max Ping failure reached, reconnecting to default."
                    self.PingStop()
                    self.removeAllssid()
                    self.Ap.status = .not_connected
                    self.MCstatus = .connecting_default_phase1
                }
            }
        }
        else if self.MCstatus == .connected {
            self.sysStatus.text = "Connected to AP: " + self.Ap.SSID
            self.PingStart()
            if self.pingRecevied {
                self.PingStop()
                self.failPingCount = 0
            }
            else{
                self.failPingCount += 1
                if self.failPingCount >= self.failCountMax {
                    self.sysStatus.text = "Max Ping failure reached, reconnecting to default."
                    self.PingStop()
                    self.removeAllssid()
                    self.Ap.status = .not_connected
                    self.MCstatus = .connecting_default_phase1
                }
            }
        }

        self.getWifiSSID()
        self.seconds += 1
        let (h,m,s) = self.secondsToHoursMinutesSeconds(seconds:self.seconds)
        self.timerString = h + ":" + m + ":" + s
        self.timerLable.text = self.timerString
    }
    
    func LoadData(){
        var activeSSID = NSDictionary()
        self.ref.observeSingleEvent(of: .value, with: { (snapshot) in
            for child in snapshot.children {
                let snap = child as! DataSnapshot
                let key = snap.key
                let value = snap.value
                if key == "active_ssid"{activeSSID = value as! NSDictionary}
                //print("key = \(key)  value = \(value!)")
            }
            // load into data
            self.Ap.SSID = activeSSID["ssid"] as! String? ?? ""
            self.Ap.username = activeSSID["username"] as! String? ?? ""
            self.Ap.password = activeSSID["password"] as! String? ?? ""
            self.Ap.type = activeSSID["type"] as! String? ?? ""
        })
    }
    
    @IBAction func getWifiSSID(){
        var ssid : String! = ""
        if let interfaces = CNCopySupportedInterfaces() as NSArray? {
            for interface in interfaces {
                if let interfaceInfo = CNCopyCurrentNetworkInfo(interface as! CFString) as NSDictionary? {
                    ssid = interfaceInfo[kCNNetworkInfoKeySSID as String] as? String
                    break
                }
            }
        }
        
        if ssid == "" {
            self.connectionLable.text =  "-"
            self.ssidLable.text = "-"
            self.pwdLable.text = "-"
            self.typeLable.text = "-"
            self.statusLable.text = "-"
        }
        else if ssid == self.DefaultAp.SSID {
            self.connectionLable.text = ssid
            self.ssidLable.text = self.DefaultAp.SSID
            self.pwdLable.text = self.DefaultAp.password
            self.typeLable.text = self.DefaultAp.type
            self.statusLable.text = statusString_Convert(statusID: self.DefaultAp.status)
        }
        else if ssid == self.Ap.SSID {
            self.connectionLable.text = ssid
            self.ssidLable.text = self.Ap.SSID
            self.pwdLable.text = self.Ap.password
            self.typeLable.text = self.Ap.type
            self.statusLable.text = statusString_Convert(statusID: self.Ap.status)
        }
    }
    
    func removeAllssid(){
        self.DefaultAp.status = .not_connected
        self.Ap.status = .not_connected
        NEHotspotConfigurationManager.shared.getConfiguredSSIDs { (ssidsArray) in
            for ssid in ssidsArray {NEHotspotConfigurationManager.shared.removeConfiguration(forSSID: ssid)}
        }
    }
    
    func UIreset(){
        self.removeAllssid()
        self.timer.invalidate()
        self.MCstatus = .connecting_default_phase1
        self.Ap = ApClass()
        self.pingRecevied = false
       
        self.sysStatus.text = "-"
        self.connectionLable.text = "-"
        self.ssidLable.text = "-"
        self.pwdLable.text = "-"
        self.typeLable.text = "-"
        self.statusLable.text = "-"
        
        self.failPingCount = 0
        self.seconds = 0
        let (h,m,s) = self.secondsToHoursMinutesSeconds(seconds:self.seconds)
        self.timerString = h + ":" + m + ":" + s
        self.timerLable.text = self.timerString
        self.startButton.isUserInteractionEnabled = true
    }
    
    func log(input: String){
        let date = Date()
        let formatter = DateFormatter()
        formatter.dateFormat = "dd.MM.yyyy hh:mm:ss"
        let Dateresult = formatter.string(from: date)
        let timestamp = Dateresult
        print("[" + timestamp + "] " + input)
    }
    
    func secondsToHoursMinutesSeconds (seconds : Int) -> (String, String, String) {
        let h = seconds / 3600; let m = (seconds % 3600) / 60; let s = (seconds % 3600) % 60
        var hSting = "\(h)"; var mSting = "\(m)"; var sSting = "\(s)"
        if h < 10{ hSting = "0" + "\(h)" }; if m < 10{ mSting = "0" + "\(m)" }; if s < 10{ sSting = "0" + "\(s)" }
        return (hSting, mSting, sSting)
    }
}
