import pygame
import os
import sys
import math
import time
import random
#from PIL import Image, ImageFilter
import websockets
import asyncio
import threading

from pathlib import Path
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption("igrica!!")
THISFILE = Path(__file__).resolve().parent
happy1Dir = THISFILE / "happy1.png"
happy2Dir = THISFILE / "happy2.png"
suprisedDir = THISFILE / "suprised.png"
waveAnimDir = THISFILE / "waveAnim.png"
smallrock1Dir = THISFILE / "smallrock1.png"
grassDir = THISFILE / "grass.png"
fontDir = THISFILE / "Tiny5-Regular.ttf"
font = pygame.font.Font(str(fontDir), 40)
fontSmall = pygame.font.Font(str(fontDir), 10)
happy1Img = pygame.image.load(happy1Dir)
happy2Img = pygame.image.load(happy2Dir)
suprisedImg = pygame.image.load(suprisedDir)
waveAnimImg = pygame.image.load(waveAnimDir).convert_alpha()
waveAnimFrame = waveAnimImg.subsurface(pygame.Rect(0, 0, 32, 32))
smallRock1Img = pygame.image.load(smallrock1Dir)
smallRock1OnHeadImg = pygame.image.load(smallrock1Dir)
smallRock1OnHeadImg = pygame.transform.scale(smallRock1OnHeadImg, (24,24))
grassImg = pygame.image.load(grassDir)
grassImg = pygame.transform.scale(grassImg, (64,64))
clock = pygame.time.Clock()
posX = 200
posY = 125
iconState = 1
waveAnimState = 0
haveRock = False
lastXMove = 0
lastYMove = 0
ismousedown=False
NamePopup = True
pulseRed = 0
ofSenPData = False
global Connected
#Connected = False
Name = ""
returnData = ()
global packetData
packetData = ""
response = ""
otherPlayer = []
packetData = ""
uri = "ws://localhost:8765"
class FireAndForgetWebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.connected = asyncio.Event()
        self.send_queue = asyncio.Queue()

    async def connect(self):
        while True:
            try:
                print("Connecting to server...")
                self.websocket = await websockets.connect(self.uri)
                self.connected.set()
                print("Connected to server.")
                asyncio.create_task(self.listen())
                asyncio.create_task(self.process_send_queue())
                break
            except Exception as e:
                print(f"Connection failed: {e}, retrying in 2s...")
                await asyncio.sleep(2)

    async def listen(self):
        global packetData
        try:
            async for message in self.websocket:
                print(f"[RECEIVED]: {message}")
                packetData = message
        except Exception as e:
            print(f"Listen error: {e}")
        finally:
            self.connected.clear()
            await self.connect()

    async def process_send_queue(self):
        while True:
            await self.connected.wait()
            packet = await self.send_queue.get()
            try:
                await self.websocket.send(packet)
                print(f"[SENT]: {packet}")
            except Exception as e:
                print(f"Send failed: {e}")

    async def send(self, packet):
        await self.send_queue.put(packet)

client = FireAndForgetWebSocketClient(uri)

async def sendPacket(packet):
    await client.send(packet)

def startLoop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop = asyncio.new_event_loop()
threading.Thread(target=startLoop, args=(loop,), daemon=True).start()
#asyncio.run_coroutine_threadsafe(client.connect(), loop)

def runAsync(coro):
    return asyncio.run_coroutine_threadsafe(coro, loop)
#blurRect = pygame.Rect(0,0,800,500)
#blurSubsurface = screen.subsurface(blurRect).copy()
#bgBlur = pygame.image.fromstring(
#    Image.frombytes("RGB", blurRect.size, pygame.image.tostring(blurSubsurface, "RGB"))
#    .filter(ImageFilter.GaussianBlur(4))
#    .tobytes(), blurRect.size, "RGB")
#smallRocksPos = [(150,100),(200,200)]
smallRocksPos = [(100,100)]
StartTime = time.time()
print(StartTime)

#def startLoop(loop):
#    asyncio.set_event_loop(loop)
#    loop.run_forever()
#loop = asyncio.new_event_loop()
#threading.Thread(target=startLoop, args=(loop,), daemon=True).start()
#def runAsync(coroutine):
#    asyncio.run_coroutine_threadsafe(coroutine, loop)
#global packetPlayerName
#global packetPlayerX
#global packetPlayerY
#global packetPlayerState
#global packetPlayerSubState
#global packetPlayerHasRock #= False
rockPopID = ""
rockAddX = ""
rockAddY = ""

def clearPDataByName(name):
    for i in range(len(otherPlayer)):
        if otherPlayer[i][0] == name:
            return int(i)
            
def deobfPacketDataRock(data):
    idx = 5
    rockPopID = ""
    rockAddX = ""
    rockAddY = ""
    if data[3] =="p":
        while data[idx] != ";":
            print(idx)
            rockPopID += data[idx]
            idx += 1
        
        return rockPopID
    if data[3] =="a":
        while data[idx] != ",":
            rockAddX += data[idx]
            idx += 1
        idx += 1
        while data[idx] != ";":
            rockAddY += data[idx]
            idx += 1
        return (rockAddX,rockAddY)
packetPlayerName = ""
packetPlayerX = ""
packetPlayerY = ""
packetPlayerState = ""
packetPlayerSubState = ""
packetPlayerHasRock = False
def deobfPacketDataPlayer(data):
    print(data)
    packetPlayerName = ""
    packetPlayerX = ""
    packetPlayerY = ""
    packetPlayerState = ""
    packetPlayerSubState = ""
    packetPlayerHasRock = False
    idx = 3
    while data[idx] != ";":
        packetPlayerName += data[idx]
        idx += 1
    print(packetPlayerName)
    idx += 1
    while data[idx] != ",":
        packetPlayerX += data[idx]
        idx += 1
    print("X:" + packetPlayerX)
    idx += 1
    while data[idx] != ";":
        packetPlayerY += data[idx]
        idx += 1
    print(packetPlayerY)
    idx += 1
    while data[idx] != ";":
        packetPlayerState += data[idx]
        idx += 1
    idx += 1
    print(packetPlayerState)
    #print(idx)
    #print(data[idx])
    while data[idx] != ";":
        packetPlayerSubState += data[idx]
        idx += 1
    idx += 1
    print(packetPlayerSubState)
    if data[idx] == "F":
        packetPlayerHasRock == False
    if data[idx] == "T":
        packetPlayerHasRock == True
    return (packetPlayerName, packetPlayerX, packetPlayerY, packetPlayerState, packetPlayerSubState, packetPlayerHasRock)
#def doBlur(blur):
#    blurSubsurface = screen.subsurface(blurRect).copy()
#    bgBlur = pygame.image.fromstring(
#    Image.frombytes("RGB", blurRect.size, pygame.image.tostring(blurSubsurface, "RGB"))
#    .filter(ImageFilter.GaussianBlur(blur))
#    .tobytes(), blurRect.size, "RGB")
def isANameChar(char):
    if char == " " or char == "_" or char == "-" or char == "." or char == "*":return True
    elif char.isnumeric():return True
    elif char.isalpha():return True
    else:return False
#pressedKey = ""
#screen = pygame.transform.grayscale(screen)
asyncio.run_coroutine_threadsafe(client.connect(), loop)
while NamePopup:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(Name) >= 3 and len(Name) <= 12:
                NamePopup = False
            if event.key == pygame.K_RETURN and not len(Name) >= 3:pulseRed = 255
            if event.key == pygame.K_BACKSPACE:
                Name = Name[:-1]
            elif isANameChar(event.unicode) and len(Name) < 12:Name += event.unicode

    screen.fill("#2edf3e")
    for i in range(13):
        for j in range(8):
            screen.blit(grassImg, ((i*64),(j*64)))
    #doBlur(4)
    #screen.blit(bgBlur, blurRect.topleft)
    screen.blit(font.render("Vpiši Ime:", True, "#000000"), (250,175))
    pygame.draw.rect(screen, (pulseRed,0,0), (250,225,300,60)) #300 max(300,font.size(Name + "W")[0])
    pygame.draw.rect(screen, "#4d4d4d", (260,235,280,40)) #280
    screen.blit(font.render(Name, True, "#ffffff"), (265,235)) #shouldve bemm 275
    pulseRed *= 0.94
    if pulseRed <=1:pulseRed = 0
    pygame.display.flip()
    clock.tick(60)

runAsync(sendPacket("{n;"+Name+"}"))
runAsync(sendPacket("{n;req"))
#asyncio.run_coroutine_threadsafe(client.connect(), loop)
#runAsync(sendPacket("{n;"+Name+"}"))
#runAsync(sendPacket("{n;req"))
while False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill("#2edf3e")
    for i in range(13):
        for j in range(8):
            screen.blit(grassImg, ((i*64),(j*64)))
    #doBlur(4)
    #screen.blit(bgBlur, blurRect.topleft)
    screen.blit(font.render("waiting for server", True, "#000000"), (0,0))
    print(client.Connected)
    pygame.display.flip()
    clock.tick(60)

#while packetData == "successfullyAddedName" or packetData == "0":
while packetData == "a":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill("#2edf3e")
    for i in range(13):
        for j in range(8):
            screen.blit(grassImg, ((i*64),(j*64)))
    #doBlur(4)
    #screen.blit(bgBlur, blurRect.topleft)
    screen.blit(font.render("waiting to connect", True, "#000000"), (0,0))
    pygame.display.flip()
    clock.tick(60)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            ismousedown=True
            #print("aaa")
            if haveRock and posX+(48*lastXMove) >= 0 and posX+(48*lastXMove) <= 768 and posY+(48*lastYMove) >= 0 and posY+(48*lastYMove) <= 468:
                smallRocksPos.append((posX+(48*lastXMove),posY+(48*lastYMove)))
                print((posX+(48*lastXMove),posY+(48*lastYMove)))
                print(str((posX+(48*lastXMove),posY+(48*lastYMove))))
                print(smallRocksPos)
                haveRock = False
                ismousedown = False
                runAsync(sendPacket("{r;a;"+str(posX+(48*lastXMove))+","+str(posY+(48*lastYMove))+";}"))
        if event.type == pygame.MOUSEBUTTONUP:
            ismousedown=False
    screen.fill("#2edf3e")
    for i in range(13):
        for j in range(8):
            
            screen.blit(grassImg, ((i*64),(j*64)))
    pressedKey = pygame.key.get_pressed()
    if pressedKey[pygame.K_RIGHT]:
        posX += 1
        lastXMove = 1
        lastYMove = 0
    if pressedKey[pygame.K_LEFT]:
        posX -= 1
        lastXMove = -1
        lastYMove = 0
    if pressedKey[pygame.K_DOWN]:
        posY += 1
        lastYMove = 1
        lastXMove = 0
    if pressedKey[pygame.K_UP]:
        posY -= 1
        lastYMove = -1
        lastXMove = 0
    if posX < 0:
        posX = 0
    if posY < 0:
        posY = 0
    if posX > 768:
        posX = 768
    if posY > 468:
        posY = 468
    if iconState == 0:
        screen.blit(happy1Img, (posX,posY))
    if iconState == 1:
        screen.blit(happy2Img, (posX,posY))
    if iconState == 2:
        screen.blit(suprisedImg, (posX,posY))
    if iconState == 3:
        screen.blit(waveAnimFrame, (posX,posY))
        #print(math.floor(waveAnimState))
        #print(math.floor(waveAnimState / 2))
        #print((math.floor((waveAnimState+1)/2) % 2) + ""+str(math.floor(waveAnimState / 2)))
        #waveAnimFrame = waveAnimImg.subsurface(pygame.Rect(32*(math.floor(waveAnimState) % 2),math.floor(waveAnimState / 2)*32, 32, 32))
        waveAnimFrame = waveAnimImg.subsurface(pygame.Rect(32*(math.floor((waveAnimState+1)/2) % 2),math.floor(waveAnimState / 2)*32, 32, 32))
        waveAnimState += 4 / 60
        if waveAnimState >= 4:
            waveAnimState = 0
    if haveRock == True:screen.blit(smallRock1OnHeadImg, (posX+4,posY-24))
    if time.time() - StartTime >= 1 and not ofSenPData:
        runAsync(sendPacket("{p;"+Name+";"+str(posX)+","+str(posY)+";"+str(iconState)+";"+str(1)+";"+str(haveRock)))
        ofSenPData = True
    for i in range(len(smallRocksPos)):
        #print(smallRocksPos[i])
        screen.blit(smallRock1Img, (smallRocksPos[i][0],smallRocksPos[i][1]))
    if ismousedown:
        for i in range(len(smallRocksPos)): #have to double cause it popped before it got to the other rock
            if posX >= smallRocksPos[i][0]-32 and posX <= smallRocksPos[i][0]+32 and posY >= smallRocksPos[i][1]-32 and posY <= smallRocksPos[i][1]+32 and haveRock == False:
                print("rock!")
                smallRocksPos.pop(i) 
                print(smallRocksPos)
                haveRock = True 
                runAsync(sendPacket("{r;p;"+str(i)+";}"))
                break
    if time.time() - StartTime >= 2 and iconState < 2:
        StartTime = time.time()
        iconState = 1-iconState
        ofSenPData = False
        #runAsync(sendPacket("{p;p;"+str(i)+"}"))
    #print("packetData"[:-(len("packetData")-3)])
    #print(packetData)
    #if packetData[:-(len(packetData)-3)] == "{p;":print("adasd")
    if packetData[:-(len(packetData)-3)] == "{p;":
        returnData = deobfPacketDataPlayer(packetData)
        print(returnData)
        print(returnData[0])
        print(clearPDataByName(returnData[0]))
        otherPlayer[int(clearPDataByName(returnData[0]))] = str((returnData[0],int(returnData[1]),int(returnData[2]),int(returnData[3]),int(returnData[4]),returnData[5],0))
    #    print("playerX:"+returnData[1])
    #    print("playerY:"+returnData[2])
    #    screen.blit(happy1Img, (int(returnData[1]),int(returnData[2])))
    if packetData[:-(len(packetData)-3)] == "{r;":
        returnData = deobfPacketDataRock(packetData)
        if packetData[3]=="p":
            smallRocksPos.pop(int(returnData[0]))
            packetData = "" #clear cuz useless
        else:
            print("invalid quoteunquote:"+str(returnData[0])+", "+str(returnData[1]))
            smallRocksPos.append((int(returnData[0]),int(returnData[1])))
            packetData = "" #clear cuz useless

    for i in range(len(otherPlayer)):
        print("len "+str(len(otherPlayer)))
        print("lenF "+str(otherPlayer))
        screen.blit(happy1Img, (otherPlayer[i+1][1],otherPlayer[i+1][2]))
    pygame.display.flip()
    clock.tick(60)
