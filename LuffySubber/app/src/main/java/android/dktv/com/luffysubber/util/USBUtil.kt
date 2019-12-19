package android.dktv.com.luffysubber.util

import android.content.Context
import android.hardware.usb.UsbConstants
import android.hardware.usb.UsbManager
import androidx.core.content.ContextCompat.getSystemService
import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader

fun getUsbMoutPoint(usb:UsbManager){
    //val pid = Runtime.getRuntime().exec("mount | grep ")
//val usb = this.getSystemService(UsbManager::class.java)
//        getUsbMoutPoint(usb)
    for( i in usb.deviceList){
        println("===============")
        println(i.key)
        println(i.value.manufacturerName)
        //println(i.value)
        var l = i.value.interfaceCount -1
        while(l>=0){
            if(i.value.getInterface(l).interfaceClass == UsbConstants.USB_CLASS_MASS_STORAGE){
                println(i.value.getInterface(l))
                println("----")
                println(i.value)

            }
            l--
        }
        println("===============")
    }
}

fun getMountedStorage():List<String> {

    val pid = Runtime.getRuntime().exec("mount")
    pid.waitFor()
    val tty = pid.inputStream.readBytes()

    var s = ""
    tty.forEach {
        s+=it.toChar()
    }

    val words = s.split(" ")
    val re = "^/storage/[^ \\t]*".toRegex()
    val re2 = "/storage/(self|emulated)".toRegex()

    var result = mutableListOf<String>()
    words.forEach {
        if(it.matches(re) and !it.matches(re2)){
            result.add(it)
        }
    }

    return result

}

fun verifyUSB(usb:String,dir:String,mkdir:Boolean = false):Boolean{

    val tg = File(usb,dir)
    if(tg.exists() && tg.isDirectory){
        return true
    }

    if(!tg.exists() && mkdir){
        tg.mkdirs()
        return true
    }

    return false

}