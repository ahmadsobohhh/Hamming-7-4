# Developed by Ahmad Soboh
# 10/28/2024

import os
import random

def clear_cli():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_random_binary():
    return format(random.randint(0, 15), '04b') # Generates a random number between 0-15 and converts it to a binary format (4 digit binary code is from 0-15)

def calculate_redundant_bits(data_bits):
    d1, d2, d3, d4 = [int(bit) for bit in data_bits]
    r1 = d1 ^ d2 ^ d4
    r2 = d1 ^ d3 ^ d4
    r3 = d2 ^ d3 ^ d4
    return f"{r1}{r2}{r3}"

def calculate_codeword(data_bits, redundant_bits):
    d1, d2, d3, d4 = [int(bit) for bit in data_bits]
    r1, r2, r3 = [int(bit) for bit in redundant_bits]
    return f"{r1}{r2}{d1}{r3}{d2}{d3}{d4}"

def simulate_corruption(codeword):
    codeword_list = list(codeword)
    # Randomly flip one bit in the codeword
    error_position = random.randint(0, 6)  # There are 7 bits in the codeword
    if codeword_list[error_position] == '0':
        codeword_list[error_position] = '1'
    else: 
        codeword_list[error_position] = '0'
    return ''.join(codeword_list), error_position + 1  # Return corrupted codeword and position of the error

def correct_codeword(received_codeword):
    r1, r2, d1, r3, d2, d3, d4 = (int(bit) for bit in received_codeword)

    # Calculate the syndrome, if any of the syndrome bits are 1 it indicates an inconsistency in the relevant bits
    s1 = r1 ^ d1 ^ d2 ^ d4  # Checks for r1
    s2 = r2 ^ d1 ^ d3 ^ d4  # Checks for r2
    s3 = r3 ^ d2 ^ d3 ^ d4  # Checks for r3

    # Syndrome calculation
    syndrome = (s3, s2, s1) # Create the tuple with the syndome starting at s3 as it is the biggest bit
    error_position = int(''.join(str(x) for x in syndrome), 2) # This gives us our error position, converting the binary string to decimal
    
    if error_position != 0:
        # Correct the error by flipping the bit at the error position
        received_codeword = list(received_codeword)
        received_codeword[error_position - 1] = '1' if received_codeword[error_position - 1] == '0' else '0'
        received_codeword = ''.join(received_codeword)
        return received_codeword, error_position
    return received_codeword, None  # No error detected

def main():
    clear_cli()
    print("=========================================================================================================================")
    print("                             Hello Yalmez! Welcome to my Hamming (7, 4) FEC Algorithm Demonstrator")
    print("=========================================================================================================================")
    print("Forward Error Correction (FEC) works by adding redundant bits to data sent from the sender to the receiver.")
    print("These redundant bits are calculated from the actual data and can be used to repair any corruption that occurs during transmission.")
    print("FEC includes various algorithms, each designed to address specific error patterns.")
    print("In this demonstration, I will use the Hamming (7, 4) algorithm.")
    print("=========================================================================================================================")
    input("Click enter to continue...")
    clear_cli()
    
    print("=========================================================================================================================")
    print("Here is what the simulation will entail:")
    print("1. We will need to generate a random 4 digit binary value")
    print("2. We will need to calculate the redundant digits using the Hamming (7, 4) algorithm")
    print("3. Simulate a corrupt transmission by flipping a bit in the codeword")
    print("4. Use the redundant bits to correct the corrupted data")
    print("=========================================================================================================================")
    input("Click enter to generate a random 4-digit binary number...")
    
    random_binary = generate_random_binary()
    print(f"Generated 4-digit binary number: {random_binary}")
    input("Click enter to continue...")
    clear_cli()

    print("=========================================================================================================================")
    print(f"4-digit binary bits: {random_binary}")
    print("=========================================================================================================================")
    print("In the Hamming (7, 4) code, you start with 4 data bits (e.g., d1, d2, d3, d4) and add 3 redundant bits (e.g., r1, r2, r3)")
    print("This creates a 7-bit codeword. Each parity bit is calculated using an exclusive OR (XOR) operation on selected data bits.")
    print("Our redundant bits are calculated as follows:")
    print("r1 = d1 XOR d2 XOR d4")
    print("r2 = d1 XOR d3 XOR d4")
    print("r3 = d2 XOR d3 XOR d4")
    print("=========================================================================================================================")
    
    input("Press enter to calculate redundant bits...")
    clear_cli()
    redundant_bits = calculate_redundant_bits(random_binary)
    
    print("=========================================================================================================================")
    print(f"4-digit binary bits: {random_binary}")
    print(f"3-digit redundant bits: {redundant_bits}")
    print("=========================================================================================================================")
    
    print("After calculating our redundant bits, we can combine the data bits and redundant bits to create the 7-bit codeword.")
    print("Typically in Hamming (7, 4) it is structured like this: r1,r2,d1,r3,d2,d3,d4")
    input("Press enter to calculate 7-bit codeword...")
    clear_cli()
    
    seven_bit_codeword = calculate_codeword(random_binary, redundant_bits)
    print("=========================================================================================================================")
    print(f"4-digit binary bits: {random_binary}")
    print(f"3-digit redundant bits: {redundant_bits}")
    print(f"7-digit codeword: {seven_bit_codeword}")
    print("=========================================================================================================================")

    print("Now that we have our 7-digit codeword, let's simulate transmission and see if any data gets corrupted.")
    corrupted_codeword, error_position = simulate_corruption(seven_bit_codeword)
    print(f"Corrupted Codeword: {corrupted_codeword} (Error at position: {error_position})")

    print("=========================================================================================================================")
    clear_cli()
    print("=========================================================================================================================")
    print(f"4-digit binary bits: {random_binary}")
    print(f"3-digit redundant bits: {redundant_bits}")
    print(f"7-digit codeword: {seven_bit_codeword}")
    print(f"Corrupted 7-digit codeword: {corrupted_codeword} (Error at position: {error_position})")
    print("=========================================================================================================================")

    
    print("After transmission the receiver gets a 7-bit codeword. This codeword may contain errors due to transmission noise.")
    print("The receiver calculates the syndrome to detect errors and determine their positions.")
    print("A syndrome is a set of bits calculated from the received codeword that helps determine whether there are errors in the transmitted data and which bits are incorrect")
    print("If the syndrome is 000, it means there are no errors in the received codeword.")
    print("If the syndrome is non-zero (e.g., 101, 011, etc.), it indicates that there is an error, and the value of the syndrome corresponds to the position of the error.")
    print("If the syndrome indicates an error, the receiver can identify which bit is incorrect and flip it to correct the codeword.")


    corrected_codeword, error_position = correct_codeword(corrupted_codeword)
    print("")
    print("=========================================================================================================================")
    print(f"4-digit binary bits: {random_binary}")
    print(f"3-digit redundant bits: {redundant_bits}")
    print(f"7-digit codeword: {seven_bit_codeword}")
    print(f"Corrupted 7-digit codeword: {corrupted_codeword} (Error at position: {error_position})")
    if error_position:
        print(f"Corrected Codeword: {corrected_codeword} (Error corrected at position: {error_position})")
    else:
        print("No error detected. Codeword is correct.")
    print("=========================================================================================================================")

if __name__ == "__main__":
    main()  