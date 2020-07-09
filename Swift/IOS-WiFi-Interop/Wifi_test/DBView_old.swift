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
    var timer2 = Timer()
    
    var pinger: SimplePing?
    let hostName : String! = "google.com"
    var sentTime : TimeInterval = 0
    var pingRecevied : Bool! = false
    var failPingCount : Int! = 0
    
    var timerString : String! = "00:00:00"
    var seconds : Int! = 0
    let failCountMax = 5
    
    override func viewDidLoad() {super.viewDidLoad()}
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        self.removeAllssid()
        self.timer.invalidate()
        self.timer2.invalidate()
        self.UIreset()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        self.timer.invalidate()
        self.timer2.invalidate()
        self.startButton.isUserInteractionEnabled = true
        self.removeAllssid()
        self.DefaultAp = ApClass(SSID:"SWI-MOBILE", username:"", password:"@irPr1m3", type:"-", status:.not_connected)
        self.defautSSIDLable.text = self.DefaultAp.SSID
        self.defautpwdLable.text = self.DefaultAp.password
        self.UIreset()
        self.pingRecevied = false
        
        self.timer2 = Timer.scheduledTimer(timeInterval: 5, target: self, selector: #selector(self.getWifiSSID), userInfo: nil, repeats: true)
        RunLoop.main.add(self.timer2, forMode: RunLoop.Mode.common)
        
        self.ref = Database.database().reference()
    }
    
    @IBOutlet var timerLable: UILabel!
    @IBOutlet var connectionLable: UILabel!
    @IBOutlet var sysStatus: UILabel!
    @IBOutlet var indexLable: UILabel!
    @IBOutlet var ssidLable: UILabel!
    @IBOutlet var typeLable: UILabel!
    @IBOutlet var statusLable: UILabel!
    @IBOutlet var defautSSIDLable: UILabel!
    @IBOutlet var defautpwdLable: UILabel!
    @IBOutlet var startButton: UIButton!
    
    @IBAction func start(_ sender: UIButton) {
        self.timer.invalidate()
        self.removeAllssid()
        
        let hotspotConfig = NEHotspotConfiguration(ssid: self.DefaultAp.SSID, passphrase: self.DefaultAp.password, isWEP: false)
        NEHotspotConfigurationManager.shared.apply(hotspotConfig) { (error) in
            if let error = error {print("error = ",error)}
            else {
                print("Connected to Default AP")
                self.DefaultAp.status = .connected
                self.timer = Timer.scheduledTimer(timeInterval: 2, target: self, selector: #selector(self.ping), userInfo: nil, repeats: true)
                RunLoop.main.add(self.timer, forMode: RunLoop.Mode.common)
                self.startButton.isUserInteractionEnabled = false
            }
        }
        
        
        self.seconds = 0
        let (h,m,s) = self.secondsToHoursMinutesSeconds(seconds:self.seconds)
        self.timerString = h + ":" + m + ":" + s
        self.timerLable.text = self.timerString
    }
    
    @IBAction func stop(_ sender: UIButton) {
        self.UIreset()
    }
    
    @IBAction func clock(){
        
        if self.MCstatus == .not_connected{
           
            // could have different config https://developer.apple.com/documentation/networkextension/nehotspotconfiguration
            var  hotspotConfig = NEHotspotConfiguration(ssid: self.Ap.SSID, passphrase: self.Ap.password, isWEP: false)
            if self.Ap.type == "open"{hotspotConfig = NEHotspotConfiguration(ssid: self.Ap.SSID)}
            else if self.Ap.type == "EAP" {
                let eapSetting1 = NEHotspotEAPSettings()
                eapSetting1.username = self.Ap.username
                eapSetting1.password = self.Ap.password
                eapSetting1.trustedServerNames  = ["sierrawireless.qa.server"]
                eapSetting1.supportedEAPTypes = [NEHotspotEAPSettings.EAPType.EAPPEAP.rawValue] as [NSNumber]
                hotspotConfig = NEHotspotConfiguration(ssid: self.Ap.SSID, eapSettings: eapSetting1)
            }
        
            NEHotspotConfigurationManager.shared.apply(hotspotConfig) { (error) in
                if let error = error {print("error = ",error)}
                else {
                    self.MCstatus = .connecting_Phase1
                    self.Ap.status = .connecting_Phase1
                }
            }
        }
        else if self.MCstatus == .connecting_Phase1{
            self.PingStart()
            if self.pingRecevied {
                self.PingStop()
                self.Ap.status = .connected
                self.MCstatus = .connected
            }
            else{
                self.failPingCount += 1
                if self.failPingCount >= self.failCountMax {
                    self.PingStop()
                    self.removeAllssid()
                    self.Ap.status = .not_connected
                    self.MCstatus = .connecting_default_phase1
                }
            }
        }
        else if self.MCstatus == .connected{
            self.sysStatus.text = "Connected to: " + self.Ap.SSID
            self.PingStart()
            if self.pingRecevied != true{
                self.failPingCount += 1
                if self.failPingCount >= self.failCountMax{
                    self.PingStop()
                    self.failPingCount = 0
                    self.Ap.status = .not_connected
                    self.MCstatus = .connecting_default_phase1
                    self.removeAllssid()
                    self.Ap = ApClass()
                }
            }
        }
        else if self.MCstatus == .connecting_default_phase1{
            self.sysStatus.text = "Lost Connection | Connecting to Default"
            let hotspotConfig = NEHotspotConfiguration(ssid: self.DefaultAp.SSID, passphrase: self.DefaultAp.password, isWEP: false)
            NEHotspotConfigurationManager.shared.apply(hotspotConfig) { (error) in
                if let error = error {
                    if error.localizedDescription == "already associated."{self.MCstatus = .connecting_Phase2}
                    print("error = ",error)
                }
                else { self.MCstatus = .connecting_default_phase2 }
            }
        }
        else if self.MCstatus == .connecting_default_phase2{
            self.PingStart()
            if self.pingRecevied{
                self.PingStop()
                self.DefaultAp.status = .connected
                self.MCstatus = .connected_default
            }
        }
        else if self.MCstatus == .connected_default{
            let blackAP = ApClass()
            if self.Ap.SSID != blackAP.SSID {
                self.MCstatus = .not_connected
                self.removeAllssid()
            }
        }
        self.seconds += 1
        let (h,m,s) = self.secondsToHoursMinutesSeconds(seconds:self.seconds)
        self.timerString = h + ":" + m + ":" + s
        self.timerLable.text = self.timerString
    }
    
    @IBAction func ping(){
        self.LoadData()
        
        if self.Ap.SSID != ""{
            self.MCstatus = .not_connected
            self.timer.invalidate()
            self.timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.clock), userInfo: nil, repeats: true)
            RunLoop.main.add(self.timer, forMode: RunLoop.Mode.common)
            self.removeAllssid()
        }
        else{self.sysStatus.text = "Retry Default Ping to internet..."}
    }
    
    func LoadData(){
        var activeSSID = NSDictionary()
//        var defaultSSID = NSDictionary()
        self.ref.observeSingleEvent(of: .value, with: { (snapshot) in
            for child in snapshot.children {
                let snap = child as! DataSnapshot
                let key = snap.key
                let value = snap.value

                if key == "active_ssid"{activeSSID = value as! NSDictionary}
//                else if key == "default_ssid"{defaultSSID = value as! NSDictionary}
//                print("key = \(key)  value = \(value!)")
            }
            
            // load into data
            self.Ap.SSID = activeSSID["ssid"] as! String? ?? ""
            self.Ap.username = activeSSID["username"] as! String? ?? ""
            self.Ap.password = activeSSID["password"] as! String? ?? ""
            self.Ap.type = activeSSID["type"] as! String? ?? ""

//            self.DefaultAp.SSID = defaultSSID["ssid"] as! String? ?? ""
//            self.DefaultAp.username = defaultSSID["username"] as! String? ?? ""
//            self.DefaultAp.password = defaultSSID["password"] as! String? ?? ""
//            self.DefaultAp.type = defaultSSID["type"] as! String? ?? ""
//            self.defautSSIDLable.text = self.DefaultAp.SSID
//            self.defautpwdLable.text = self.DefaultAp.password
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
            self.ssidLable.text =  "-"
            self.typeLable.text = "-"
            self.statusLable.text = "-"
            if self.Ap.SSID == "" {self.indexLable.text = "-"}
            else{self.indexLable.text = self.Ap.SSID }
            
        }
        else if ssid == self.DefaultAp.SSID {
            self.connectionLable.text = ssid
            self.ssidLable.text = self.DefaultAp.SSID
            self.typeLable.text = self.DefaultAp.type
            self.statusLable.text = statusString_Convert(statusID: self.DefaultAp.status)
            if self.Ap.SSID == "" {self.indexLable.text = "-"}
            else{self.indexLable.text = self.Ap.SSID }
            
            self.ref.observeSingleEvent(of: .value, with: { snapshot in
                let NSActiveSSID = snapshot.childSnapshot(forPath: "active_ssid").value as? NSDictionary
                self.Ap.SSID = NSActiveSSID?["SSID"] as! String? ?? ""
                self.Ap.username = NSActiveSSID?["username"] as! String? ?? ""
                self.Ap.password = NSActiveSSID?["password"] as! String? ?? ""
                self.Ap.type = NSActiveSSID?["type"] as! String? ?? ""
            })
        }
        else{
            if self.Ap.SSID == "" && ssid == "" {
                self.connectionLable.text =  "-"
                self.indexLable.text = "-"
                self.ssidLable.text = "-"
                self.typeLable.text = "-"
                self.statusLable.text = "-"
            }
            else{
                self.connectionLable.text = self.Ap.SSID
                self.indexLable.text = self.Ap.SSID
                self.ssidLable.text = self.Ap.SSID
                self.typeLable.text = self.Ap.type
                self.statusLable.text = statusString_Convert(statusID: self.Ap.status)
            }
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
        self.timer.invalidate()
        self.removeAllssid()
        self.MCstatus = .not_connected
        self.pingRecevied = false
        self.Ap = ApClass()
        self.sysStatus.text = "-"
        self.indexLable.text = "-"
        self.ssidLable.text = "-"
        self.typeLable.text = "-"
        self.statusLable.text = "-"
        self.connectionLable.text = "-"
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
