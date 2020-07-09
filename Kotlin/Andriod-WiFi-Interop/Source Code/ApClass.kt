package com.example.jerliu.wifi_test

import android.app.Application

enum class statusID {
    not_connected, connecting_phase1, connecting_phase2, connected
}

class ApClass(ssid:String, password:String, username:String, type:String, status:statusID) {

    var ssid = ssid
    var password = password
    var type = type
    var username = username
    var status = status

    init{}

}