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
import org.vosk.android.RecognitionListener
import org.vosk.android.SpeechService
import org.vosk.android.StorageService
import java.net.InetSocketAddress

class MainActivity : AppCompatActivity(), RecognitionListener {

    private var speechService: SpeechService? = null
    private lateinit var tvResult: TextView
    private lateinit var btnStart: Button
    private var wakeLock: PowerManager.WakeLock? = null
    // THE NEW WEBSOCKET SERVER
    private var wsServer: SimpleWebSocketServer? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvResult = findViewById(R.id.tvResult)
        btnStart = findViewById(R.id.btnStart)
        val powerManager = getSystemService(POWER_SERVICE) as PowerManager
        wakeLock = powerManager.newWakeLock(
            PowerManager.PARTIAL_WAKE_LOCK,
            "PhoneListener::WsServerLock"
        )
        wakeLock?.acquire(30 * 60 * 1000L)
        // Start the server on port 8080
        wsServer?.stop()
        wsServer = SimpleWebSocketServer(InetSocketAddress("0.0.0.0", 9090))
        wsServer?.isReuseAddr = true
        wsServer?.start()

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), 1)
        } else {
            loadVoskModel()
        }
    }

    private fun loadVoskModel() {
        StorageService.unpack(this, "voskmodel", "model_ro", // Note: using your previous model name!
            { model ->
                val recognizer = Recognizer(model, 16000.0f)
                speechService = SpeechService(recognizer, 16000.0f)
                btnStart.text = "Start Listening"
                btnStart.isEnabled = true
                btnStart.setOnClickListener {
                    speechService?.startListening(this)
                    btnStart.text = "Listening..."
                    btnStart.isEnabled = false
                }
            },
            { exception -> tvResult.text = "Error: ${exception.message}" }
        )
    }

    // --- VOSK CALLBACKS (Modified to send to ESP32!) ---
    override fun onPartialResult(hypothesis: String?) {
        if (hypothesis != null) {
            val partialText = JSONObject(hypothesis).getString("partial")
            if (partialText.isNotEmpty()) {
                tvResult.text = partialText
                wsServer?.broadcast(partialText) // SEND TO ESP32!
            }
        }
    }

    override fun onResult(hypothesis: String?) {
        if (hypothesis != null) {
            val finalText = JSONObject(hypothesis).getString("text")
            if (finalText.isNotEmpty()) {
                tvResult.text = finalText
                wsServer?.broadcast(finalText) // SEND TO ESP32!
            }
        }
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
    override fun onFinalResult(hypothesis: String?) {}
    override fun onError(exception: Exception?) {}
    override fun onTimeout() {}
    override fun onDestroy() {
        super.onDestroy()
        wakeLock?.release()
        wsServer?.stop()
        speechService?.shutdown()
    }

    inner class SimpleWebSocketServer(address: InetSocketAddress) : WebSocketServer(address) {
        var running = false
        override fun onOpen(conn: WebSocket?, handshake: ClientHandshake?) {
            Log.d("WS", "ESP32 Connected!")
        }
        override fun onClose(conn: WebSocket?, code: Int, reason: String?, remote: Boolean) {
            Log.d("WS", "ESP32 Disconnected!")
        }
        override fun onMessage(conn: WebSocket?, message: String?) {}
        override fun onError(conn: WebSocket?, ex: Exception?) {}
        override fun onStart() {
            running = true
            Log.d("WS", "Server Started!")
        }
    }
}