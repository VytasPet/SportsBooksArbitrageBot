from fuzzywuzzy import fuzz
import difflib

class Compare:
    def __init__(self, site1, site2, site3):
        self.site1 = site1
        self.site2 = site2
        self.site3 = site3

    # Define a function to check if two team names match with tolerance
    def team_names_match_with_tolerance(self, team_name1, team_name2, tolerance=0.5):
        # Use difflib's SequenceMatcher to calculate similarity
        similarity = difflib.SequenceMatcher(None, team_name1, team_name2).ratio()
        return similarity >= tolerance

    def find_matched_matches(self):
        # Create a list to store the matched matches
        matched_matches = []

        # Iterate through matches from site1
        for match1 in self.site1:
            # Extract team names from the first site's match
            team_one_1 = match1['team_one']
            team_two_1 = match1['team_two']
            break_loop_one = False

            # Iterate through matches from site2
            for match2 in self.site2:
                # Extract team names from the second site's match
                team_one_2 = match2['team_one']
                team_two_2 = match2['team_two']
                break_loop = False

                # Check if team names match with tolerance for Site 1 and Site 2
                if (self.team_names_match_with_tolerance(team_one_1, team_one_2) and
                        self.team_names_match_with_tolerance(team_two_1, team_two_2)):

                    # Iterate through matches from site3
                    for match3 in self.site3:
                        # Extract team names from the third site's match
                        team_one_3 = match3['team_one']
                        team_two_3 = match3['team_two']

                        # Check if team names match with tolerance for Site 2 and Site 3
                        if (self.team_names_match_with_tolerance(team_one_2, team_one_3) and
                                self.team_names_match_with_tolerance(team_two_2, team_two_3)):
                            # If all three sites have matches, add it to the matched_matches list
                            matched_matches.append((match1, match2, match3))
                            break_loop = True
                            break

                        elif (self.team_names_match_with_tolerance(team_one_1, team_one_3) and
                              self.team_names_match_with_tolerance(team_two_1, team_two_3)):
                            # If all three sites have matches, add it to the matched_matches list
                            matched_matches.append((match1, match2, match3))
                            break_loop = True
                            break
                    if break_loop:
                        break


                    matched_matches.append((match1, match2))


                else:
                    # Iterate through matches from site3
                    for match3 in self.site3:
                        # Extract team names from the third site's match
                        team_one_3 = match3['team_one']
                        team_two_3 = match3['team_two']

                        # Check if team names match with tolerance for Site 2 and Site 3
                        if (self.team_names_match_with_tolerance(team_one_1, team_one_3) and
                                self.team_names_match_with_tolerance(team_two_1, team_two_3)):
                            matched_matches.append((match1, match3))
                            break

                        elif (self.team_names_match_with_tolerance(team_one_2, team_one_3) and
                              self.team_names_match_with_tolerance(team_two_2, team_two_3)):
                            matched_matches.append((match2, match3))
                            break

        return matched_matches
