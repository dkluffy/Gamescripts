package android.dktv.com.luffysubber.util

//import com.hierynomus.smbj.SMBClient
//import com.hierynomus.smbj.auth.AuthenticationContext
import jcifs.smb.SmbFile
import org.junit.Test

import org.junit.Assert.*

class SmbUtilKtTest {




    @Test
    fun connectShare() {
//        val client = SMBClient()
//
//        try{
//            val conn =  client.connect("172.168.1.251")
//            val ac = AuthenticationContext("admin", "ciscoAdmin".toCharArray(), "DOMAIN")
//            val session = conn.authenticate(ac)
//            val share = session.connectShare("public")
//
//            println("bbbb-->> $share.smbPath")
//
//        }catch (e:Exception){
//            println(e)
//        }
        val client = SmbFile("smb://guest:guest@172.168.1.251/public/")
        println("${client.list()[0]}")

    }
}