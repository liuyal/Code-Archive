package com.example.jerliu.wifi_test

import android.app.Application

class MyApplication : Application() {

    companion object {
        var ApArray: MutableList<ApClass> = mutableListOf<ApClass>()
        var timerString  = "00:00:00"

    }

}