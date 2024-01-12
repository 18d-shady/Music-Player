import pygame
from pygame import mixer
import math
import sys
import os
import random 


counter = 0
pygame.init()
mixer.init()
screen = pygame.display.set_mode((700, 500))
running = True
names = []
#for rectangle
recc = []
searchRecc = []
filepaths = []
searchResult = []
i = 0
music = ".mp3"
rec = '$Recycle.Bin'
musicChoosed = 0
newPos = 0
shuffle = 0
volumeVal = 0.7
volumeVals = []
searchCount = 0
searched = ''
playNext = 0
queueRecc = []
queueVal = 0

"""
def nextPage(i):
    j = i
    while i > 10:
        i = i % 10
    return i, j
"""
def searchPage():
    global searchResult
    global searchCount
    global searched

    #a count to show that the search page is active
    searchCount = 1
    #searched = "Abba"
    #clear the seach list to be the same with searchresult
    searchRecc.clear()
    #search through the names with the keyboard input
    searchResult  = [index for (index, item) in enumerate(names) if searched.lower() in item.lower()]
    #print(searchResult)
    #add the searchrecc list
    j = 40
    for r in range(len(searchResult)):
        searchRecc.append(pygame.Rect(0, j, 700, 35))
        if j >= 355:
            break
        else:
            j = j + 35

    new_surface = pygame.Surface((700, 390))
    new_surface.fill("#160521")
    font = pygame.font.SysFont("Arial", 25)
    new_surface.blit(font.render(f"Search Result for {searched}", True, "white"), (70, 5))
    pygame.draw.rect(new_surface, "grey", prevPage, 1)

    #previous
    pygame.draw.line(new_surface, "grey", (20, 10), (10, 20), 2)
    pygame.draw.line(new_surface, "grey", (10, 20), (20, 30), 2)
    pygame.draw.line(new_surface, "grey", (40, 10), (30, 20), 2)
    pygame.draw.line(new_surface, "grey", (30, 20), (40, 30), 2)
    
    pygame.draw.line(new_surface, "grey", (0, 39), (700, 39))

    #display search result
    for j in range(len(searchRecc)):
        font = pygame.font.SysFont("Arial", 15)
        #draw d rectangles
        pygame.draw.rect(new_surface, "#160521", searchRecc[j])
        searchName = searchResult[j]
        new_surface.blit(font.render(names[searchName], True, "white"), (5, (j*35)+50))
        
            

    screen.blit(new_surface, (0, 0))
    pygame.display.update()


def getMusic(num):
    """
    this function displays the songs gotten from
    the local machine and appended in the array above
    """
    global i
    #to not display the search window
    global searchCount
    searchCount = 0
    searchRecc.clear()
    
    new_surface = pygame.Surface((700, 390))
    new_surface.fill("#160521")
    font = pygame.font.SysFont("comicsansms", 25)
    new_surface.blit(font.render("Davis Music App", True, "white"), (250, 5))
    pygame.draw.rect(new_surface, "grey", nextPage, 1)
    pygame.draw.rect(new_surface, "grey", prevPage, 1)
    #next
    pygame.draw.line(new_surface, "grey", (660, 10), (670, 20), 2)
    pygame.draw.line(new_surface, "grey", (670, 20), (660, 30), 2)
    pygame.draw.line(new_surface, "grey", (680, 10), (690, 20), 2)
    pygame.draw.line(new_surface, "grey", (690, 20), (680, 30), 2)
    #previous
    pygame.draw.line(new_surface, "grey", (20, 10), (10, 20), 2)
    pygame.draw.line(new_surface, "grey", (10, 20), (20, 30), 2)
    pygame.draw.line(new_surface, "grey", (40, 10), (30, 20), 2)
    pygame.draw.line(new_surface, "grey", (30, 20), (40, 30), 2)

    pygame.draw.rect(new_surface, "grey", searchRect, 1)
    font = pygame.font.SysFont("comicsansms", 20)
    new_surface.blit(font.render("Search", True, "white"), (565, 5))
    
    pygame.draw.line(new_surface, "grey", (0, 39), (700, 39))
    

    try:
        if num != 1:
            i = i - 20
            if i < 0:
                i = 0
        for j in range(40, 390, 35):
            font = pygame.font.SysFont("Arial", 15)
            #draw d rectangles
            #recc.append(pygame.Rect(0, j, 700, 35))
            pygame.draw.rect(new_surface, "#160521", recc[i])
            new_surface.blit(font.render(names[i], True, "white"), (5, j+10))
            #for the play next
            pygame.draw.rect(new_surface, "#160521", queueRecc[i])
            new_surface.blit(font.render("Play Next", True, "white"), (635, j+10))
            i = i + 1
                
    except IndexError:
        i = 0
        getMusic(1)

    screen.blit(new_surface, (0, 0))
    pygame.display.update()
    #return i

    

def chooseMusic(numm):
    global musicChoosed
    #so that the position of the music will reset
    #and not continue from the last time you pressed
    #next 10 sec
    global newPos
    newPos = 0
    #for the queue to reset
    global playNext
    playNext = 0
    #print(nextShuf, len(names))
    
    #for previous button
    if numm == 1:
        if shuffle == 2:
            musicChoosed = random.randint(0, len(names))
        else:
            musicChoosed = musicChoosed - 1
    #for next button
    elif numm == 2:
        if shuffle == 2:
            musicChoosed = random.randint(0, len(names))
        else:
            musicChoosed = musicChoosed + 1
    #for choosing a music
    else:
        musicChoosed = musicChoosed
        
    #to choose the music clicked
    #print(f"clicked {musicChoosed}")
    #choosen = filepaths[choice]+'.mp3'
    mixer.music.unload()
    try:
        mixer.music.load(filepaths[musicChoosed])
        #mixer.music.set_volume(0.7)
        mixer.music.play()
        #display the music playing
        #put a rectangle under 
        pygame.draw.rect(screen, "#160521", (0, 480, 700, 20))
        font = pygame.font.SysFont("Arial", 12)
        screen.blit(font.render(f"Now playing: {names[musicChoosed]}", True, "white"), (5, 480))
        

    except pygame.error:
        chooseMusic(2)
    except IndexError:
        musicChoosed = 0
    pause()


def fastForward(num):
    global newPos
    
    if newPos > 0:
        curPos = newPos
        if num == 1:
            newPos =  curPos + 10
            #print(newPos)
        else:
            newPos =  curPos - 10
            #print(newPos)
    else:        
        curPos = mixer.music.get_pos()
        #print(curPos)
        if num == 1:
            newPos =  (curPos / 1000) + 10
            #print(newPos)
        else:
            newPos =  (curPos / 1000) - 10
            #print(newPos)

    if newPos <= 0:
        chooseMusic(3)
    else:
        try:
            mixer.music.rewind()
            mixer.music.set_pos(newPos)
        except pygame.error:
            chooseMusic(2)
            
    #print(mixer.music.get_pos())
    

    

def displayy():
    """
    this is the main function that displays the root window
    """
    screen.fill("#160521")
    playy()
    getMusic(1)
    pygame.draw.line(screen, "white", (0, 390), (700, 390))
    

def volumeBar(val):
    #pygame.draw.rect(screen, "white", (600, 440, 80, 3))
    #drawing the volume bar on the screen
    value = val * 10
    for v in range(len(volumeVals)):
        if v <= value:
            pygame.draw.rect(screen, "blue", volumeVals[v])
        else:
            pygame.draw.rect(screen, "white", volumeVals[v])
    mixer.music.set_volume(val)

def togShuffle():
    #shuffle
    #drawing the shufffle buttons on the screen
    font = pygame.font.SysFont("Arial", 13)
    pygame.draw.rect(screen, "#160521", shufRect)
    if shuffle == 0:
        screen.blit(font.render("Loop All", True, "white"), (20, 430))

    elif shuffle == 1:
        screen.blit(font.render("Loop Once", True, "white"), (20, 430))

    else:
        screen.blit(font.render("Shuffle", True, "white"), (20, 430))

       
def playNextFunc(queueVal):
    #for the queue to reset
    global playNext
    playNext = 0
    try:
        mixer.music.load(filepaths[queueVal])
        mixer.music.play()
        #display the music playing
        #put a rectangle under 
        pygame.draw.rect(screen, "#160521", (0, 480, 700, 20))
        font = pygame.font.SysFont("Arial", 12)
        screen.blit(font.render(f"Now playing: {names[queueVal]}", True, "white"), (5, 480))
        
    except pygame.error:
        chooseMusic(2)
    except IndexError:
        musicChoosed = 0
    pause()

    
def nextt():
    #10s
    pygame.draw.polygon(screen, "white", ((400, 430), (420, 440), (420, 430), (440, 440), (420, 450), (420, 440), (400, 450)))
    pygame.draw.polygon(screen, "white", ((260, 440), (280, 430), (280, 440), (300, 430), (300, 450), (280, 440), (280, 450)))

    #next
    pygame.draw.polygon(screen, "white", ((460, 430), (480, 440), (480, 430), (485, 430), (485, 450), (480, 450), (480, 440), (460, 450)))
    pygame.draw.polygon(screen, "white", ((215, 430), (220, 430), (220, 440), (240, 430), (240, 450), (220, 440), (220, 450), (215, 450)))

    volumeBar(volumeVal)
    font = pygame.font.SysFont("Arial", 10)
    screen.blit(font.render("Volume", True, "white"), (625, 445))
    togShuffle()
    


def pause():
    #put a rectangle under first
    pygame.draw.rect(screen, "#160521", (0, 400, 700, 80))

    pygame.draw.circle(screen, "white", (350, 445), 30, 2)
    pygame.draw.rect(screen, "white", (335, 430, 10, 30))
    pygame.draw.rect(screen, "white", (355, 430, 10, 30))
    mixer.music.unpause()
    nextt()
    pygame.display.update()

def playy():
    #put a rectangle under first
    pygame.draw.rect(screen, "#160521", (0, 400, 700, 80))
    
    pygame.draw.circle(screen, "white", (350, 445), 30, 2)
    pygame.draw.polygon(screen, "white", ((340, 430), (370, 450), (340, 460)))
    mixer.music.pause()
    nextt()
    pygame.display.update()




j = 40

for path, _, files in os.walk("C:/Users/"+ os.getlogin() +"/Music"):
    for file in files:
        if music in file:
            #if rec not in path and "Music" in path:
            filepath = os.path.join(path, file)
            filepaths.append(filepath)
            name = file.replace(".mp3", "")
            names.append(name)
            recc.append(pygame.Rect(0, j, 629, 35))
            queueRecc.append(pygame.Rect(630, j, 100, 35))
            if j >= 355:
                j = 40
            else:
                j = j + 35
            
for v in range(0, 80, 8):
    volumeVals.append(pygame.Rect(600+v, 440, 8, 3))

nextPage = pygame.Rect(651, 0, 50, 40)
prevPage = pygame.Rect(0, 0, 50, 40)
searchRect = pygame.Rect(559, 0, 90, 40)
shufRect =  pygame.Rect(20, 430, 60, 20)
#create end event for when music ends so you can play another
MUSIC_END = 44
pygame.mixer.music.set_endevent(MUSIC_END)
chooseMusic(3)
displayy()



while running:
    #pygame quit means clicking the X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == MUSIC_END:
            if playNext == 1:
                playNextFunc(queueVal)
            else:
                if shuffle == 0:
                    #loop all
                    chooseMusic(2)
                
                elif shuffle == 1:
                    #loop one
                    chooseMusic(3)
                   
                else:
                    #shuffle
                    chooseMusic(1)

        # checking if keydown event happened or not
        if searchCount == 1:
            if event.type == pygame.KEYDOWN:
                
                # checking if key "backspace" was pressed
                #if it was pressed remove the last alphabet
                if event.key == pygame.K_BACKSPACE:
                   searched = searched[:-1]

                #if enter then search the letters
                elif event.key == pygame.K_RETURN:
                    searchPage()
                    
                #if alphabet or numbers update the searched variable
                else:
                    searched += event.unicode
                    #print(searched)
                searchPage()
                
      
        if event.type == pygame.MOUSEBUTTONDOWN:
            #to make the circle clickable
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]

            sqx = (x - 350)**2
            sqy = (y - 445)**2

            #making the area around 30 clickable
            if math.sqrt(sqx + sqy) < 30:
                if counter == 0:
                    counter = 1
                    pause()
                    #print(counter)
                else:
                    counter = 0
                    playy()
                    #print(counter)
            
            #nextt10
            sqxnn = (x - 420)**2
            sqynn = (y - 440)**2

            if math.sqrt(sqxnn + sqynn) < 20:
                fastForward(1)

            #prev10
            sqxpp = (x - 280)**2
            sqypp = (y - 440)**2

            if math.sqrt(sqxpp + sqypp) < 20:
                fastForward(2)

            #nextt
            sqxn = (x - 475)**2
            sqyn = (y - 440)**2

            if math.sqrt(sqxn + sqyn) < 15:
                #nextAction()
                #in case there is a queued music
                if playNext == 1:
                    playNextFunc(queueVal)
                else:
                    chooseMusic(2)

            #prev
            sqxp = (x - 225)**2
            sqyp = (y - 440)**2

            if math.sqrt(sqxp + sqyp) < 15:
                #prevAction()
                chooseMusic(1)
                

            #print(i)
            
            next1 = nextPage.collidepoint(pygame.mouse.get_pos())
            if next1 == 1:
                getMusic(1)
                
            prev1 = prevPage.collidepoint(pygame.mouse.get_pos())
            if prev1 == 1:
                getMusic(2)

            searchPos = searchRect.collidepoint(pygame.mouse.get_pos())
            if searchPos == 1:
                searchPage()

            shuff = shufRect.collidepoint(pygame.mouse.get_pos())
            if shuff == 1:
                shuffle =  shuffle + 1
                if shuffle > 2:
                    shuffle = 0
                togShuffle()

            for v in range(len(volumeVals)):
                vol = volumeVals[v].collidepoint(pygame.mouse.get_pos())
                if vol == 1:
                    volumeVal = v / 10
                    volumeBar(volumeVal)
                    #print(volumeVal)

            #for play next
            for p in range(i-10, i):
                pn = queueRecc[p].collidepoint(pygame.mouse.get_pos())
                if pn == 1:
                    queueVal = p
                    playNext = 1

            #for clicking music        
            for f in range(i-10, i):
                click = recc[f].collidepoint(pygame.mouse.get_pos())
                if click == 1:
                    musicChoosed = f
                    chooseMusic(3)
            
            if searchCount == 1:
                for s in range(len(searchRecc)):
                    sre = searchRecc[s].collidepoint(pygame.mouse.get_pos())
                    if sre == 1:
                        searchClick = searchResult[s]
                        musicChoosed = searchClick
                        chooseMusic(3)
                    
                
    pygame.display.update()
   

pygame.quit()

#useful or not useful things
"""
#keyboardKeys = {pygame.K_a:"a", pygame.K_b:"b", pygame.K_c:"c", pygame.K_d:"d", pygame.K_e:"e", pygame.K_f:'f', pygame.K_g:'g', pygame.K_h:'h', pygame.K_i:'i', pygame.K_j:'j', pygame.K_k:'k', pygame.K_l:'l', pygame.K_m:'m', pygame.K_n:'n', pygame.K_o:'o', pygame.K_p:'p', pygame.K_q:'q', pygame.K_r:'r', pygame.K_s:'s', pygame.K_t:'t', pygame.K_:'u', pygame.K_v:'v', pygame.K_x:'x', pygame.K_y:'y', pygame.K_z:'z'}
j = 40       
names = sorted(firstNames)
filepaths = sorted(firstFiles)

for r in range(len(filepaths)):
    recc.append(pygame.Rect(0, j, 700, 35))
    if j >= 355:
        j = 40
    else:
        j = j + 35
def getMusic1():
    global i
    new_surface = pygame.Surface((700, 350))
    new_surface.fill("#160521")
    pygame.draw.rect(new_surface, "grey", nextPage)

    pygame.draw.line(new_surface, "#160521", (665, 150), (685, 175), 2)
    pygame.draw.line(new_surface, "#160521", (685, 175), (665, 200), 2)


    for j in range(10):
        font = pygame.font.SysFont("Arial", 15)
        #draw d rectangles
        recc.append(pygame.Rect(0, j*35, 650, 35))
        pygame.draw.rect(new_surface, "white", recc[i], 1)
        new_surface.blit(font.render(names[i], True, "white"), (5, (j*35)+10))
        i = i + 1
        j = j + 1


                    
    screen.blit(new_surface, (0, 40))
    #return i
"""


