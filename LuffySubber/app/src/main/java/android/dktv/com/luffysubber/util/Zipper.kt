package android.dktv.com.luffysubber.util

import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.util.zip.ZipInputStream

fun UnZipper(dstpath: String, zipstream: ZipInputStream) {

    var e = zipstream.nextEntry
    while (e != null) {
        //println("Prcessing: ${e.name}")
        if (e.isDirectory) {
            //create directory
            val d = File(dstpath + e.name)
            d.mkdirs()
            e = zipstream.nextEntry
            continue
        }

        //unzip: copy bytes to fileoutputstream
        val output = FileOutputStream(dstpath + e.name)

        /* buff 的方式节省内存*/
//        val buff = ByteArray(2048)
//        while (zipstream.available()!=0) {
//            val len = zipstream.read(buff)
//            if (len <= 0) {
//                output.close()
//                break
//            }
//            output.write(buff,0,len)
//        }

        //需要大内存
        output.write(zipstream.readBytes())
        output.close()

        e = zipstream.nextEntry

    }


    zipstream.close()

}