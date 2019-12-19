package android.dktv.com.luffysubber.util


import java.io.FileOutputStream
import java.io.InputStream

fun copyRaw(src:InputStream,dst:String){
    val dstFile = FileOutputStream(dst)
    dstFile.write(src.readBytes())
    dstFile.flush()
    dstFile.close()
}

