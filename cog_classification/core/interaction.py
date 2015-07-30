from cog_classification.core.changing_class import ChangingClass


class Interaction(ChangingClass):

    def interact(self, agents, environment):
        return self.current_behavior.interact(agents, environment)
