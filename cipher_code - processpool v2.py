import binascii
from multiprocessing import Process

#Converts string characters into decimal ints
def to_decimal(character):
    data = ((int.from_bytes(character.encode(),'big')))
    return(data)

#Converts int to characters
def to_ascii(data):
    data = (chr(data))
    return(data)

#Runs the inputed msg and key through XOR process to encode the information
def encode_decode(file_data,key):
    #Iterates through entire message in steps of two and within each step decodes each corresponding half with its part of the key
    for x in range(0,len(file_data),2):
        #print(file_data[x],file_data[x+1],"",to_decimal(file_data[x]),to_decimal(file_data[x+1]))#This line and the one on the other side of the calculations are used for bug testing; it allows me to see if the XOR comparisons are doing their job correctly
        file_data = file_data[:x] + to_ascii(to_decimal(file_data[x])^to_decimal(key[0])) + file_data[x + 1:]
        file_data = file_data[:x + 1] + to_ascii(to_decimal(file_data[x+1])^to_decimal(key[1])) + file_data[x + 2:]
        #print(file_data[x],file_data[x+1],"",to_decimal(file_data[x]),to_decimal(file_data[x+1]))
    return(file_data)

#Takes file name and turns the file into a data string
def file_to_data(file_name):
    print(file_name)
    file = open(file_name,'r')
    file_data = file.read() 
    print ("Character Count :",len(file_data))
    if ((len(file_data) % 2) == 1):
        file_data += " "
        print("Odd Number character count, space added to end")
    return(file_data)

#This is the actual brute for algorithm that the different processes call to use
def brute_force(index,start,file_data,common_words):
    print("Begin Brute-Force")
    for i in range(start,start+16):
        for j in range(128):
            key = (to_ascii(i),to_ascii(j))
            candidate = encode_decode(file_data,key)
            #print(key) #Can change from being a comment to print each key that has been checked, mainly used for trouble-shooting
            if any(dict_str in candidate for dict_str in common_words): 
                print("Key:",key)
                #print("Detected", dict_str)
                print(candidate)   

if __name__ == "__main__":
    
    common_words = [
        " if ",
        " the ",
        " was ",
        " that ",
        " too ",
        " stone ",
        " die ",
        " kick ",
        " christ ",
        " disco ",
        " this ",
        " we ",
        " they ",
        " there ",
        " but ",
        " not ",
        " go ",
        " when ",
        " so, ",
        " so ",
        " tuxedo ",
        " first ",
        " last ",
        " over ",
        " try ",
        " state ",
        " ever ",
        " out "
    ]
    
    #This input allows you to determine what you want to do
    choice = input("Input '1' for encrypt/decrypt or '2' for brute force\n")
    str(choice)
    
    #This checks to make sure that either 1 or 2 was input; else nothing will happen and the program will end
    if choice == "1" or choice == "2":
        #Input for file name and key
        file_name = input("Input the file name: ")
        #Calling function to retrieve file data
        file_data = file_to_data(file_name)
    
    #This is encryption/decryption choice
    if choice == "1":
        key = input("Input a 2-character key: ")
        coded = encode_decode(file_data,key)
        recoded = encode_decode(coded,key)
        print(coded)
        print(recoded)
    
    #This is the brute force choice
    if choice == "2":
        
        #Defines process list for checkcing multiple sections of data at the same time
        my_process = [None] * 8
        
        #This section of for loops assigns processes, starts them, then joins them once all done
        for index in range(8):
            start = index*16
            my_process[index] = Process(target = brute_force, args = (index,start,file_data,common_words))            
        for index in range(8):
            my_process[index].start()
        for index in range(8):
            my_process[index].join()        
