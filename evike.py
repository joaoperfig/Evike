import example
import random

def initial_generation(creator, quantity):
    pop = []
    for i in range(quantity):
        pop += [creator()]
    return pop

def fitnesses(generation, fitness_getter):
    fitnesses = []
    for member in generation:
        fitnesses += [fitness_getter(member)]
    return fitnesses

def create_mating_pool(generation, fitnesses, quantity, mode):
        
    if mode == "top":
        selectids = []
        result = []
        while len(result) < quantity:
            bestm = None
            besti = 0
            bestf = 9999999999           
            for i, member in enumerate(generation):
                f = fitnesses[i]
                if f <= bestf and not i in selectids:
                    bestf = f
                    bestm = member
                    besti = i
            result += [bestm]
            selectids += [besti]
        return result
    
    elif mode == "roulette":
        result = []
        invert = []
        for f in fitnesses:
            invert += [1/f]
        totalf = sum(invert)
        while len(result) < quantity:        
            selected = random.random() * totalf
            counter = 0
            for i, inv in enumerate(invert):
                if inv + counter >= selected:
                    result += [generation[i]]
                    break
                else:
                    counter += inv
        return result
    
    elif mode == "tournament":
        result = []
        while len(result) < quantity:   
            i1, f1 = random.choice(list(enumerate(fitnesses)))
            i2, f2 = random.choice(list(enumerate(fitnesses)))
            if f1 < f2:
                result += [generation[i1]]
            else:
                result += [generation[i2]]
        return result
    
    else:
        raise ValueError("No such selection mode")
    
def mate(mating_pool, quantity, mating_method):
    result = []
    while len(result) <= quantity:
        newmember = mating_method(random.choice(mating_pool), random.choice(mating_pool))
        result += [newmember]
    return result

def mutate(generation, mutate_method):
    result = []
    for member in generation:
        result += [mutate_method(member)]
    return result

def do_full_next_generation(generation, fitness_getter, mating_size, mating_mode, mating_method, mutate_method):
    fit = fitnesses(generation, fitness_getter)
    mp = create_mating_pool(generation, fit, mating_size, mating_mode)
    nex = mate(mp, len(generation), mating_method)
    nex = mutate(nex, mutate_method)
    return (max(fit), min(fit), nex)

def do_everything(duration, members, creator_method, fitness_getter, mating_size, mating_mode, mating_method, mutate_method):
    generation = initial_generation(creator_method, members)
    for i in range(duration):
        worst, best, generation = do_full_next_generation(generation, fitness_getter, mating_size, mating_mode, mating_method, mutate_method)
        print(best)