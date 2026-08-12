package com.example.phonelistenerv1

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import org.json.JSONObject
import org.vosk.Recognizer
import org.vosk.android.RecognitionListener
import org.vosk.android.SpeechService
import org.vosk.android.StorageService

class MainActivity : AppCompatActivity(), RecognitionListener {

    private var speechService: SpeechService? = null
    private lateinit var tvResult: TextView
    private lateinit var btnStart: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvResult = findViewById(R.id.tvResult)
        btnStart = findViewById(R.id.btnStart)

        // 1. Ask for Microphone Permission
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), 1)
        } else {
            loadVoskModel()
        }
    }

    // 2. If permission is granted, load the model
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            loadVoskModel()
        } else {
            tvResult.text = "Microphone permission is required!"
        }
    }

    // 3. Unpack the model from the assets folder
    private fun loadVoskModel() {
        StorageService.unpack(this, "voskmodel", "model2",
            { model ->
                val recognizer = Recognizer(model, 16000.0f)
                speechService = SpeechService(recognizer, 16000.0f)

                // Model is loaded! Enable the button.
                btnStart.text = "Start Listening"
                btnStart.isEnabled = true

                btnStart.setOnClickListener {
                    speechService?.startListening(this)
                    btnStart.text = "Listening..."
                    btnStart.isEnabled = false // Disable button while listening
                }
            },
            { exception -> tvResult.text = "Error loading model: ${exception.message}" }
        )
    }

    // --- Vosk Callback Functions ---

    override fun onPartialResult(hypothesis: String?) {
        if (hypothesis != null) {
            val json = JSONObject(hypothesis)
            val partialText = json.getString("partial")
            if (partialText.isNotEmpty()) {
                tvResult.text = partialText
            }
        }
    }

    override fun onResult(hypothesis: String?) {
        if (hypothesis != null) {
            val json = JSONObject(hypothesis)
            val finalResultText = json.getString("text")
            if (finalResultText.isNotEmpty()) {
                tvResult.text = finalResultText
            }
        }
    }

    override fun onFinalResult(hypothesis: String?) {}
    override fun onError(exception: Exception?) {}
    override fun onTimeout() {}
}