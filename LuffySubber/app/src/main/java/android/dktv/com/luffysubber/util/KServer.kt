package android.dktv.com.luffysubber.util

import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

import java.io.*
import java.net.ServerSocket
import java.net.Socket
import kotlin.Exception

enum class HttpMethods {
    GET, POST, PUT, DELETE, OPTIONS, HEAD, TRACE, CONNECT, PATCH
}


const val  DEFAULT_HTTP_VERSION = "HTTP/1.1"

class KServer(val port: Int = 9090,val rootDir:String = ".") {

    private var sock = ServerSocket(port)
    var isActive = true

    fun run() = runBlocking {
        try {
            if(sock.isClosed){
                sock = ServerSocket(port)
            }
            println("bbbb ->> running")
            while (!sock.isClosed) {
                val client = sock.accept()
                GlobalScope.launch {
                    client.use {
                        handleClient(client)
                    }
                }
            }

        } catch (e: IOException) {
            println(e.message)
            isActive = false

        }
    }

    fun stop(){
        println("bbbb ->> stopping")
        isActive = false
        sock.close()
    }

    private suspend fun handleClient(client: Socket) {
        val input = BufferedReader(InputStreamReader(client.inputStream))
        val out = client.outputStream

        val request = readRequest(input)
        var response = HttpResponse(status = Status.InternalServerError,content = "Unknown".toByteArray())

        when(request.headEntry.method ){
            HttpMethods.GET ->{
                response=doGet(request)
            }

        }
        try{
            send(out,response)
        }catch (e:Exception){
            println(e)
        }


    }
    private fun doGet(req:HttpRequest):HttpResponse{

        var version = req.headEntry.httpVersion
        var status = Status.OK
        var headers = mutableMapOf<String,String>()
        var contentType = "text/html; charset=\"UTF-8\""
        var content = ByteArray(0)
        var contentLength = 0

        val fullUrls = req.headEntry.url.toLowerCase().split("?")
        val url = fullUrls[0]


        val resFilePat = "\\.[0-9a-z]*$".toRegex()

        var path = File(this.rootDir).absolutePath
        val ext = resFilePat.find(url)?.value

        when(ext){
            null -> {
                content=doLet(url)

            }
            else -> {

                try {

                    contentType = ContenTypes.valueOf(ext.replace(".","").toUpperCase()).value

                }catch (e:Exception){
                    contentType = ContenTypes.UNKNOWN.value
                }
                val staticFile = File(path,url)
                if(staticFile.exists()){
                    content = staticFile.inputStream().readBytes()
                }

            }
        }
        content.let {
            contentLength = it.size
        }


        headers.put("Content-length",contentLength.toString())
        headers.put("Content-type",contentType)

        return HttpResponse(version,status,headers,content)
    }

    private fun doLet(url:String):ByteArray{

        return "Not Found : $url  ".toByteArray()
    }


    private fun send(out:OutputStream,response:HttpResponse){
        out.write("${response.version} ${response.status.code} ${response.status.value}".toByteArray())
        out.write("\r\n".toByteArray())

        response.headers.forEach{
            out.write("${it.key}: ${it.value}\r\n".toByteArray())
        }
        out.write("\r\n".toByteArray())

        out.write(response.content)
        out.flush()

    }



    private fun readRequest(reader: BufferedReader):HttpRequest{
        val headEntry  = reader.readLine().split(' ').let{  HeadEntry(HttpMethods.valueOf(it[0]),it[1],it[2])}
        val headers = LinkedHashMap<String,String>().apply {
            reader.lineSequence().takeWhile(String::isNotBlank).forEach {
                    line -> line.split(":").let { put(it[0], it[1].trim()) }
            }
        }
        return HttpRequest(headEntry,headers,reader)
    }


}


data class HeadEntry(val method: HttpMethods,val url: String,val httpVersion: String)

data class HttpRequest(
    val headEntry:HeadEntry,
    val headers: Map<String, String>,
    val stream: BufferedReader
) {
    val content: String by lazy {
        //通过委托，返回stream里 1~"Content-Length" 里的字符
        (1..headers.getOrElse("Content-Length",{"0"}).toInt()).fold(""){ chars, _ -> chars + stream.read().toChar() }
    }
}

data class HttpResponse(val version:String = DEFAULT_HTTP_VERSION,
                        val status: Status = Status.OK,
                        var headers:Map<String,String> = emptyMap(),
                        var content: ByteArray?=null)


enum class ContenTypes(val value: String){
    JS("application/x-javascript"),
    HTML("text/html; charset=\"UTF-8\""),
    CSS("text/css"),
    TXT("text/plain"),
    SVG("text/xml"),

    UNKNOWN("application/octet-stream")
}

enum class Status(val code: Int, val value: String) {
    // 100
    Continue(100, "Continue"),
    SwitchingProtocols(101, "Switching Protocols"), Processing(102, "Processing"),
    // 200
    OK(200, "OK"),
    Created(201, "Created"), Accepted(202, "Accepted"), NonAuthoritativeInformation(
        203,
        "Non-Authoritative Information"
    ),
    NoContent(204, "No Content"), ResetContent(205, "Reset Content"), PartialContent(206, "Partial Content"),
    MultiStatus(207, "Multi-Status"), AlreadyReported(208, "Already Reported"), IMUsed(226, "IM Used"),
    // 300
    MultipleChoices(300, "Multiple Choices"),
    MovedPermanently(301, "Moved Permanently"), Found(302, "Found"),
    SeeOther(303, "See Other"), NotModified(304, "Not Modified"), UseProxy(305, "Use Proxy"), SwitchProxy(
        306,
        "Switch Proxy"
    ),
    TemporaryRedirect(307, "Temporary Redirect"), PermanentRedirect(308, "Permanent Redirect"),
    // 400
    BadRequest(400, "Bad Request"),
    Unauthorized(401, "Unauthorized"), PaymentRequired(402, "Payment Required"),
    Forbidden(403, "Forbidden"), NotFound(404, "Not Found"), MethodNotAllowed(405, "Method Not Allowed"),
    NotAcceptable(406, "Not Acceptable"), ProxyAuthenticationRequired(407, "Proxy Authentication Required"),
    RequestTimeout(408, "Request Timeout"), Conflict(409, "Conflict"), Gone(410, "Gone"), LengthRequired(
        411,
        "Length Required"
    ),
    PreconditionFailed(412, "Precondition Failed"), PayloadTooLarge(413, "Payload Too Large"), URITooLong(
        414,
        "URI Too Long"
    ),
    UnsupportedMediaType(415, "Unsupported Media Type"), RangeNotSatisfiable(416, "Range Not Satisfiable"),
    ExpectationFailed(417, "Expectation Failed"), ImATeapot(418, "I'm a teapot"), MisdirectedRequest(
        421,
        "Misdirected Request"
    ),
    UnprocessableEntity(422, "Unprocessable Entity"), Locked(423, "Locked"), FailedDependency(424, "Failed Dependency"),
    UpgradeRequired(426, "Upgrade Required"), PreconditionRequired(428, "Precondition Required"),
    TooManyRequests(429, "Too Many Requests"), RequestHeaderFieldsTooLarge(431, "Request Header Fields Too Large"),
    UnavailableForLegalReasons(451, "Unavailable For Legal Reasons"),
    // 500
    InternalServerError(500, "Internal Server Error"),
    NotImplemented(501, "Not Implemented"), BadGateway(502, "Bad Gateway"),
    ServiceUnavailable(503, "Service Unavailable"), GatewayTimeout(504, "Gateway Timeout"),
    HTTPVersionNotSupported(505, "HTTP Version Not Supported"), VariantAlsoNegotiates(506, "Variant Also Negotiates"),
    InsufficientStorage(507, "Insufficient Storage"), LoopDetected(508, "Loop Detected"), NotExtended(
        510,
        "Not Extended"
    ),
    NetworkAuthenticationRequired(511, "Network Authentication Required")
}