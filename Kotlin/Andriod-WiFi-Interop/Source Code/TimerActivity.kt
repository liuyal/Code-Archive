package com.example.jerliu.wifi_test

import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.support.design.widget.BottomNavigationView
import android.support.v7.app.AppCompatActivity
import android.support.v7.widget.LinearLayoutManager
import android.support.v7.widget.RecyclerView
import android.support.v7.widget.RecyclerView.ViewHolder
import android.support.v4.os.HandlerCompat.postDelayed
import android.view.LayoutInflater
import kotlinx.android.synthetic.main.activity_timer.*
import kotlinx.android.synthetic.main.cell_layout.*
import kotlinx.android.synthetic.main.cell_layout.view.*
import android.widget.TextView
import android.widget.LinearLayout
import android.widget.Toast
import android.widget.Button
import android.content.Intent
import android.graphics.Color
import android.net.wifi.WifiConfiguration
import android.net.wifi.WifiManager
import android.net.NetworkInfo
import android.net.ConnectivityManager
import android.net.wifi.WifiEnterpriseConfig
import android.util.Log
import com.example.jerliu.wifi_test.ApClass
import com.example.jerliu.wifi_test.statusID
import android.support.design.widget.TabLayout


fun statusID2String(input: statusID): String {
    var output = ""
    when{
        input == statusID.not_connected ->  output = "-x-"
        input == statusID.connecting_phase1 ->  output = "Connecting..."
        input == statusID.connecting_phase2 ->  output = "Connecting..."
        input == statusID.connected ->  output = "Connected"
    }

    return output
}

class TimerActivity : AppCompatActivity() {

    lateinit var tabLayout: TabLayout

    private val handler = Handler()
    val hostName = "google.com"
    var pingRecevied = false
    var failPingCount = 0
    val failPingMax = 6

    var seconds = 0
    var lastB = 0
    var currentB = 0

    val timeout = 15
    val checktime = 13

    var mode = "ALEOS"

    // bottom tab listener/handler
    private val mOnNavigationItemSelectedListener = BottomNavigationView.OnNavigationItemSelectedListener { item ->
        when (item.itemId) {
            R.id.navigation_home -> { return@OnNavigationItemSelectedListener true }
            R.id.navigation_dashboard -> {
                handler.removeCallbacksAndMessages(null)
                this.log("Timer Mode Stopped.")
                this.removeAllSSID()
                val intent = Intent(this, DBActivity::class.java)
                startActivity(intent)
                return@OnNavigationItemSelectedListener true
            }
        }
        false
    }

    override fun onStart() {
        super.onStart()
        this.removeAllSSID()
        MyApplication.ApArray = mutableListOf<ApClass>()
        if (this.mode == "MGOS"){ this.createTestAP_MGOS() }
        else{ this.createTestAP_ALEOS() }
        navigation1.getMenu().getItem(0).setChecked(true)
        recyclerView.adapter?.notifyDataSetChanged()
    }

    // Initialization of UI and data
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_timer)
        setTitle("Timer")
        tabLayout = findViewById(R.id.tab) as TabLayout
        this.removeAllSSID()
        navigation1.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener)
        recyclerView.setBackgroundColor(Color.WHITE)
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = MainAdapter { partItem: ApClass -> partItemClicked(partItem) }
        recyclerView.addItemDecoration(SimpleDividerItemDecoration(this))

        tabLayout.addOnTabSelectedListener(object : TabLayout.OnTabSelectedListener {
            val builder = (this@TimerActivity)
            override fun onTabSelected(tab: TabLayout.Tab) {
                builder.handler.removeCallbacksAndMessages(null)
                builder.removeAllSSID()

                MyApplication.ApArray = mutableListOf<ApClass>()

                if (tab.position == 0) {
                    builder.mode = "ALEOS"
                    builder.createTestAP_ALEOS()}
                else{
                    builder.mode = "MGOS"
                    builder.createTestAP_MGOS()
                }
                recyclerView.adapter?.notifyDataSetChanged()
            }

            override fun onTabUnselected(tab: TabLayout.Tab) {}

            override fun onTabReselected(tab: TabLayout.Tab) {}
        })
    }
    // Handles click of button labled connect
    private fun partItemClicked(partItem: ApClass) {

        this.log("Test Start...")
        handler.removeCallbacksAndMessages(null)
        this.removeAllSSID()
        val index = MyApplication.ApArray.indexOf(partItem)
        this.seconds = this.timeout + 1
        MyApplication.timerString = this.secondsToHoursMinutesSeconds(this.seconds)
        this.lastB = this.currentB
        this.currentB = index

        MyApplication.ApArray[this.lastB].status = statusID.not_connected
        MyApplication.ApArray[this.currentB].status = statusID.connecting_phase1

        val currentholder = recyclerView.findViewHolderForAdapterPosition(this.currentB)
        val lastholder = recyclerView.findViewHolderForAdapterPosition(this.lastB)
        lastholder?.itemView?.button2?.text = "Connect"
        lastholder?.itemView?.button2?.setBackgroundColor(Color.parseColor("#99ccff"))
        currentholder?.itemView?.button2?.text = MyApplication.timerString
        currentholder?.itemView?.button2?.setBackgroundColor(Color.parseColor("#fc9c9c"))
        val lastStat = "Status: " + statusID2String(MyApplication.ApArray[this.lastB].status)
        val currentStat = "Status: " + statusID2String(MyApplication.ApArray[this.currentB].status)
        lastholder?.itemView?.status_lable?.text = lastStat
        currentholder?.itemView?.status_lable?.text = currentStat

        handler.post(runnableCode)
    }

    // Clock at 1000ms
    private val runnableCode = object : Runnable {
        override fun run() {
            SMClock()
            handler.postDelayed(this, 1000)
        }
    }

    // CORE state machine
    // Ran at 1s interval after private fun partItemClicked(partItem: ApClass)
    private fun SMClock() {
        // Connection Phase1: create and apply wifi config object to wifi manager
        if (MyApplication.ApArray[this.currentB].status == statusID.connecting_phase1) {
            this.seconds -= 1
            this.updateClockbtn()
            if (this.seconds < 0) {
                this.timeoutFunc()
            } else if (this.seconds % this.checktime == 0 && this.seconds != this.timeout && this.seconds != 0) {
                val SSID = MyApplication.ApArray[this.currentB].ssid
                val passphrase = MyApplication.ApArray[this.currentB].password

                this.log("Trying to connect to " + SSID)

                val wifiManager: WifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
                val wifiConfig = WifiConfiguration()

                wifiConfig.SSID = "\"" + SSID + "\""

                if (MyApplication.ApArray[this.currentB].type == "OPEN") {
                    wifiConfig.allowedKeyManagement.set(WifiConfiguration.KeyMgmt.NONE)
                } else if (MyApplication.ApArray[this.currentB].type == "ENT") {
                    wifiConfig.status = WifiConfiguration.Status.ENABLED
                    val wifiConfigENT = WifiEnterpriseConfig()
                    wifiConfig.allowedKeyManagement.set(WifiConfiguration.KeyMgmt.WPA_EAP)
                    wifiConfig.allowedKeyManagement.set(WifiConfiguration.KeyMgmt.IEEE8021X)
                    wifiConfigENT.identity = MyApplication.ApArray[this.currentB].username
                    wifiConfigENT.password = MyApplication.ApArray[this.currentB].password
                    wifiConfigENT.eapMethod = WifiEnterpriseConfig.Eap.PEAP
                    wifiConfigENT.phase2Method = WifiEnterpriseConfig.Phase2.NONE
                    wifiConfig.enterpriseConfig = wifiConfigENT

                }else {
                    wifiConfig.allowedKeyManagement.set(WifiConfiguration.KeyMgmt.WPA_PSK)
                    wifiConfig.preSharedKey = "\"" + passphrase + "\""
                }

                try {
                    val netId = wifiManager.addNetwork(wifiConfig)
                    wifiManager.disconnect()
                    wifiManager.enableNetwork(netId, true)
                }
                catch (e: NumberFormatException) {
                    this.log("ERROR")
                }

                MyApplication.ApArray[this.currentB].status = statusID.connecting_phase2
            }
            // Connection Phase2: ping host name until connect
        } else if (MyApplication.ApArray[this.currentB].status == statusID.connecting_phase2) {
            this.seconds -= 1
            this.updateClockbtn()
            if (this.seconds < 0) { this.timeoutFunc() }
            this.checkInternetConnection()
            if (this.pingRecevied) {
                MyApplication.ApArray[this.currentB].status = statusID.connected
                this.seconds = 0
                this.failPingCount = 0
                this.updateClockbtn()
                val currentholder = recyclerView.findViewHolderForAdapterPosition(this.currentB)
                val currentStat = "Status: " + statusID2String(MyApplication.ApArray[this.currentB].status)
                currentholder?.itemView?.status_lable?.text = currentStat
            } else { this.failPingCount += 1 }
            // Connection phase connected: Device connected to AP ping forever
        } else if (MyApplication.ApArray[this.currentB].status == statusID.connected) {
            this.checkInternetConnection()
            if (!this.pingRecevied) { this.failPingCount += 1 }
            if (this.failPingCount >= this.failPingMax) { this.timeoutFunc() }
            this.seconds += 1
            this.updateClockbtn()
        }
    }//SMClock

    //https://stackoverflow.com/questions/52571339/how-do-i-programmatically-ping-a-website-in-android
    private fun checkInternetConnection() {
        val cm = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val ni = cm.activeNetworkInfo
        if (null == ni) {
            this.log("no internet connection for SSID: " + MyApplication.ApArray[this.currentB].ssid)
            this.pingRecevied = false
        } else {
            this.log("Internet Connection is detected...")
            this.pingRecevied = true
        }
    }

    // timeout handler for UI and data/state machine
    private fun timeoutFunc() {
//        val ap = MyApplication.ApArray
        this.removeAllSSID()
        this.seconds = this.timeout
        MyApplication.timerString = this.secondsToHoursMinutesSeconds(this.seconds)
        this.failPingCount = 0
        MyApplication.ApArray[this.currentB].status = statusID.not_connected

        val currentholder = recyclerView.findViewHolderForAdapterPosition(this.currentB)
        currentholder?.itemView?.button2?.text = "Connect"
        currentholder?.itemView?.button2?.setBackgroundColor(Color.parseColor("#99ccff"))
        currentholder?.itemView?.status_lable?.text = "Status: " + statusID2String(MyApplication.ApArray[this.currentB].status)

        this.lastB = this.currentB
        this.currentB += 1
        if (this.currentB >= MyApplication.ApArray.size) { this.currentB = 0 }
        MyApplication.ApArray[this.currentB].status = statusID.connecting_phase1

        val nextholder = recyclerView.findViewHolderForAdapterPosition(this.currentB)
        nextholder?.itemView?.button2?.text = MyApplication.timerString
        nextholder?.itemView?.button2?.setBackgroundColor(Color.parseColor("#fc9c9c"))
        nextholder?.itemView?.status_lable?.text = "Status: " + statusID2String(MyApplication.ApArray[this.currentB].status)

        recyclerView.adapter?.notifyItemChanged(this.lastB)
        recyclerView.adapter?.notifyItemChanged(this.currentB)

        this.log("Timed out at SSID: " + MyApplication.ApArray[this.lastB].ssid)
    }

    // remove all ssid
    private fun removeAllSSID() {
        val wifiManager: WifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val list = wifiManager.configuredNetworks
        for (i in list) {
            wifiManager.disableNetwork(i.networkId)
            wifiManager.removeNetwork(i.networkId)
        }
        wifiManager.disconnect()
    }

    private fun log(input: String) {
        Log.d("Log", "[Status] " + input)
    }

    private fun updateClockbtn() {
        MyApplication.timerString = this.secondsToHoursMinutesSeconds(this.seconds)
        val currentholder = recyclerView.findViewHolderForAdapterPosition(this.currentB)
        currentholder?.itemView?.button2?.text = MyApplication.timerString
    }

    private fun createTestAP_ALEOS() {
        MyApplication.ApArray.add(ApClass("Airport1", "","","OPEN", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport2", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport3", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport4", "","","OPEN", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport5", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport6", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport7", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport8", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport9", "newworld","peapuser","ENT", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport10", "","","OPEN", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport11", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport12", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport13", "newworld","peapuser","ENT", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport14", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport15", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport16", "newworld","peapuser","ENT", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport17", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport18", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("Airport19", "newworld","peapuser","ENT", statusID.not_connected))
    }

    private fun createTestAP_MGOS() {
        MyApplication.ApArray.add(ApClass("MG_AP1", "","","OPEN", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP2", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP3", "newworld","peapuser","ENT", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP4", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP5", "newworld","peapuser","ENT", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP6", "","","OPEN", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP7", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP8", "newworld","peapuser","ENT", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP9", "","","OPEN", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP10", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP11", "newworld","peapuser","ENT", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP12", "","","OPEN", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP13", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP14", "newworld","peapuser","ENT", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP15", "","","open", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP16", "1234567890","","WPA/WPA2", statusID.not_connected))
        MyApplication.ApArray.add(ApClass("MG_AP17", "newworld","peapuser","ENT", statusID.not_connected))
    }


    private fun secondsToHoursMinutesSeconds(seconds: Int): String {
        val h = seconds / 3600
        val m = (seconds % 3600) / 60
        val s = (seconds % 3600) % 60
        var hSting = h.toString()
        var mSting = m.toString()
        var sSting = s.toString()
        if (h < 10) { hSting = "0" + h.toString() }
        if (m < 10) { mSting = "0" + m.toString() }
        if (s < 10) { sSting = "0" + s.toString() }
        return (hSting + ":" + mSting + ":" + sSting)
    }

}

