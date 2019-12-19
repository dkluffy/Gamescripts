package android.dktv.com.luffysubber.util

import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
import java.io.File
import java.io.IOException
import java.net.URL

fun a2cRunner(bin:String, usb:String) {

    checkRPC("aria2.shutdown")

    var rpc = "Not Running!"

    try{

        val rdir = usb+"/a2croot"
        File(rdir).mkdirs()

        val sessionfile = rdir+"/a2c.sessions"
        if(!File(sessionfile).exists()){
            File(sessionfile).createNewFile()
        }

        val dhtfile = rdir+"/dht.dat"
        if(!File(dhtfile).exists()) {
            File(dhtfile).createNewFile()
        }

        var configfile = rdir+"/aria2.conf"
        val f = File(configfile)
            f.writeText("""
async-dns-server=8.8.8.8
async-dns=true
save-session-interval=60
check-certificate=false
disable-ipv6=true
bt-tracker=http://tracker.internetwarriors.net:1337/announce,http://tracker2.itzmx.com:6961/announce,http://tracker1.itzmx.com:8080/announce,http://explodie.org:6969/announce,http://tracker.port443.xyz:6969/announce,http://private.minimafia.nl:443/announce,http://prestige.minimafia.nl:443/announce,http://open.acgnxtracker.com:80/announce,http://tracker3.itzmx.com:6961/announce,http://torrent.nwps.ws:80/announce,http://t.nyaatracker.com:80/announce,http://opentracker.xyz:80/announce,http://open.trackerlist.xyz:80/announce,http://tracker1.wasabii.com.tw:6969/announce,http://wegkxfcivgx.chickenkiller.com:80/announce,http://tracker.torrentyorg.pl:80/announce,http://tracker.open-tracker.org:1337/announce,http://tracker.gbitt.info:80/announce,http://tracker.city9x.com:2710/announce,http://torrentclub.tech:6969/announce,http://retracker.mgts.by:80/announce,http://open.acgtracker.com:1096/announce,http://node.611.to:9000/announce,http://bt.artvid.ru:6969/announce,http://0d.kebhana.mx:443/announce,http://tracker4.itzmx.com:2710/announce,http://tracker.tfile.me:80/announce.php,http://tracker.tfile.me:80/announce,http://tracker.tfile.co:80/announce,http://share.camoe.cn:8080/announce,http://peersteers.org:80/announce,http://omg.wtftrackr.pw:1337/announce,http://fxtt.ru:80/announce

# see --split option
max-concurrent-downloads=10
continue=true
max-overall-download-limit=0
max-overall-upload-limit=200K
max-upload-limit=100K
enable-dht=false

# RPC Options
enable-rpc=true
rpc-allow-origin-all=true
rpc-listen-all=true
rpc-save-upload-metadata=true
rpc-secure=false

# Advanced Options
daemon=true

dir=$rdir
save-session=$sessionfile
input-file=$sessionfile
dht-file-path=$dhtfile
#log=$rdir/1a.log
""")


        //nohup aria2c --enable-rpc --rpc-listen-all=true --rpc-allow-origin-all --rpc-secret=<yousecretcode> &

        val para = "  --conf-path=$configfile "

        val pid = Runtime.getRuntime().exec("$bin $para")

        pid.waitFor()

        rpc=checkRPC("aria2.getVersion")

        println(rpc)
        printError(pid)
        println("bbbb $pid ,$rdir,$bin")
        println(para)




    }catch (e:Exception){
        println("aaaa $e")
    }


}


fun printError(pid:Process){

    var errtty=pid.errorStream.readBytes()
    var tty=pid.inputStream.readBytes()
    var s=""
    println("===== Output of PID: $pid =====")
    tty.forEach {
        s+=it.toChar()
    }
    errtty.forEach {
        s+=it.toChar()
    }
    println("$s \n=========END=============")

}

fun checkRPC(m:String,id:Int=1):String{
    val url = "http://127.0.0.1:6800/jsonrpc?method=$m&id=$id"
    var txt = "---->> FAILED: method = $m"
    var maxtry = 3

    while(maxtry>0){
        try {
            val obj = URL(url)
            txt = obj.readText()

            if(m == "aria2.shutdown"){
                runBlocking {
                    println("----> wait aria2c to shutdown")
                    delay(10000)
                }
            }

            break
        }catch (e:Exception){

            println("-----> retrying rpc: $m")
            maxtry-=1
            runBlocking {
                delay(2000)
            }
        }

    }



    return txt
}