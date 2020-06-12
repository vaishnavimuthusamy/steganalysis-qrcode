# Encryption

import sys, math
import time
 
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'
 
def main():
     # Runs a test that encrypts a message to a file or decrypts a message
     # from a file.
     filename = 'encrypted_file.txt' # The file to write to/read from.
     message = raw_input("Enter the message: ")
     pubKeyFilename = 'RSA_pubkey.txt'
     print('Encrypting and writing to %s...' % (filename)) 
     encryptedText = encryptAndWriteToFile(filename, pubKeyFilename,message)
     #print('Encrypted text:')
     #print(encryptedText)
     time.sleep(5)
 
def getBlocksFromText(message, blockSize):
     # Converts a string message to a list of block integers.
     for character in message:
         if character not in SYMBOLS:
             print('ERROR: The symbol set does not have the character %s' %(character))
             sys.exit()
     blockInts = []
     for blockStart in range(0, len(message), blockSize):
         # Calculate the block integer for this block of text:
         blockInt = 0
         for i in range(blockStart, min(blockStart + blockSize,len(message))):
             blockInt += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % blockSize))
         blockInts.append(blockInt)
     return blockInts
 
def encryptMessage(message, key, blockSize):
     # Converts the message string into a list of block integers, and then
     # encrypts each block integer. Pass the PUBLIC key to encrypt.
     encryptedBlocks = []
     n, e = key
     for block in getBlocksFromText(message, blockSize):
         # ciphertext = plaintext ^ e mod n
         encryptedBlocks.append(pow(block, e, n))
     return encryptedBlocks

def readKeyFile(keyFilename):
     # Given the filename of a file that contains a public or private key,
     # return the key as a (n,e) or (n,d) tuple value.
     fo = open(keyFilename)
     content = fo.read()
     fo.close()
     keySize, n, EorD = content.split(',')
     return (int(keySize), int(n), int(EorD))
def encryptAndWriteToFile(messageFilename, keyFilename, message,
     blockSize=None):
     # Using a key from a key file, encrypt the message and save it to a
     # file. Returns the encrypted message string.
     keySize, n, e = readKeyFile(keyFilename)
     if blockSize == None:
         # If blockSize isn't given, set it to the largest size allowed by the key size and symbol set size.
         blockSize = int(math.log(2 ** keySize, len(SYMBOLS)))
         # Check that key size is large enough for the block size:
     if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
         sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?')
     # Encrypt the message:
     encryptedBlocks = encryptMessage(message, (n, e), blockSize)
     # Convert the large int values to one string value:
     for i in range(len(encryptedBlocks)):
         encryptedBlocks[i] = str(encryptedBlocks[i])
     encryptedContent = ','.join(encryptedBlocks)
     # Write out the encrypted string to the output file:
     encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
     fo = open(messageFilename, 'w')
     fo.write(encryptedContent)
     fo.close()
     # Also return the encrypted string:
     return encryptedContent

#If publicKeyCipher.py is run (instead of imported as a module), call
# the main() function.
if __name__ == '__main__':
     main()

