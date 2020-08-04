import os
from os.path import join, isfile
import subprocess


def yes_no(text):
    answer = input(text + " [y/N] ").upper()
    if answer == "Y" or answer == "YE" or answer == "YES":
        return True
    else:
        return False

def flac_to_mp3(flacs, bitrate):
    for flac in flacs:
        subprocess.run(["ffmpeg", "-i", flac, "-b:a", str(bitrate*1000), f'{flac[:-5]}.mp3'])


flacs = []
for root, dirs, files in os.walk("."):
    for name in files:
        f = os.path.join(root, name)
        if isfile(f) and f.endswith(".flac"):
            flacs.append(f)

if flacs == []:
    print("No flac file found in current directory and subdirectories")
    exit()

if yes_no("Display found flac files ?"):
    count = 1
    for flac in flacs:
        print(count, "", flac)
        count += 1


bitrates =[320, 256, 128, 96]
choice = 0
try:
    print("")
    count = 1
    for bitrate in bitrates:
        print(count, "", bitrate, "kbps")
        count += 1
    choice = int(input("Select a bitrate [1-4] "))
    if choice < 1 or choice > 4:
        raise Error
except:
    print("Invalid selection, aborting")
    exit()


if yes_no("\nConvert everything ?"):
    choice2 = 1
    choice3 = len(flacs)
else:
    if len(flacs) > 1:
        print("\nSelect the desired range ( from 1 to", len(flacs),")")
        try:
            choice2 = int(input("First track : "))
            choice3 = int(input("Last track : "))
            if choice3 < choice2 or choice2 < 0 or choice3 < 0 or choice2 > len(flacs) or choice3 > len(flacs):
                raise Error
        except:
            print("Invalid selection, aborting")
            exit()
    else:
        exit()

flacs = flacs[choice2-1:choice3]
flac_to_mp3(flacs, bitrates[choice-1])

if yes_no("Remove successfully converted flac files ?"):
    if yes_no("Are you sure ?"):
        for flac in flacs:
            check_mp3 = flac[:-4]+"mp3"
            if isfile(check_mp3):
                os.remove(flac)
