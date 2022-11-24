import socket
import os
import tqdm
import random
import zlib
import time
from threading import Thread

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
MAX_INPUT = 1500
sender_IP = "127.0.0.1"
sender_PORT = 5001
receiver_IP = "127.0.0.1"
receiver_PORT = 8030
sender_ADDR = (sender_IP, sender_PORT)
receiver_ADDR = (receiver_IP, receiver_PORT)

mode = input("choose mode (sender or receiver) or exit: ")
while True:
    if (mode == "sender"):
        ackNum = random.randrange(1, 16383)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(sender_ADDR)



        def Approving_Transmission(ackNum):
            s.settimeout(5)
            try:
                package_read, receiver_ADDR = s.recvfrom(MAX_INPUT)
                ack_read = int(int.from_bytes(package_read[0:8], byteorder='big', signed=True))
                flags_read = int(int.from_bytes(package_read[16:17], byteorder='big', signed=True))
                return (ack_read == ackNum and flags_read == 2)
            except socket.timeout as err:
                return False

        def Approving_Connection(ackNum):
            s.settimeout(2)
            package_read, receiver_ADDR = s.recvfrom(MAX_INPUT)
            ack_read = int(int.from_bytes(package_read[0:8], byteorder='big', signed=True))
            flags_read = int(int.from_bytes(package_read[16:17], byteorder='big', signed=True))
            if (ack_read == (ackNum + 32768) and flags_read == 3):
                print("A server is ready to establish a connection. Approving...")
                time.sleep(1)
                ackNum = ack_read + 1
                ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                flagsToSend = int(2).to_bytes(1, byteorder='big', signed=True)
                package_full = ackToSend + sumToSend + flagsToSend
                s.sendto(package_full, receiver_ADDR)
            else:
                print("An error occured during an establishment.")
                print(ack_read, ackNum, flags_read)
            return ackNum

        def Approving_Disconnect(ackNum):
            s.settimeout(2)
            package_read, receiver_ADDR = s.recvfrom(MAX_INPUT)
            ack_read = int(int.from_bytes(package_read[0:8], byteorder='big', signed=True))
            flags_read = int(int.from_bytes(package_read[16:17], byteorder='big', signed=True))
            if (ack_read == (ackNum + 1) and flags_read == 7):
                print("A server is ready to end a connection. Approving...")
                time.sleep(1)
                ackNum = ack_read + 1
                ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                flagsToSend = int(2).to_bytes(1, byteorder='big', signed=True)
                package_full = ackToSend + sumToSend + flagsToSend
                s.sendto(package_full, receiver_ADDR)
            else:
                print("An error occured during an establishment.")
                print(ack_read, ackNum, flags_read)

        def Wait_Transmission():
            global thread_running

            start_time = time.time()
            while thread_running:
                time.sleep(0.1)

                if time.time() - start_time >= 5:
                    start_time = time.time()
                    ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                    sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                    flagsToSend = int(4).to_bytes(1, byteorder='big', signed=True)
                    package_full = ackToSend + sumToSend + flagsToSend
                    s.sendto(package_full, receiver_ADDR)

        def Wait_Input():
            global filename
            filename = input("write a name of a file to send, 'exit' to terminate the program or 'change' to become a receiver: ")

        receiver_IP = input("Enter receiver's IP: ")
        receiver_PORT = input("Enter receiver's port: ")

        ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
        sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
        flagsToSend = int(1).to_bytes(1, byteorder='big', signed=True)
        firstPackage = ackToSend + sumToSend + flagsToSend
        print("Establishing a connection with a server.")
        s.sendto(firstPackage, receiver_ADDR)
        ackNum = Approving_Connection(ackNum)



        while True:
            thread_running = True

            progress = 0

            t1 = Thread(target=Wait_Transmission)
            t2 = Thread(target=Wait_Input)

            t1.start()
            t2.start()

            t2.join()


            if (filename != "exit" and filename != "change"):
                if (os.path.isfile(filename)):

                    BUFFER_SIZE = int(input("select the size of a package(up to a 1455): "))
                    thread_running = False
                    filesize = os.path.getsize(filename)
                    if (BUFFER_SIZE > 1455):
                        print("selected size is above maximum. Size of a package shanged to 1455 bytes.")
                        BUFFER_SIZE = 1455
                    else:
                        print("selected size: ", BUFFER_SIZE, " bytes.")

                    if (filesize < BUFFER_SIZE):
                        numOfPackages = 1
                    else:
                        numOfPackages = int(filesize / BUFFER_SIZE) + 1
                    print("The file ", filename, " will be delivered in ", numOfPackages, " package(s).")
                    filepath = os.path.abspath(filename)
                    print(filename," is located in ", filepath)
                    ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                    sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                    flagsToSend = int(0).to_bytes(1, byteorder='big', signed=True)
                    firstPackage = ackToSend + sumToSend + flagsToSend + f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{BUFFER_SIZE}{SEPARATOR}{numOfPackages}".encode()
                    s.sendto(firstPackage, receiver_ADDR)
                    print("Starting transmittion.")
                    # start sending the file
                    progress = tqdm.tqdm(range(filesize), f"Sending {filename} ", unit="B", unit_scale=True, unit_divisor=1024, leave = False)
                    print("")
                    with open(filename, "rb") as f:
                        while True:
                            packageToSend = f.read(BUFFER_SIZE)
                            sum = zlib.adler32(packageToSend)
                            if not packageToSend:
                                break
                            ackNum += 1
                            ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                            sumToSend = sum.to_bytes(8, byteorder='big', signed=True)
                            flagsToSend = int(0).to_bytes(1, byteorder='big', signed=True)
                            package_full = ackToSend + sumToSend + flagsToSend + packageToSend
                            s.sendto(package_full, receiver_ADDR)
                            print("Package sent.")
                            if (Approving_Transmission(ackNum)):
                                print("Transmission approved.")
                            else:
                                print("An error occured during a transmission. Resending last packet.")
                                ERROR = 1
                                while (ERROR < 3):
                                    s.sendto(package_full, receiver_ADDR)
                                    if (Approving_Transmission(ackNum)):
                                        break
                                    print("An error occured during a transmission. Resending last packet.")
                                    ERROR += 1
                                if (ERROR == 3):
                                    print("NO APPROVING FOR 3 TRIES, FULL RESET")
                                    ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                                    sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                                    flagsToSend = int(5).to_bytes(1, byteorder='big', signed=True)
                                    package_full = ackToSend + sumToSend + flagsToSend
                                    s.sendto(package_full, receiver_ADDR)
                                    s.close()
                                    exit()

                            progress.update(len(packageToSend))
                            print("")

                        process = 0


                elif (filename == "change"):
                    mode = "receiver"
                elif (filename == "exit"):
                    exit()
                else:
                    print(filename, " is not a file.")
            else:
                thread_running = False
                progress = 0
                ackNum += 1
                ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                flagsToSend = int(6).to_bytes(1, byteorder='big', signed=True)
                package_full = ackToSend + sumToSend + flagsToSend
                s.sendto(package_full, receiver_ADDR)
                print("Sending a request to end a connection.")
                Approving_Disconnect(ackNum)
                s.close()
                exit()
    elif (mode == "receiver"):
        task = input("write nothing to stay as a receiver, 'change' to become a sender and 'exit' to exit: ")
        if (task == ""):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.bind(receiver_ADDR)


            def Check_Checksum(package_read):
                a = int(int.from_bytes(package_read[8:16], byteorder='big', signed=True))
                b = zlib.adler32(package_read[17:])
                # """
                global i
                global small_error
                if (i == 1 and small_error == 1):
                    small_error = 0
                    a += 1
                # """
                return (a == b)

            def Package_Received(ack_read):
                # """
                #time.sleep(1)
                # """
                ackToSend = ack_read.to_bytes(8, byteorder='big', signed=True)
                sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                flagsToSend = int(2).to_bytes(1, byteorder='big', signed=True)
                package_send = ackToSend + sumToSend + flagsToSend
                s.sendto(package_send, sender_ADDR)
                print("Approving transmission.")

            def Reset():
                print("Resieved RST flag. Aborting.")
                s.close()
                exit()
            package_read = s.recv(MAX_INPUT)
            ack_read = int(int.from_bytes(package_read[0:8], byteorder='big', signed=True))
            flags_read = int(int.from_bytes(package_read[16:17], byteorder='big', signed=True))
            if (flags_read == 1):
                ackNum = ack_read + 32768
                ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                flagsToSend = int(3).to_bytes(1, byteorder='big', signed=True)
                package_send = ackToSend + sumToSend + flagsToSend
                time.sleep(1)
                s.sendto(package_send, sender_ADDR)
                print("Received a connection establishment message. Approving connection.")


                package_read, receiver_ADDR = s.recvfrom(MAX_INPUT)
                ack_read = int(int.from_bytes(package_read[0:8], byteorder='big', signed=True))
                flags_read = int(int.from_bytes(package_read[16:17], byteorder='big', signed=True))
                if (ack_read == (ackNum + 1) and flags_read == 2):
                    print("A connection establishment approved.")
                else:
                    print("An error occured during an establishment approval.")
                    print(ack_read, ackNum, flags_read)
            s.settimeout(10)

            while True:
                package_read = s.recv(MAX_INPUT)
                ack_read = int(int.from_bytes(package_read[0:8], byteorder='big', signed=True))
                flags_read = int(int.from_bytes(package_read[16:17], byteorder='big', signed=True))
                if (flags_read == 0):

                    properties = package_read[17:].decode()
                    filename, filesize, packageSize, numOfPackages = properties.split(SEPARATOR)
                    packageSize = int(packageSize)
                    numOfPackages = int(numOfPackages)
                    filename = os.path.basename(filename)
                    filesize = int(filesize)



                    i = 0
                    small_error = 1
                    with open(filename, "wb") as f:
                        while (i < numOfPackages):
                            package_read, receiver_ADDR = s.recvfrom(MAX_INPUT)

                            ack_read = int(int.from_bytes(package_read[0:8], byteorder='big', signed=True))
                            sum_read = int(int.from_bytes(package_read[8:16], byteorder='big', signed=True))
                            sum_received = zlib.adler32(package_read[17:])
                            flags_read = int(int.from_bytes(package_read[16:17], byteorder='big', signed=True))
                            if (flags_read == 5):
                                Reset()
                            print("Recieved a package: ", (i + 1), "/", numOfPackages, " of ", filename)
                            if (Check_Checksum(package_read)):
                                Package_Received(ack_read)
                                f.write(package_read[17:])
                                i += 1

                        filepath = os.path.abspath(filename)
                        print("")
                        print("Recieved a file")
                        print("filename: ", filename)
                        print("located in: ", filepath)
                        print("completed from ", numOfPackages, " packages with ", packageSize,"B each.")

                elif (flags_read == 6):
                    ackNum = ack_read + 1
                    ackToSend = ackNum.to_bytes(8, byteorder='big', signed=True)
                    sumToSend = int(0).to_bytes(8, byteorder='big', signed=True)
                    flagsToSend = int(7).to_bytes(1, byteorder='big', signed=True)
                    package_send = ackToSend + sumToSend + flagsToSend
                    time.sleep(1)
                    s.sendto(package_send, sender_ADDR)
                    print("Received a connection ending message. Approving disconnect.")

                    package_read, receiver_ADDR = s.recvfrom(MAX_INPUT)
                    ack_read = int(int.from_bytes(package_read[0:8], byteorder='big', signed=True))
                    flags_read = int(int.from_bytes(package_read[16:17], byteorder='big', signed=True))
                    if (ack_read == (ackNum + 1) and flags_read == 2):
                        print("A connection disconnect approved.")
                        s.close()
                        break
                    else:
                        print("An error occured during establishing approval.")
                        print(ack_read, ackNum, flags_read)
                        s.close()
                        break

                elif (flags_read == 5):
                    Reset()

                elif (flags_read == 4):
                    print("Asked to wait. Waiting...")

                else:
                    print("Unknown flag. Aborting.")
                    s.close()
                    exit()
        elif (task == "change"):
            mode = "sender"
        elif (task == "exit"):
            exit()
        else:
            print("wrong input.")
    elif (mode == "exit"):
        exit()

    else:
        print("wrong input.")
