from optimum.onnxruntime import ORTModelForSeq2SeqLM
from optimum.onnxruntime import ORTQuantizer
from optimum.onnxruntime.configuration import AutoQuantizationConfig
import os

model_path = "./opus-mt-en-ro-onnx"
output_path = "./opus-mt-en-ro-quantized"
os.makedirs(output_path, exist_ok=True)

qconfig = AutoQuantizationConfig.arm64(is_static=False, per_channel=False)

for filename in ["encoder_model.onnx", "decoder_model.onnx", "decoder_with_past_model.onnx"]:
    print(f"Quantizing {filename}...")
    quantizer = ORTQuantizer.from_pretrained(model_path, file_name=filename)
    quantizer.quantize(
        save_dir=output_path,
        quantization_config=qconfig
    )
    print(f"Done.")

