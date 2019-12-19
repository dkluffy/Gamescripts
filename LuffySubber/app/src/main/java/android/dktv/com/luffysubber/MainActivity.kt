/*
 * Copyright (C) 2017 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */

package android.dktv.com.luffysubber

import android.app.Activity
import android.dktv.com.luffysubber.util.*

import android.os.Bundle

import android.view.View
import android.widget.RadioButton
import android.widget.RadioGroup


import kotlinx.android.synthetic.main.activity_main.*
import org.jetbrains.anko.*
import java.io.File
import java.net.NetworkInterface

import java.util.zip.ZipInputStream



class MainActivity : Activity() {

    var appdir: String = "/"
    var webServer: KServer? = null

    var usbDir: String = "/"

    private var  webport = 9090

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        appdir = applicationInfo.dataDir + "/files/"

        //web server
        val webdir = appdir+"/AriaNg-DailyBuild-master/"
        webServer = KServer(port=webport,rootDir=webdir)

        bReload(this.contentView!!)
    }

    //usb
    // /storage/960E30880E306401/Android/media/android.dktv.com.luffysubber/a2croot
    fun bReload(view: View){
        listUsb(view)
        if(!File(appdir,"aria2c").exists()){
            extraFiles()
        }

        doAsync {
            webServer?.stop()
            webServer?.run()
        }

        val nis = NetworkInterface.getNetworkInterfaces().toList()

        var urltxt = ""
        val regIp4 = "([0-9]{1,3}\\.){3}[0-9]{1,3}".toRegex()
        nis.forEach {
            if( !it.isLoopback and !it.isVirtual){
                for(i in it.inetAddresses.toList()){
                    if(regIp4.find(i.toString())?.value != null){
                        var httpurl = "http://${regIp4.find(i.toString())?.value }:$webport/index.html"
                        qrview.setImageBitmap(Qrcode.createQRCode(httpurl))
                        urltxt+=(httpurl+"\n")
                    }

                }

            }

        }
        infoview.text = urltxt
        println(urltxt)


    }

    fun listUsb(view: View){

        val rg:RadioGroup = findViewById(R.id.storagedirs)
        val dirlist = mutableListOf<List<Any>>()


        rg.removeAllViews()

        applicationContext.externalMediaDirs.forEach {
            dirlist.add(listOf(it.absolutePath,(it.freeSpace/1000.0/1000.0).toInt(),(it.totalSpace/1000.0/1000.0).toInt()))
        }

        if(dirlist.size == 0){

            toast("No USB attached!")

        }else{
            //val regtxt = "/storage/emulated/.*".toRegex()
            var mxfree = mutableListOf(0,0)

            dirlist.forEach{
                val r = RadioButton(view.context)

                val k = it[1].toString().toInt()

                if( k > mxfree[0]) {
                    mxfree[0] = k
                    mxfree[1] +=1
                }

                r.text = "${it[0]} / Total: ${ it[1]} /${it[2]} MB"

                rg.addView(r)

                r.setOnCheckedChangeListener { _, isChecked ->
                    if(isChecked){
                        usbDir = it[0].toString()
                        toast("set USB dir to: $usbDir")

                        doAsync {
                            a2cRunner(appdir+"/aria2c",usbDir)
                        }


                    }


                }


            }
            rg.check(mxfree[1])



        }



    }


    //unzip button click
    fun extraFiles(){

        val dstdir = this.appdir

        println("bbbb-->> $dstdir")

        longToast("UnZipping...")

        doAsync {
            try {
                val rawfd = R.raw.ariaweb
                val zipin = ZipInputStream(resources.openRawResource(rawfd))
                zipin.use {
                    UnZipper(dstdir, zipin)
                }

                Runtime.getRuntime().exec("chmod 777 ${dstdir}/aria2c")

                runOnUiThread {
                    toast("files copied to $dstdir !!!")
                }

            }catch (e:Exception){
                runOnUiThread {
                    toast("Unzip files failed!!!")
                }

            }

        }

    }




}
