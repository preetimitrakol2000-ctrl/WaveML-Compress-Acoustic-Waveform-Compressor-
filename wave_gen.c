#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define SAMPLE_COUNT 100
#define M_PI 3.14159265358979323846

// Simulates wave interference and quantizes data into discrete frequency bins (0-9)
void generate_wave_stream(int* output_stream, double phase_shift) {
    for (int i = 0; i < SAMPLE_COUNT; i++) {
        double t = (double)i / SAMPLE_COUNT;
        
        // Wave 1: Fundamental frequency
        double wave1 = sin(2.0 * M_PI * 5.0 * t); 
        // Wave 2: Interfering frequency with dynamic phase shift
        double wave2 = sin(2.0 * M_PI * 12.0 * t + phase_shift); 
        
        // Combine waves and normalize to a scale of 0.0 to 1.0
        double combined = (wave1 + wave2 + 2.0) / 4.0;
        
        // Quantize into discrete character categories for the Huffman encoder (0 to 9)
        output_stream[i] = (int)(combined * 9.99);
    }
}
