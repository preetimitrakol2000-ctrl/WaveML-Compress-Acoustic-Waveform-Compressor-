#include <stdio.h>
#include <stdlib.h>

// Defines a Node in the Huffman Binary Tree
typedef struct Node {
    int value;
    int frequency;
    struct Node *left, *right;
} Node;

// Basic selection sort helper to organize our node queue by frequency
void sort_nodes(Node** nodes, int size) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = i + 1; j < size; j++) {
            if (nodes[i]->frequency > nodes[j]->frequency) {
                Node* temp = nodes[i];
                nodes[i] = nodes[j];
                nodes[j] = temp;
            }
        }
    }
}

// Builds the Huffman Tree from character stream frequencies
Node* build_huffman_tree(int* values, int* frequencies, int unique_count) {
    int size = unique_count;
    Node** pool = (Node**)malloc(size * sizeof(Node*));
    
    for (int i = 0; i < size; i++) {
        pool[i] = (Node*)malloc(sizeof(Node));
        pool[i]->value = values[i];
        pool[i]->frequency = frequencies[i];
        pool[i]->left = pool[i]->right = NULL;
    }
    
    while (size > 1) {
        sort_nodes(pool, size);
        
        // Extract the two lowest frequency nodes
        Node* left_child = pool[0];
        Node* right_child = pool[1];
        
        // Create an internal combined parent node
        Node* parent = (Node*)malloc(sizeof(Node));
        parent->value = -1; // Internal node flag
        parent->frequency = left_child->frequency + right_child->frequency;
        parent->left = left_child;
        parent->right = right_child;
        
        // Restructure the array pool
        pool[0] = parent;
        for (int i = 1; i < size - 1; i++) {
            pool[i] = pool[i + 1];
        }
        size--;
    }
    
    Node* root = pool[0];
    free(pool);
    return root;
}

// Clean up allocated tree memory recursively
void free_tree(Node* root) {
    if (!root) return;
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

// Python bridge interface to calculate compressed data tree size
int get_compressed_bit_depth(int* values, int* frequencies, int unique_count) {
    Node* root = build_huffman_tree(values, frequencies, unique_count);
    int total_weight = root->frequency;
    free_tree(root);
    
    // Returns a simulated data weight compression ratio scalar
    return total_weight * 3; 
}
