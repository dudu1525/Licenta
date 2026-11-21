package com.example.phonelistenerv1


import android.os.Bundle
import android.os.PowerManager
import android.util.Log
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import org.java_websocket.WebSocket
import org.java_websocket.handshake.ClientHandshake
import org.java_websocket.server.WebSocketServer
import org.json.JSONObject
import org.vosk.Recognizer
import org.vosk.android.StorageService
import java.net.InetSocketAddress
import java.nio.ByteBuffer
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class MainActivity : AppCompatActivity() {

    private lateinit var tvResult: TextView
    private lateinit var btnStart: Button
    private var wakeLock: PowerManager.WakeLock? = null
    private var wsServer: SimpleWebSocketServer? = null

    private var recognizer: Recognizer? = null

    //the translator runs on its single thread
    @Volatile private var translator: com.chaquo.python.PyObject? = null
    private val translateExecutor = java.util.concurrent.Executors.newSingleThreadExecutor()
    private val translating = java.util.concurrent.atomic.AtomicBoolean(false)
    private var lastKey = ""
    ////////////////////////////////////////////////translator functions

    private fun loadTranslator() {
        Thread {
            if (!Python.isStarted()) Python.start(AndroidPlatform(this))
            translator = Python.getInstance().getModule("translator")
            runOnUiThread { btnStart.text = "Translator has loaded" }
        }.start()
    }
    private fun translate(original: String, isFinal: Boolean) {

        if (!isFinal && translating.get()) return

        translateExecutor.execute {
            translating.set(true)
            try {
                val translated = translator
                    ?.callAttr("translateSentence", original)
                    ?.toString()
                    ?: return@execute
                runOnUiThread { tvResult.text = "$original\n→ $translated" }
                wsServer?.broadcast(translated) //send translated to oled
            } finally {
                translating.set(false)
            }
        }
    }




    /////////////////////////////////////////
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvResult = findViewById(R.id.tvResult)
        btnStart = findViewById(R.id.btnStart)
        btnStart.text = "Initializing AI voice to text model"
        btnStart.isEnabled = false
        //partial wake lock so the phone doesent go to sleep whilest the translation and getting incoming audio happens
        //also runs even if screen is off
        val powerManager = getSystemService(POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "PhoneListener::WsServerLock")
        wakeLock?.acquire(30 * 60 * 1000L)

        wsServer?.stop()
        wsServer = SimpleWebSocketServer(InetSocketAddress("0.0.0.0", 9090))
        wsServer?.isReuseAddr = true
        wsServer?.start()

            loadVoskModel()
            loadTranslator()

    }

    private fun loadVoskModel() {
        StorageService.unpack(this, "voskmodel", "model_ro",
            { model ->
                recognizer = Recognizer(model, 16000.0f)
                runOnUiThread {
                    btnStart.text = "AI Loaded. Waiting for ESP Connection"
                }
            },
            { exception -> tvResult.text = "Error: ${exception.message}" }
        )
    }




    override fun onResume() {
        super.onResume()
        if (wsServer?.running == false) {
            wsServer?.stop()
            wsServer = SimpleWebSocketServer(InetSocketAddress("0.0.0.0", 9090))
            wsServer?.isReuseAddr = true
            wsServer?.start()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
       // wakeLock?.release()
        wsServer?.stop()
        recognizer?.close()
        translateExecutor.shutdownNow()
    }

    inner class SimpleWebSocketServer(address: InetSocketAddress) : WebSocketServer(address) {
        var running = false
        override fun onOpen(conn: WebSocket?, handshake: ClientHandshake?) {
            Log.d("WS", "ESP32 Connected!")
            runOnUiThread { btnStart.text = "You can hear others speak" }
        }
        override fun onClose(conn: WebSocket?, code: Int, reason: String?, remote: Boolean) {
            Log.d("WS", "ESP32 Disconnected!")
            runOnUiThread { btnStart.text = "ESP32 Disconnected." }
        }
        override fun onMessage(conn: WebSocket?, message: String?) {}


        override fun onMessage(conn: WebSocket?, message: ByteBuffer?) {
            message ?: return;
            //get remaining (unread data) from the esp
            val audioData = ByteArray(message.remaining()) //get the remaining(how many more are stored) in the bytebuffer (bytes available to be read)
            message.get(audioData)

            val rec = recognizer ?: return;

            val isFinal = rec.acceptWaveForm(audioData, audioData.size)//send data to the vosk model, also returns if its final or partial result
            val json = JSONObject(if (isFinal) rec.result else rec.partialResult)
            val text = json.optString(if (isFinal) "text" else "partial").trim()

            if (text.isEmpty()) return;

            //if nothing changed, do not translate or send
            val key = (if (isFinal) "F:" else "P:") + text
            if (key == lastKey) return;
            lastKey = key


            runOnUiThread { tvResult.text = text }

            translate(text, isFinal)
        }

        override fun onError(conn: WebSocket?, ex: Exception?) {}
        override fun onStart() {
            running = true
        }
    }
}