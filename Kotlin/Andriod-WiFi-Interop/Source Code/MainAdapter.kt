package com.example.jerliu.wifi_test

import android.graphics.Color
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import kotlinx.android.synthetic.main.cell_layout.view.*
import com.example.jerliu.wifi_test.ApClass
import com.example.jerliu.wifi_test.statusID
import android.content.Intent.getIntent
import android.content.Intent

class MainAdapter (private val listener: (ApClass) -> Unit): RecyclerView.Adapter<RecyclerView.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CutsomViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        val cellForRow = layoutInflater.inflate(R.layout.cell_layout, parent, false)
        return CutsomViewHolder(cellForRow)
    }

    override fun onBindViewHolder(holder:  RecyclerView.ViewHolder, position: Int) {

        (holder as CutsomViewHolder).bind(MyApplication.ApArray[position], listener)
    }

    override fun getItemViewType(position: Int): Int {
        return position
    }

    override fun getItemCount() = MyApplication.ApArray.size


    class CutsomViewHolder(val view: View) : RecyclerView.ViewHolder(view){
        fun bind(part: ApClass, clickListener: (ApClass) -> Unit) {

            view.ssid_lable.text = "SSID: " + MyApplication.ApArray[position].ssid
            view.button2.setBackgroundColor(Color.parseColor("#99ccff"))
            view.button2.setOnClickListener { clickListener(part) }

            if (MyApplication.ApArray[position].status != statusID.not_connected) {
                view.button2?.text = MyApplication.timerString
                view.button2.setBackgroundColor(Color.parseColor("#fc9c9c"))
                view.status_lable?.text = "Status: " + statusID2String(MyApplication.ApArray[position].status)

            }
            else{
                view.button2?.text = "Connect"
                view.button2.setBackgroundColor(Color.parseColor("#99ccff"))
                view.status_lable?.text = "Status: " + statusID2String(MyApplication.ApArray[position].status)
            }

        }
    }


}






