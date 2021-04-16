from copy import deepcopy
from PIL import Image, ImageDraw, ImageChops, ImageFont
import random
import time


# As a fitness function, I use the root mean square error (MSE) between the current image and the original image.
# About the MSE technique I read in the article, which is listed in the reference list.

# The argument to the function is the current image (image), which is compared with the original image (chromosome).
# Functions return difference between images as int value


def fitness_function(image):
    square_error = ImageChops.difference(image, chromosome)
    histogram = square_error.histogram()
    squares = (val * ((index % 256) ** 2) for index, val in enumerate(histogram))
    squares_sum = sum(squares)
    answer = squares_sum / float(512 * 512)
    return int(answer)


# In the mutation stage  I change the chromosome by putting a text, which is my name, on the image.

# The function mutation takes an image as an argument, randomly generates colours for the font,
# the size of the font is fixed ( size=7 )
def mutation(image):
    text = "Dariya"
    size = 7
    font = ImageFont.truetype("Inkfree.ttf", size)
    canva = ImageDraw.Draw(image)

    for l in range(0, 30):
        x = random.randint(0, 511)
        y = random.randint(0, 511)
        color = chromosome.getpixel((x, y))
        canva.text((x, y), text, color, font)

    return image


# Function crossover takes two images as an argument and generates a third image by taking 60 % of the first image and
# 40 % of the second image. A new image then added to the population.
# Function crossover responsible for increasing the number of entities in the population.
def crossover(image1, image2):
    chromosome3 = Image.blend(image1, image2, 0.6)
    population.append(chromosome3)


# The selection function selects the best image from the population.
# It takes 2 arguments as input: generation - number of evolutions and fitness - minimal error between two images,
# further will be used to select best images
def selection(generation, fitness):
    while generation <= 150:
        generation += 1
        for m in range(len(population) // 2):
            k = random.randint(0, len(population) - 1)
            mutation(population[k])

        for m in range(len(population) // 4):
            k1 = random.randint(0, len(population) - 1)
            k2 = random.randint(0, len(population) - 1)
            crossover(population[k1], population[k2])

        for m in range(len(population) // 2 - generation):
            if fitness_function(population[m]) < fitness:
                population.remove(population[m])
        fitness *= 1000
        print("Iteration ", generation)

    max_fit = 0
    answer = [chromosome]
    for m in range(len(population)):
        if fitness_function(population[m]) > max_fit:
            max_fit = fitness_function(population[m])
            answer.clear()
            answer.append(population[m])
    return answer[0]


start = time.time()  # for measuring time
input_im = 'head.jpg'
output_im = 'output_h.png'
image = Image.open(input_im).convert('RGBA')
chromosome = image.resize((512, 512))  # in case if image not 512*512
population_size = 5  # size of initial population
population = list()
image = Image.new('RGBA', (512, 512), (255, 255, 255, 255))  # white image
for i in range(population_size):
    population.append(deepcopy(image))
generation = 0
min_fit = 100
selection(generation, min_fit).save(output_im)
end = time.time() - start
print('time in min  is', end // 60)
