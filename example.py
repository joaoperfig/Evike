import random
import math

def creator():
    return random.random()

def fitness(member):
    return member

def mate(member1, member2):
    m1w = random.random()
    m2w = random.random()
    total = m1w + m2w
    return ((member1*m1w)+(member2*m2w))/total

def mutate(member):
    return member * (1+((random.random()-0.5)*0.1))
