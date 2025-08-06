class ProgressionLimits:
    def __init__(self, player, faith_pass=None):
        self.player = player
        self.faith_pass = faith_pass
        self.daily_mission_limit = 5
        self.missions_completed_today = 0
        self.last_reset = None

    def can_start_mission(self):
        limit = self.daily_mission_limit
        if self.faith_pass and self.faith_pass.is_active():
            limit += 3 + self.faith_pass.extra_slots
        return self.missions_completed_today < limit

    def complete_mission(self):
        self.missions_completed_today += 1

    def reset_daily(self):
        self.missions_completed_today = 0
        if self.faith_pass:
            self.faith_pass.reset_daily()
