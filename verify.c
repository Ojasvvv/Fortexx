#include <stdio.h>
#include <stdlib.h>
#include <stdint.h> // REQUIRED
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/err.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

// MUST include the function here too!
uint64_t compute_ahash(unsigned char *pixels, int w, int h, int channels){
    uint64_t hash = 0; double total = 0; unsigned char small[64];
    for (int y = 0; y < 8; y++) {
        for (int x = 0; x < 8; x++) {
            int idx = ((y * h / 8) * w + (x * w / 8)) * channels;
            small[y * 8 + x] = (pixels[idx] + pixels[idx+1] + pixels[idx+2]) / 3;
            total += small[y * 8 + x];
        }
    }
    double avg = total/64.0;
    for (int i = 0; i < 64; i++) if(small[i] >= avg) hash |= (1ULL << i);
    return hash;
}

int main() {
    int width, height, channels;
    unsigned char *pixels = stbi_load("protected.jpg", &width, &height, &channels, 0);
    if (!pixels) return 1;

    // 1. RSA Verification Logic (Keep your code here)
    // ... (your existing RSA check) ...

    // 2. Perceptual Verification Logic
    uint64_t saved_hash;
    FILE *h_file = fopen("ahash.bin", "rb");
    if (h_file) {
        fread(&saved_hash, sizeof(uint64_t), 1, h_file);
        fclose(h_file);

        uint64_t current_hash = compute_ahash(pixels, width, height, channels);
        int diff = 0;
        uint64_t x = saved_hash ^ current_hash;
        while (x > 0) { if (x & 1) diff++; x >>= 1; }

        printf("Perceptual Difference: %d bits\n", diff);
        if (diff == 0) printf("CONTENT: IDENTICAL\n");
        else if (diff < 5) printf("CONTENT: AUTHENTIC (Minor noise)\n");
        else printf("CONTENT: TAMPERED/AI MODIFIED\n");
    }

    // 3. Cleanup happens at the VERY END
    stbi_image_free(pixels); 
    return 0;
}