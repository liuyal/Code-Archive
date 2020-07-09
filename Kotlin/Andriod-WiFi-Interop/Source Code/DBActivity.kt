package com.example.jerliu.wifi_test

import android.os.Bundle
import android.support.design.widget.BottomNavigationView
import android.support.v7.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_db.*
import android.widget.Button
import android.content.Intent
import android.util.Log

class DBActivity : AppCompatActivity() {

    private val mOnNavigationItemSelectedListener = BottomNavigationView.OnNavigationItemSelectedListener { item -> when (item.itemId) {
            R.id.navigation_home -> { finish(); return@OnNavigationItemSelectedListener true }
            R.id.navigation_dashboard -> { return@OnNavigationItemSelectedListener true }
        }
        false
    }

    override fun onDestroy() { super.onDestroy() }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_db)
        setTitle("Database")
        navigation2.getMenu().getItem(1).setChecked(true);
        navigation2.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener)



    }




}
