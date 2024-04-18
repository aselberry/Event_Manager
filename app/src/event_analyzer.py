class EventAnalyzer:
    def get_joiners_multiple_meetings_method(self, events):
        joiner_meetings_count = {}
        for event in events:
            for joiner in event.joiners:
                if joiner in joiner_meetings_count:
                    joiner_meetings_count[joiner] += 1
                else:
                    joiner_meetings_count[joiner] = 1

        joiners_multiple_meetings = [joiner for joiner, count in joiner_meetings_count.items() if count >= 2]
        
        if joiners_multiple_meetings:
            return joiners_multiple_meetings
        else:
            return ["No joiners attending at least 2 meetings"]

