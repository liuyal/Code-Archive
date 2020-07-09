package com.example.manikrai.wifiapp

import android.content.BroadcastReceiver
import android.content.Context
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import kotlinx.android.synthetic.main.activity_main.*
import org.jetbrains.anko.toast
import android.net.wifi.WifiConfiguration
import android.net.wifi.WifiManager
import android.widget.Toast
import android.content.Intent
import android.net.NetworkInfo
import android.net.wifi.WifiInfo
import android.os.CountDownTimer
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.ValueEventListener
import kotlinx.coroutines.experimental.channels.NULL_VALUE


class MainActivity : AppCompatActivity() {

    object Config{

        var active_ssid = NULL_VALUE   //GETTING ACTIVE SSID FROM FIREBASE
        var name = NULL_VALUE           //GETTING name of active ssid from firebase   ........eg airport1
        var password= NULL_VALUE        //getting password of active ssid from firebase.......eg 12345678
        var ssid_name = NULL_VALUE      //WILL  enclose active ssid name in DOUBLE QUOTES.....eg "airport1"
        var pass = NULL_VALUE              //WILL  enclose active ssid password in DOUBLE QUOTES....eg "12345678"
    }

    val TAG:String="MainActivity";

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        start.setOnClickListener {
             retrieveactivessid()  //getting the active ssid number from the database for first time after that it will be automatic
            starting.text = "Test running"   //to dispaly on screen that test is started

            Log.d("testbed", "test started")
        }

        stop.setOnClickListener {
            //toast(isConnectedTo("\"airport5\"").toString())
        }
    }

    fun retrieveactivessid(){
        //this function is triggered automatically after test is started i.e whenever active ssid variable is changed in database it is called
        FirebaseDatabase.getInstance().reference.child("active_ssid").addValueEventListener(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {

                //if its succesfully able to retrieve data then enters here
                println("Active SSID is: " + dataSnapshot!!.value)
                //  var manik = dataSnapshot!!.value.toString()
                Config.active_ssid = dataSnapshot!!.value.toString()
                retrievessidinfo()   //to retrieve the info of active ssid i.e its name and password
                toast("connected to database ")

            }

            override fun onCancelled(databaseError: DatabaseError) {
                //if not able to retrieve data from db
                toast("Something went wrong when retrieving data!")
            }
        })


    }

    fun upadteStuffFromDatabase(){

        //it uis used to update data on db
        //rn this function is not used anywhere

        FirebaseDatabase.getInstance().reference.child("ssid1").child("name").setValue("manik").addOnCompleteListener {

            if (it.isSuccessful) {
                Log.d("testbed", "value uploaded successfully!")
            } else {
                Log.d("testbed", "Something went wrong when uploading value")
            }
        }

    }

    fun retrievessidinfo(){

        //to get active SSID info

        var ssid_reference = "ssid" + Config.active_ssid // Using this as a reference to database eg ssid1 (where 1 is active ssid)
        FirebaseDatabase.getInstance().reference.child(ssid_reference).child("name").addListenerForSingleValueEvent(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {
                println("Name of SSID is: " + dataSnapshot!!.value)
                //  var manik = dataSnapshot!!.value.toString()
                Config.name = dataSnapshot!!.value.toString()
            }

            override fun onCancelled(databaseError: DatabaseError) {
                println("Something went wrong when retrieving data!")
            }
        })

        FirebaseDatabase.getInstance().reference.child(ssid_reference).child("password").addListenerForSingleValueEvent(object : ValueEventListener {

            override fun onDataChange(dataSnapshot: DataSnapshot) {
                println("Password of SSID is: " + dataSnapshot!!.value)
                //  var manik = dataSnapshot!!.value.toString()
                Config.password = dataSnapshot!!.value.toString()
                toast("Changing wifi to " + Config.name)

                Config.ssid_name = "\""+Config.name+"\""    //enclosing name in double quotes
                Config.pass = "\""+Config.password+"\""     //enclosing password in double quotes

                ssid_info.text = "Current SSID is " + Config.name + " with password "+ Config.password //to display on screen

                connectToWPAWiFi(Config.ssid_name.toString(), Config.pass.toString())  //connecting to that particular SSID
            }

            override fun onCancelled(databaseError: DatabaseError) {
                println("Something went wrong when retrieving data!")
            }
        })
    }

    fun connectToWPAWiFi(ssid:String,pass:String){

       // if(isConnectedTo(ssid)){ //see last ssid name to which tried to make connection
         //   toast("Connected to "+ssid)
           // Results.text = "Connection Successful"
            //return
        //}

        val wm:WifiManager= applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        var wifiConfig=getWiFiConfig(ssid)  //see if config already exist or not
        if(wifiConfig==null){//if the given ssid is not present in the WiFiConfig, create a config for it
            createWPAProfile(ssid,pass)
            wifiConfig=getWiFiConfig(ssid)
        }
        wm.disconnect()    //if connected to any wifi network disconnect from it
        wm.enableNetwork(wifiConfig!!.networkId,true)
        wm.reconnect()  //try to connect to active SSID

        Log.d(TAG,"intiated connection to SSID"+ssid);
    }

    fun isConnectedTo(ssid: String):Boolean{
        val wm:WifiManager= applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager

        if(wm.connectionInfo.ssid == ssid){


            return true

        }
        return false
    }

    fun getWiFiConfig(ssid: String): WifiConfiguration? {

        //if wifi config already exist return true else false
        val wm:WifiManager= applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val wifiList=wm.configuredNetworks
        for (item in wifiList){
            if(item.SSID != null && item.SSID.equals(ssid)){
                return item
            }
        }
        return null
    }

    fun createWPAProfile(ssid: String,pass: String){

        //if wifi config not exsit then make that
        Log.d(TAG,"Saving SSID :"+ssid)
        val conf = WifiConfiguration()
        conf.SSID = ssid
        conf.preSharedKey = pass
        val wm:WifiManager= applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        wm.addNetwork(conf)
        Log.d(TAG,"saved SSID to WiFiManger")
    }

    class WiFiChngBrdRcr : BroadcastReceiver(){ 
    // called automatically whenever we connect to ANY SSID.....this is the reason why we need to
    //turn off AUTO CONNECT while configuring SSID profiles
        
        private val TAG = "WiFiChngBrdRcr"

        override fun onReceive(context: Context, intent: Intent) {
            val networkInfo=intent.getParcelableExtra<NetworkInfo>(WifiManager.EXTRA_NETWORK_INFO)
            if(networkInfo.state == NetworkInfo.State.CONNECTED){
                val bssid=intent.getStringExtra(WifiManager.EXTRA_BSSID)
                Log.d(TAG, "Connected to BSSID:"+bssid)
                val ssid=intent.getParcelableExtra<WifiInfo>(WifiManager.EXTRA_WIFI_INFO).ssid
                val log="Connected to SSID: "+ssid
                Log.d(TAG,"Connected to  SSID:"+ssid)
                Toast.makeText(context, log, Toast.LENGTH_SHORT).show()
            }
        }
    }
}
