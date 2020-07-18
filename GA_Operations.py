
import copy
import random


import functions as func

class Operations:

    ### Parent Selection Methods ###
    def PS_RW(self, PS_settings, population):

        # Sum of fitness
        pass


    def PS_TO(self, PS_settings, population):

        parents = []

        #   This temp population is to not affect the original one
        temp_population = copy.deepcopy(population)

        #   Tournament Selection
        for parent_count in range(PS_settings["quantity_of_parents"]):

            # Choose parents for tournament
            choices = random.sample(temp_population, k=PS_settings["TO_K"])

            # Parent with highest fitness - add to parent list
            fittest_parent = eval("func.find_PS_" + PS_settings["problem_type"] + "(choices)")
            parents.append(fittest_parent)

            # Find fittest parent in population and delete
            temp_population.remove(fittest_parent)


        return parents



    ### Crossover Methods ###
    def CR_OP(self , CR_settings, parents):

        crossover = []
        chromosome_len = len(parents[0].chromosome)
        temp_parents = copy.deepcopy(parents)

        while len(temp_parents) >= 2:

            # Pick two random parents - .sample does not gert repeating values
            choices = random.sample(temp_parents, k=2)

            # Choose random number between 0 - 1 ... Mutation Rate
            if random.uniform(0, 1) > CR_settings["rate"]:

                # Pick a random part between chomosome
                split = random.randint(1, chromosome_len-1)

                # Swap parts from chosen part
                offspring = func.mutation_swap(choices, split, None)

                # # Update fitness and ID
                # for child in offspring:
                #
                #     print(child.id)
                #     child = func.new_id(temp_parents + crossover)
                #     print(child.id)
                #
                #     print(child.fitness)
                #     child.update_fitness()
                #     print(child.fitness)
                #
                # exit()

                # Save offspring
                for person in offspring:
                    crossover.append(person)

            else:
                # If didnt go through mutation process then add parents to next list
                for person in choices:
                    crossover.append(person)

            # Remove from temp_parent
            for person in choices:
                temp_parents.remove(person)

        # If there are any remaining parents in the parent list then add reagrdless to crossover
        for person in temp_parents:

            crossover.append(person)

        func.print_population_section("parents", parents)
        func.print_population_section("after mutation", crossover)

        return crossover


    def CR_TP(self):
        print("TP", CR_settings)



    ### Mutation Methods ###
    def MU_BF(self, MU_settings, crossover):

        mutation = []
        chromosome_len = len(crossover[0].chromosome)
        temp_crossover = copy.deepcopy(crossover)

        for person in temp_crossover:

            func.print_divisor()

            func.print_individual(person, "\nBefore mutation:")

            # Mutation Rate
            if random.uniform(0, 1) > MU_settings["rate"]:

                # choose an index to flip value
                bit_flip_index = random.randint(0, chromosome_len-1)

                print(f"Index to flip: {bit_flip_index}")

                # Flip the value
                if person.chromosome[bit_flip_index] is 0:
                    person.chromosome[bit_flip_index] = 1
                else:
                    person.chromosome[bit_flip_index]= 0

                mutation.append(person)

                func.print_individual(person, "\nAfter mutation:")

            else:
                print("Not going through mutation")
                mutation.append(person)

        func.print_population_section("crossover", crossover)
        func.print_population_section("mutation", mutation)

        return mutation

    def MU_SW(self, MU_settings):
        print(SW)



    ### Survivor Selection Methods ###
    def SS_FB(self, SS_settings, mutation, population):

        func.print_population_section("Updated Mutation Fitness", mutation)

        temp_mutation = copy.deepcopy(mutation)


        if SS_settings["problem_type"] == "maximum":

            # Sort old and new populations
            population.sort(key=lambda x: x.fitness, reverse=False) # lowest at start of list
            temp_mutation.sort(key=lambda x: x.fitness, reverse=True) # highest fitness at start of list

            # Replace x of old with new offspring
            for count in range(SS_settings["FB_suvivor_quantity"]):
                population[count] = copy.deepcopy(temp_mutation[count])

        elif SS_settings["problem_type"] == "minimum":

            # Sort old and new populations
            population.sort(key=lambda x: x.fitness, reverse=True)  # highest at start of list
            temp_mutation.sort(key=lambda x: x.fitness, reverse=False)  # lowest fitness at start of list

            # Replace x of old with new offspring
            for count in range(SS_settings["FB_suvivor_quantity"]):
                population[count] = copy.deepcopy(temp_mutation[count])

        else:
            print("Something wrong in the SS function")


        return population



