# this script helps to provide specific simulation file. The second iteration was added to measure CS and DS, where all agents meet together, but they still learn in fixed network. Content of the new file should be added to simulation file
interactions = ""

for i in range(5000):
    # interactions=""
    s = """
        {
        "id" : 1,
        "type" : "GuessingGame",
        "start" : %s,
        "context_size" : 4,
        "learning" : true,
        "inc_category_threshold" : 0.95
        },
        """ % (2 * i + 1)
    s2 = """
        {
        "id" : 2,
        "type" : "GuessingGame",
        "start" : %s,
        "game_name" : "CL",
        "context_size" : 4,
        "learning" : false,
        "inc_category_threshold" : 0.95
                },
        """ % (2 * i + 2)
    interactions = interactions + s + s2
f = open('interactions.txt', 'w')
f.write(interactions)
f