import pygame
from random import randint
import math
from sklearn.cluster import KMeans

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("K-Means visualizer")

running = True

clock = pygame.time.Clock()
background = (214,214,214)
black = (0,0,0)
background_panel =(249,255,230)
White = (255,255,255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147,153,35)
PURPLE = (255,0,255)
SKYBLUE = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKYBLUE,ORANGE,GRAPE,GRASS]

font = pygame.font.SysFont("sans",40)
font_small = pygame.font.SysFont("sans",20)
text_plust = font.render("+",True,White)
text_minus = font.render("-",True,White)
text_run = font.render("Run",True,White)
text_random = font.render("Random",True,White)
text_algorithm = font.render("Algorithm",True,White)
text_Reset = font.render("Reset",True,White)

K = 0
error = 0
points = []
clusters = []
labels = []

while running:
    clock.tick(60)
    screen.fill(background)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    #draw interface
    # Draw panel

    pygame.draw.rect(screen,black,(50,50,700,500))
    pygame.draw.rect(screen,background_panel,(55,55,690,490))

    #Draw K button +
    pygame.draw.rect(screen,black,(850,50,50,50))
    screen.blit(text_plust, (860,50))

    #Draw K button -
    pygame.draw.rect(screen,black,(950,50,50,50))
    screen.blit(text_minus, (960,50))

    #Draw K value 
    text_k = font.render("K = "+str(K),True,black)
    screen.blit(text_k, (1050,50))

    #Draw run button
    pygame.draw.rect(screen,black,(850,150,150,50))
    screen.blit(text_run, (900,150))

    #Draw random button
    pygame.draw.rect(screen,black,(850,250,150,50))
    screen.blit(text_random, (850,250))

    #Draw reset button
    pygame.draw.rect(screen,black,(850,550,150,50))
    screen.blit(text_Reset, (850,550))

    #Draw algorithm button
    pygame.draw.rect(screen,black,(850,450,150,50))
    screen.blit(text_algorithm, (850,450))


    #Draw mouse position when mouse is in panel
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = font_small.render("("+str(mouse_x-50)+","+str(mouse_y-50)+")",True,black)
        screen.blit(text_mouse, (mouse_x+5,mouse_y))

    #End draw interface

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #create point
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point = [mouse_x-50,mouse_y-50]
                points.append(point)
               



            #Change K button +
            if 850 < mouse_x <900 and 50 < mouse_y < 100:
                if K < 8:
                    K = K+1
                
            #Change K button -
            if 950 < mouse_x <1000 and 50 < mouse_y < 100:
                if K > 0:
                    K = K-1
                print("K-")

            #Run button
            if 850 < mouse_x <1000 and 150 < mouse_y < 200:
                labels = []
                if clusters == []:
                    continue

                #Assign points to closest clusters
                for p in points:
                    distances_to_clusters = [] 
                    for c in clusters:
                        dis=distance(p,c)
                        distances_to_clusters.append(dis)

                    min_distance = min(distances_to_clusters)
                    label = distances_to_clusters.index(min_distance)
                    labels.append(label)

                #Update clusters
                for i in range(K):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x = sum_x + points[j][0]
                            sum_y = sum_y + points[j][1]
                            count = count + 1
                    if count > 0:
                        new_cluster_x = sum_x/count
                        new_cluster_y = sum_y/count
                        clusters[i] = [new_cluster_x,new_cluster_y] 
                    
            
            #Random button
            if 850 < mouse_x <1000 and 250 < mouse_y < 300:
                labels = []
                clusters = []
                for i in range(K):
                    random_point = [randint(0,700),randint(0,500)]
                    clusters.append(random_point)

            #Reset button
            if 850 < mouse_x <1000 and 550 < mouse_y < 600:
                points = []
                clusters = []
                labels = []
                error = 0

            #Algorithm button
            if 850 < mouse_x <1000 and 450 < mouse_y < 500:
                kmeans = KMeans(n_clusters = K).fit(points)
                clusters = kmeans.cluster_centers_
                labels = kmeans.predict(points)
                
      
    #draw points
    for i in range(len(points)):
        pygame.draw.circle(screen,black,(points[i][0]+50,points[i][1]+50),6)

        if labels == []:
            pygame.draw.circle(screen,White,(points[i][0]+50,points[i][1]+50),5)
        else:
            pygame.draw.circle(screen,COLORS[labels[i]],(points[i][0]+50,points[i][1]+50),5)

    #draw clusters
    for i in range(len(clusters)):
        pygame.draw.circle(screen,COLORS[i],(int(clusters[i][0]+50),int(clusters[i][1]+50)),10)

    #Calculate error
    error = 0
    if clusters !=[] and labels != []:
        for i in range(len(points)):
            error += distance(points[i],clusters[labels[i]])

    text_error = font.render("Error="+ str(int(error)),True,black)
    screen.blit(text_error, (850,350))

    
    pygame.display.flip()

pygame.quit()