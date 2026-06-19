import ctypes
import os
import sys
from collections import Counter
from wave_gen import * from anomaly_detector import WaveAnomalyDetector

def compile_wave_backend():
    print("[*] Compiling backend wave processing & compression engines...")
    ext = "dll" if sys.platform.startswith("win") else "so"
    os.system(f"gcc -shared -o wave_gen.{ext} -fPIC wave_gen.c")
    os.system(f"gcc -shared -o huffman_tree.{ext} -fPIC huffman_tree.c")
    return f"./wave_gen.{ext}", f"./huffman_tree.{ext}"

def main():
    gen_path, tree_path = compile_wave_backend()
    gen_lib = ctypes.CDLL(gen_path)
    tree_lib = ctypes.CDLL(tree_path)

    # Set type mappings
    int_array_100 = ctypes.c_int * 100
    gen_lib.generate_wave_stream.argtypes = [int_array_100, ctypes.c_double]

    # 1. Generate an anomalous wave with an intentional heavy phase shift (3.14 rad)
    wave_data = int_array_100()
    phase_anomaly = 3.14
    gen_lib.generate_wave_stream(wave_data, ctypes.c_double(phase_anomaly))
    python_wave_list = list(wave_data)

    # 2. Process frequency counts for Huffman Encoding Tree
    counts = Counter(python_wave_list)
    unique_vals = list(counts.keys())
    frequencies = list(counts.values())
    size = len(unique_vals)

    c_int_arr_unique = (ctypes.c_int * size)(*unique_vals)
    c_int_arr_freq = (ctypes.c_int * size)(*frequencies)

    tree_lib.get_compressed_bit_depth.argtypes = [
        ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int
    ]
    
    # 3. Calculate Bitstream Savings
    raw_size_bits = 100 * 8  # Assuming 8-bit standard distribution
    compressed_size_bits = tree_lib.get_compressed_bit_depth(c_int_arr_unique, c_int_arr_freq, size)

    # 4. Machine Learning Anomaly Detection
    detector = WaveAnomalyDetector()
    detected_anomalies = detector.analyze_stream(python_wave_list)

    # Output Results
    print("\n================== WAVE-ML PIPELINE METRICS ==================")
    print(f"Raw Signal Size             : {raw_size_bits} bits")
    print(f"Huffman Compressed Size     : {compressed_size_bits} bits")
    print(f"Data Footprint Reduction    : {((raw_size_bits - compressed_size_bits) / raw_size_bits) * 100:.1f}%")
    print(f"ML Anomaly Flag Intercepts  : {detected_anomalies} anomalies verified in window")
    print("==============================================================\n")

if __name__ == "__main__":
    main()
