class BehaviorSwitcher:
    """
    This class implements behavior changing in time.

    :param dictionary behaviors: dictionary with time of change (long) as a key and behavior as a value. \
        Behavior switcher will be using new behavior from it's time of change.

    :raise: **ValueError** - if behaviors is None.
    """

    def __init__(self, behaviors):
        if behaviors is not None:
            if isinstance(behaviors, dict):
                self.behaviors = behaviors
            else:
                self.behaviors = {1: behaviors}
        else:
            raise ValueError
        self.current_behavior = None
        # To initialize current behavior change should be used.

    def change(self, change_time):
        """
        Changes current behavior on behavior associated with change time.

        :param long change_time: The current time that can change behavior.

        If there is no new behavior associated with change time, method leaves the old value of current behavior.
        """

        if change_time in self.behaviors:
            self.current_behavior = self.behaviors[change_time]

    def update(self, changing_class, time):
        """
        Adds behaviors moved by time from changing class to self.

        :param BehaviorSwitcher changing_class: instance whose content is added to self.
        :param long time: how much should be behaviors form changing class moved forward.
        """
        for change, behavior in changing_class.behaviors.iteritems():
            self.behaviors[change + time] = behavior
