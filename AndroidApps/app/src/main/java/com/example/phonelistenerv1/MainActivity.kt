package com.example.phonelistenerv1

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.PowerManager
import android.util.Log
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import org.java_websocket.WebSocket
import org.java_websocket.handshake.ClientHandshake
import org.java_websocket.server.WebSocketServer
import org.json.JSONObject
import org.vosk.Recognizer
import org.vosk.android.StorageService
import java.net.InetSocketAddress
import java.nio.ByteBuffer

class MainActivity : AppCompatActivity() {

    private lateinit var tvResult: TextView
    private lateinit var btnStart: Button
    private var wakeLock: PowerManager.WakeLock? = null
    private var wsServer: SimpleWebSocketServer? = null

    private var recognizer: Recognizer? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvResult = findViewById(R.id.tvResult)
        btnStart = findViewById(R.id.btnStart)
        btnStart.text = "Initializing AI..."
        btnStart.isEnabled = false

        val powerManager = getSystemService(POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "PhoneListener::WsServerLock")
        wakeLock?.acquire(30 * 60 * 1000L)

        wsServer?.stop()
        wsServer = SimpleWebSocketServer(InetSocketAddress("0.0.0.0", 9090))
        wsServer?.isReuseAddr = true
        wsServer?.start()

            loadVoskModel()

    }

    private fun loadVoskModel() {
        StorageService.unpack(this, "voskmodel", "model_ro",
            { model ->
                recognizer = Recognizer(model, 16000.0f)
                runOnUiThread {
                    btnStart.text = "AI Ready! Waiting for ESP32..."
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
        wakeLock?.release()
        wsServer?.stop()
        recognizer?.close()
    }

    inner class SimpleWebSocketServer(address: InetSocketAddress) : WebSocketServer(address) {
        var running = false
        override fun onOpen(conn: WebSocket?, handshake: ClientHandshake?) {
            Log.d("WS", "ESP32 Connected!")
            runOnUiThread { btnStart.text = "ESP32 Connected! Speak into ESP32 Mic." }
        }
        override fun onClose(conn: WebSocket?, code: Int, reason: String?, remote: Boolean) {
            Log.d("WS", "ESP32 Disconnected!")
            runOnUiThread { btnStart.text = "ESP32 Disconnected." }
        }
        override fun onMessage(conn: WebSocket?, message: String?) {}


        override fun onMessage(conn: WebSocket?, message: ByteBuffer?) {
            val audioData = message?.array() ?: return

            recognizer?.let { rec ->
                val isSentenceFinished = rec.acceptWaveForm(audioData, audioData.size)
                val jsonResult = if (isSentenceFinished) rec.result else rec.partialResult

                val json = JSONObject(jsonResult)
                val key = if (isSentenceFinished) "text" else "partial"

                if (json.has(key)) {
                    val spokenText = json.getString(key)
                    if (spokenText.isNotEmpty()) {
                        runOnUiThread { tvResult.text = spokenText }
                        broadcast(spokenText) //sent to oled
                    }
                }
            }
        }

        override fun onError(conn: WebSocket?, ex: Exception?) {}
        override fun onStart() {
            running = true
        }
    }
}