//
//  timerView.swift
//  Wifi_test
//
//  Created by Sierra on 2018-12-12.
//  Copyright © 2018 Sierra. All rights reserved.
//

import UIKit
import NetworkExtension
import SystemConfiguration.CaptiveNetwork

class timerView: UIViewController {
    
    var ApArray = [ApClass]()
    var timer = Timer()
    var ApArraySize : Int! = 21
    
    var pinger: SimplePing?
    let hostName : String! = "google.com"
    var sentTime : TimeInterval = 0
    var pingRecevied : Bool! = false
    var failPingCount : Int! = 0
    
    var timerString : String! = "00:00:00"
    var seconds : Int! = 0
    var lastB : Int! = 0
    var currentB : Int! = 0
    var mode = "ALEOS"
    
    var timeout = 15
    var checktime = 13
    let failPingMax = 6
    
    let salmon = UIColor(red:250/255,green:128/255,blue:114/255,alpha:1.0)
    let ocean = UIColor(red:0/255, green:64/255, blue:128/255, alpha:1.0)
    
    override func viewDidLoad() {super.viewDidLoad()}
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        self.timer.invalidate()
        self.removeAllssid()
        self.ApArray.removeAll()
    }
    // initiaze table view and UI
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        self.removeAllssid()
        self.table.delegate = self
        self.table.dataSource = self
        
        if self.mode == "ALEOS"{self.createApArray_ALEOS()}
        else{self.createApArray_MGOS()}
        
        self.segment_control.layer.cornerRadius = 0.0
        self.segment_control.layer.borderWidth = 2
        self.segment_control.layer.borderColor = UIColor.white.cgColor
        let font = UIFont.systemFont(ofSize: 20)
        self.segment_control.setTitleTextAttributes([NSAttributedString.Key.font: font], for: .normal)
        self.segment_control.setTitle("ALEOS", forSegmentAt: 0)
        self.segment_control.setTitle("MGOS", forSegmentAt: 1)
        
        self.table.reloadData()
        self.timer.invalidate()
    }
    
    @IBOutlet weak var table: UITableView!
    @IBOutlet var segment_control: UISegmentedControl!
    
    // Button Handler function
    // Reset UI and state machine and start AP connection of selected cell
    @IBAction func button(_ sender: UIButton) {
        self.log(input: "Test Start...")
        self.timer.invalidate()
        NEHotspotConfigurationManager.shared.removeConfiguration(forSSID: self.ApArray[self.currentB].SSID)
        self.lastB = self.currentB
        self.currentB = sender.tag
        self.ApArray[self.lastB].status = .not_connected
        self.ApArray[self.currentB].status = .connecting_Phase1
       
        self.failPingCount = 0
        self.seconds = self.timeout
        let (h,m,s) = self.secondsToHoursMinutesSeconds(seconds:self.seconds)
        self.timerString = h + ":" + m + ":" + s
        
        let lastindexPath = IndexPath(row: self.lastB, section: 0)
        let indexPath = IndexPath(row: self.currentB, section: 0)
        let lastCell = self.table.cellForRow(at: lastindexPath) as? ApCell
        let Cell = self.table.cellForRow(at: indexPath) as? ApCell
        lastCell?.button?.setTitle("Connect", for: UIControl.State.normal)
        lastCell?.button?.setTitleColor(self.ocean, for: UIControl.State.normal)
        lastCell?.button?.backgroundColor = UIColor.white
        lastCell?.status?.text = "Status: " + statusString_Convert(statusID: self.ApArray[self.lastB].status)
        Cell?.button?.setTitle(self.timerString, for: UIControl.State.normal)
        Cell?.button?.setTitleColor(UIColor.white, for: UIControl.State.normal)
        Cell?.button?.backgroundColor = self.salmon
        Cell?.status?.text = "Status: " + statusString_Convert(statusID: self.ApArray[self.currentB].status)
        // calls clock() CORE state machine
        self.timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.clock), userInfo: nil, repeats: true)
        RunLoop.main.add(self.timer, forMode: RunLoop.Mode.common)
    }
    
    // load test case for ALEOS or MGOS
    @IBAction func change_mode(_ sender: Any) {
        self.timer.invalidate()
        self.removeAllssid()
        self.ApArray.removeAll()
        if segment_control.selectedSegmentIndex == 0 {self.mode = "ALEOS";self.createApArray_ALEOS()}
        else{self.mode = "MGOS";self.createApArray_MGOS()}
        self.table.reloadData()
    }
    
    // CORE state machine
    // Ran at 1s cycles after button action function is called
    @objc func clock(){
        //initial connection phase: Create AP object and apply configuration manager
        if self.ApArray[self.currentB].status == .connecting_Phase1{
            self.seconds -= 1
            self.updateClockbtn()
            
            if self.seconds < 0 {self.timeout_func()}
            else if self.seconds % self.checktime == 0 && self.seconds != self.timeout && self.seconds != 0 {
                let SSID = self.ApArray[self.currentB].SSID
                let passphrase = self.ApArray[self.currentB].password
                self.log(input: "Trying to connect to " + SSID)
                // Call NEHotspotConfiguration class to create ap object
                //https://developer.apple.com/documentation/networkextension/nehotspotconfiguration
                var hotspotConfig = NEHotspotConfiguration(ssid: SSID, passphrase: passphrase, isWEP: false)
                if self.ApArray[self.currentB].type == "OPEN"{hotspotConfig = NEHotspotConfiguration(ssid: SSID)}
                else if self.ApArray[self.currentB].type == "EAP" {
                    // EAP SSID CONNECTION CONFIG
                    let eapSetting1 = NEHotspotEAPSettings()
                    eapSetting1.username = self.ApArray[self.currentB].username
                    eapSetting1.password = passphrase
                    eapSetting1.trustedServerNames  = ["sierrawireless.qa.server"]
                    eapSetting1.supportedEAPTypes = [NEHotspotEAPSettings.EAPType.EAPPEAP.rawValue] as [NSNumber]
                    hotspotConfig = NEHotspotConfiguration(ssid: SSID, eapSettings: eapSetting1)
                }
                self.timer.invalidate()
                self.view.isUserInteractionEnabled = false
                UIApplication.shared.beginIgnoringInteractionEvents()
                // appy NEHostsoptconfiguration
                NEHotspotConfigurationManager.shared.apply(hotspotConfig) { (error) in
                    if let error = error {
                        if error.localizedDescription == "already associated."{self.ApArray[self.currentB].status = .connecting_Phase2}
                        self.timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.clock), userInfo: nil, repeats: true)
                        RunLoop.main.add(self.timer, forMode: RunLoop.Mode.common)
                        print("error = ",error)
                    }
                    else {
                        self.log(input: "Device applied SSID: " + self.ApArray[self.currentB].SSID + ", Attempting to Ping...")
                        self.ApArray[self.currentB].status = .connecting_Phase2
                        self.timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.clock), userInfo: nil, repeats: true)
                        RunLoop.main.add(self.timer, forMode: RunLoop.Mode.common)
                    }
                }
            }
        }
        // Connection phase 2: ping monitor
        // Ping host name until connected
        // if success transition to phase connected
        // else return to connection phase 1
        else if self.ApArray[self.currentB].status == .connecting_Phase2{
            self.view.isUserInteractionEnabled = true
            UIApplication.shared.endIgnoringInteractionEvents()
            self.seconds -= 1
            self.updateClockbtn()
            if self.seconds < 0 {self.timeout_func()}
            else{
                var connected_wifi = false
                self.PingStart()
                if self.pingRecevied{self.pingRecevied = false; self.PingStop();connected_wifi = true}
                if connected_wifi{
                    self.ApArray[self.currentB].status = .connected
                    self.seconds = 0
                    self.failPingCount = 0
                    self.updateClockbtn()
                    let Cell = self.table.cellForRow(at: IndexPath(row: self.currentB, section: 0)) as? ApCell
                    Cell?.status?.text = "Status: " + statusString_Convert(statusID: self.ApArray[self.currentB].status)
                    self.log(input: "Device Connected to Wifi " + self.ApArray[self.currentB].SSID)
                }
                //else{ self.failPingCount += 1; if self.failPingCount >= self.failPingMax{self.timeout_func()} }
            }
        }
        // connection phase connected: ping monitor
        // ping host name forever until max ping failuress
        else if self.ApArray[self.currentB].status == .connected {
            self.PingStart()  // Check Ping forever
            if self.pingRecevied {
                self.pingRecevied = false
                self.PingStop()
                self.failPingCount = 0
                self.log(input: "Ping to Host: " + self.hostName + " is Good!")
            }
            else {
                self.failPingCount += 1
                self.log(input: "Ping failed! Current Ping Fail count: " + "\(String(describing: self.failPingCount!))")
            }
            if self.failPingCount >= self.failPingMax { self.timeout_func() }
            self.seconds += 1
            self.updateClockbtn()
        }
    }//clock()
    
    // remove ssid configured by app only
    func removeAllssid(){
        self.failPingCount = 0
        NEHotspotConfigurationManager.shared.getConfiguredSSIDs { (ssidsArray) in
            for ssid in ssidsArray {
                self.log(input: "Disconnecting from: " + ssid)
                NEHotspotConfigurationManager.shared.removeConfiguration(forSSID: ssid)
            }
        }
    }
    
    // UI and state machine reset
    func timeout_func(){
        NEHotspotConfigurationManager.shared.removeConfiguration(forSSID: self.ApArray[self.currentB].SSID)
        self.seconds = self.timeout
        let (h,m,s) = self.secondsToHoursMinutesSeconds(seconds:self.seconds)
        self.timerString = h + ":" + m + ":" + s
        self.failPingCount = 0
        self.ApArray[self.currentB].status = .not_connected
        let indexPath = IndexPath(row: self.currentB, section: 0)
        let Cell = self.table.cellForRow(at: indexPath) as? ApCell
        Cell?.button?.setTitle("Connect", for: UIControl.State.normal)
        Cell?.button?.setTitleColor(self.ocean, for: UIControl.State.normal)
        Cell?.button?.backgroundColor = UIColor.white
        Cell?.status?.text = "Status: " + statusString_Convert(statusID: self.ApArray[self.currentB].status)
        self.lastB = self.currentB
        self.currentB += 1
        if self.currentB >= self.ApArray.count{self.currentB = 0}
        self.ApArray[self.currentB].status = .connecting_Phase1
        let NextindexPath = IndexPath(row: self.currentB, section: 0)
        let NextCell = self.table.cellForRow(at: NextindexPath) as? ApCell
        NextCell?.status?.text = "Status: " + statusString_Convert(statusID: self.ApArray[self.currentB].status)
        NextCell?.button?.setTitle(self.timerString, for: UIControl.State.normal)
        NextCell?.button?.setTitleColor(UIColor.white, for: UIControl.State.normal)
        NextCell?.button?.backgroundColor = self.salmon
        self.log(input: "Timed out at SSID: " + self.ApArray[self.lastB].SSID)
        self.log(input: "Starting next SSID: " + self.ApArray[self.currentB].SSID)
    }
    
    func log(input: String){
        let date = Date()
        let formatter = DateFormatter()
        formatter.dateFormat = "dd.MM.yyyy hh:mm:ss"
        let Dateresult = formatter.string(from: date)
        let timestamp = Dateresult
        print("[" + timestamp + "] " + input)
    }
    
    func updateClockbtn(){
        let (h,m,s) = self.secondsToHoursMinutesSeconds(seconds:self.seconds)
        self.timerString = h + ":" + m + ":" + s
        let indexPath = IndexPath(row: self.currentB, section: 0)
        let Cell = self.table.cellForRow(at: indexPath) as? ApCell
        Cell?.button?.setTitle(self.timerString, for: UIControl.State.normal)
    }
    
    func createApArray_ALEOS(){
        self.ApArray.removeAll()
        self.ApArray.append(ApClass(SSID:"Airport1", username:"", password:"", type:"OPEN", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport2", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport3", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport4", username:"", password:"", type:"OPEN", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport5", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport6", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport7", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport8", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport9", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport10", username:"", password:"", type:"OPEN", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport11", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport12", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport13", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport14", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport15", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport16", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport17", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport18", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"Airport19", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
    }
    
    func createApArray_MGOS(){
        self.ApArray.removeAll()
        self.ApArray.append(ApClass(SSID:"MG_AP1", username:"", password:"", type:"OPEN", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP2", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP3", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP4", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP5", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP6", username:"", password:"", type:"OPEN", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP7", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP8", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP9", username:"", password:"", type:"OPEN", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP10", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP11", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP12", username:"", password:"", type:"OPEN", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP13", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP14", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP15", username:"", password:"", type:"OPEN", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP16", username:"", password:"1234567890", type:"WPA/WPA2", status:.not_connected))
        self.ApArray.append(ApClass(SSID:"MG_AP17", username:"peapuser", password:"newworld", type:"EAP", status:.not_connected))

    }
    
    func secondsToHoursMinutesSeconds (seconds : Int) -> (String, String, String) {
        let h = seconds / 3600; let m = (seconds % 3600) / 60; let s = (seconds % 3600) % 60
        var hSting = "\(h)"; var mSting = "\(m)"; var sSting = "\(s)"
        if h < 10{ hSting = "0" + "\(h)" }; if m < 10{ mSting = "0" + "\(m)" }; if s < 10{ sSting = "0" + "\(s)" }
        return (hSting, mSting, sSting)
    }
}

// Extenstion for TableView functions
extension timerView: UITableViewDelegate, UITableViewDataSource{
    
    // Return number of cells in table
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {return ApArray.count}
    
    // Load cells with class Apclass: UITableViewCell
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ApCell", for: indexPath) as! ApCell
        cell.selectionStyle = UITableViewCell.SelectionStyle.none
        cell.SSID?.text = "SSID: " + self.ApArray[indexPath.row].SSID
        cell.button?.tag = indexPath.row
        cell.button?.layer.cornerRadius = 5
        
        if self.ApArray[indexPath.row].status != .not_connected {
            cell.button?.setTitle(self.timerString, for: UIControl.State.normal)
            cell.button?.setTitleColor(UIColor.white, for: UIControl.State.normal)
            cell.button?.backgroundColor = self.salmon
            cell.status?.text = "Status: " + statusString_Convert(statusID: self.ApArray[indexPath.row].status)
        }
        else{
            cell.button?.backgroundColor = UIColor.white
            cell.button?.setTitleColor(self.ocean, for: UIControl.State.normal)
            cell.button?.setTitle("Connect", for: UIControl.State.normal)
            cell.status?.text = "Status: " + statusString_Convert(statusID: self.ApArray[indexPath.row].status)
        }
        return cell
    }
    // set cells to be editable
    func tableView(_ tableView: UITableView, canEditRowAt indexPath: IndexPath) -> Bool {return false}
    // Set Cell height
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat{return 75}
    // Delete and edit fields
    func tableView(_ tableView: UITableView, editActionsForRowAt: IndexPath) -> [UITableViewRowAction]? {return nil}
}

class ApCell: UITableViewCell {
    @IBOutlet public var SSID: UILabel?
    @IBOutlet public var status: UILabel?
    @IBOutlet public var button: UIButton?
    // Initializer
    public func configure(_ ssid: String, status: String) {
        self.SSID?.text = "SSID: "
        self.status?.text = "Status: "
    }
}
