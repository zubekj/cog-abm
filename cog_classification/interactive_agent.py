import sys
sys.path.append('../../')
sys.path.append('../')
sys.path.append('')

from cog_classification.steels_classifier.steels_classification_agent import SteelsClassificationAgent as Agent
from cog_classification.core.environment import Environment
from cog_classification.run import load_dataset

from sklearn import tree


agent = Agent(classifier=tree.DecisionTreeClassifier(), alpha=0.99)
samples, classes = load_dataset('../data/classification_data/glass.data')
print samples, classes
env = Environment(samples, classes)


i = 4
while i:
    if i == 1:
        sample, category = input("sample, category\n")
        agent.add_sample(sample, env, category)
    elif i == 2:
        sample = input("sample\n")
        print(agent.classify(env.get_sample(sample)))
    elif i == 3:
        sample, category = input("sample, category\n")
        agent.increase_weights_sample_category(sample, env, category=category)
    elif i == 4:
        agent.forget()

    print("Categories: %s" % agent.sample_storage.categories)

    i = input("""
1 - Add sample.
2 - Classify.
3 - Good sample for category.
4 - Forget.
""")
