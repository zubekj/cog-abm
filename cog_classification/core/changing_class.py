class ChangingClass:
    """ This class implements behavior changing in time. """

    def __init__(self, behaviors, changes):
        """
        Args:
            behaviors (dictionary): dictionary with name of behavior as a key and behavior as a value.
            changes (dictionary): dictionary with time of change (number) as a key and name of behavior on which the
                current behavior will be changed when name of this change will be given in change.
        """
        self.behaviors = behaviors
        self.changes = changes

        self.current_behavior = None
        # To initialize current behavior change should be used.

    def change(self, change_time):
        """
        Changes current behavior on behavior associated with change time.

        If there is no such change, method leaves the old value of current behavior.
        """

        if change_time in self.changes:
            self.current_behavior = self.behaviors[self.changes[change_time]]

    def update(self, changing_class, time):
        """
        Adds behaviors and changes moved by time from changing class to self.

        Args:
            changing_class (ChangingClass): instance whose content is added to self.
            time (number): how much should be changes form changing class moved forward.
        """
        self.behaviors.update(changing_class.get_behaviors())

        for change, behavior in changing_class.get_changes().iteritems():
            self.changes[change + time] = behavior

    def get_behaviors(self):
        return self.behaviors

    def get_changes(self):
        return self.behaviors

    def get_current_behavior(self):
        return self.current_behavior
