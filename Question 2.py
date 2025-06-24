class UDGraph:

    # dictionary to store the graph
    def __init__(self):
        self.graph = dict()

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, start, end):
        if start in self.graph and end in self.graph:
            self.graph[start].append(end)
        else:
            print("One or both vertices not found.")

    def list_outgoing_adjacent_vertex(self, vertex):
        if vertex in self.graph:
            return self.graph.get(vertex)
        else:
            print(f"Vertex {vertex} not found in graph.")
            return []

    def remove_edge(self, start, end):
        if start in self.graph and end in self.graph:
            if end in self.graph[start]:
                self.graph[start].remove(end)
            else:
                print(f"No edge exists from {start} to {end}.")
        else:
            print("One or both vertices not found.")

    def get_vertices(self):
        return list(self.graph.keys())


class Person:
    def __init__(self, name, gender, biography, privacy):
        self.name = name
        self.gender = gender
        self.biography = biography
        self.privacy = privacy  # "P" for private, "U" for public

    def get_name(self):
        return self.name

    def get_privacy(self):
        return self.privacy

    def get_biography(self):
        return self.biography

    def get_gender(self):
        return self.gender

    def __str__(self):
        return self.name


class SlowGram:
    def __init__(self):
        # Initialize the graph to store the social network
        self.my_graph = UDGraph()

    def add_new_profile(self, name, gender, biography, privacy):
        person = Person(name, gender, biography, privacy)
        self.my_graph.add_vertex(person)
        return person

    def add_follow(self, follower, followee):
        self.my_graph.add_edge(follower, followee)

    def unfollow(self, follower, followee):
        self.my_graph.remove_edge(follower, followee)

    def get_all_profiles(self):
        return self.my_graph.get_vertices()

    def get_followers(self, person):
        followers = []
        for profile in self.get_all_profiles():
            if person in self.my_graph.list_outgoing_adjacent_vertex(profile):
                followers.append(profile)
        return followers

    def get_following(self, person):
        return self.my_graph.list_outgoing_adjacent_vertex(person)


def display_menu():
    """Display the main menu of the application"""
    print("*" * 45)
    print("Welcome to Slow Gram, Your Social Media App:")
    print("*" * 45)
    print("1. View names of all profiles")
    print("2. View details for any profile")
    print("3. View followers of any profile")
    print("4. View followed accounts of any profile")
    print("5. Add a new profile")
    print("6. Follow a user")
    print("7. Unfollow a user")
    print("8. Quit")
    print("*" * 45)


# display the current list of profiles saved
def display_profiles(profiles):
    for i, person in enumerate(profiles, 1):
        print(f"{i}. {person.get_name()}")


def main():
    # Initialize the application
    gram = SlowGram()

    # Create sample profiles
    karen = gram.add_new_profile("Karen", "Female", "Just an ordinary woman", "P")
    susy = gram.add_new_profile("Susy", "Female", "Just a normal person","U")
    brian = gram.add_new_profile("Brian", "Male", "Just an ordinary teenager", "U")
    calvin = gram.add_new_profile("Calvin", "Male", "Just an ordinary man", "P")
    elon = gram.add_new_profile("Elon", "Male", "Just a hardworking man","U")

    # Set up some follow relationships
    gram.add_follow(karen, susy)
    gram.add_follow(karen, brian)
    gram.add_follow(karen, elon)
    gram.add_follow(elon, karen)
    gram.add_follow(elon, calvin)
    gram.add_follow(brian, karen)
    gram.add_follow(brian, susy)

    # Main program loop
    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice (1 - 8): "))

            if choice == 1:
                # View all profile names
                print("=" * 40)
                print("View All Profile Names:")
                print("=" * 40)
                profiles = gram.get_all_profiles()
                display_profiles(profiles)
                print("=" * 40)

            elif choice == 2:
                # View details for any profile
                print("=" * 40)
                print("View Details For Any Profile:")
                print("=" * 40)
                profiles = gram.get_all_profiles()
                display_profiles(profiles)
                try:
                    profile_choice = int(input(f"Select whose profile to view (1 - {len(profiles)}): "))
                    if 1 <= profile_choice <= len(profiles):
                        person = profiles[profile_choice - 1]
                        print(f"Name: {person.get_name()}")

                        # Check privacy settings
                        if person.get_privacy() == "P":
                            print(f"{person.get_name()} has a private profile.")
                        else:
                            print(f"Gender: {person.get_gender()}")
                            print(f"Biography: {person.get_biography()}")
                    else:
                        print("Invalid profile selection.")
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == 3:
                # View followers for any profile
                print("=" * 40)
                print("View Followers For Any Profile")
                print("=" * 40)
                profiles = gram.get_all_profiles()
                display_profiles(profiles)
                try:
                    profile_choice = int(input(f"Select whose profile to view followers (1 - {len(profiles)}): "))
                    if 1 <= profile_choice <= len(profiles):
                        person = profiles[profile_choice - 1]
                        followers = gram.get_followers(person)
                        print(f"Follower List:")
                        for follower in followers:
                            print(f"- {follower.get_name()}")
                    else:
                        print("Invalid profile selection.")
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == 4:
                # View followed accounts for any profile
                print("=" * 40)
                print("View Followed Accounts for Any Profile:")
                print("=" * 40)
                profiles = gram.get_all_profiles()
                display_profiles(profiles)
                try:
                    profile_choice = int(input(f"Select whose profile to view followings (1 - {len(profiles)}): "))
                    if 1 <= profile_choice <= len(profiles):
                        person = profiles[profile_choice - 1]
                        following = gram.get_following(person)
                        print(f"Following List:")
                        for followed_person in following:
                            print(f"- {followed_person.get_name()}")
                    else:
                        print("Invalid profile selection.")
                except ValueError:
                    print("Please enter a valid number.")

            elif choice == 5:
                # add new user on demand
                print("=" * 40)
                print("Add a New Profile:")
                print("=" * 40)
                name = input("Enter name: ")
                gender = input("Enter gender: ")
                biography = input("Enter biography: ")
                privacy = input("Enter privacy setting (P for private, U for public): ").upper()
                if privacy not in ['P', 'U']:
                    privacy = 'U'  # Default to public if invalid input
                gram.add_new_profile(name, gender, biography, privacy)
                print(f"Profile for {name} created successfully!")

            elif choice == 6:
                # Follow a user
                print("=" * 40)
                print("Follow a User:")
                print("=" * 40)
                profiles = gram.get_all_profiles()
                print("Select a user who will follow:")
                display_profiles(profiles)
                try:
                    follower_choice = int(input(f"Select follower (1 - {len(profiles)}): "))
                    print("Select a user to be followed:")
                    display_profiles(profiles)
                    followee_choice = int(input(f"Select followee (1 - {len(profiles)}): "))

                    if (1 <= follower_choice <= len(profiles) and
                            1 <= followee_choice <= len(profiles) and
                            follower_choice != followee_choice):

                        follower = profiles[follower_choice - 1]
                        followee = profiles[followee_choice - 1]
                        gram.add_follow(follower, followee)
                        print(f"{follower.get_name()} is now following {followee.get_name()}")
                    else:
                        print("Invalid selection or tried to follow yourself.")
                except ValueError:
                    print("Please enter valid numbers.")

            elif choice == 7:
                # Unfollow a user (advanced feature)
                print("=" * 40)
                print("Unfollow a User:")
                print("=" * 40)
                profiles = gram.get_all_profiles()
                print("Select a user who will unfollow:")
                display_profiles(profiles)
                try:
                    follower_choice = int(input(f"Select follower (1 - {len(profiles)}): "))

                    if 1 <= follower_choice <= len(profiles):
                        follower = profiles[follower_choice - 1]
                        following = gram.get_following(follower)

                        if not following:
                            print(f"{follower.get_name()} is not following anyone.")
                        else:
                            print(f"Select which user {follower.get_name()} should unfollow:")
                            for i, person in enumerate(following, 1):
                                print(f"{i}.) {person.get_name()}")

                            followee_choice = int(input(f"Select (1 - {len(profiles)}): "))

                            if 1 <= followee_choice <= len(following):
                                followee = following[followee_choice - 1]
                                gram.unfollow(follower, followee)
                                print(f"{follower.get_name()} has unfollowed {followee.get_name()}")
                            else:
                                print("Invalid selection.")
                    else:
                        print("Invalid profile selection.")
                except ValueError:
                    print("Please enter valid numbers.")

            elif choice == 8:
                # Quit the program
                print("Thank you for using Slow Gram. Goodbye!")
                break

            else:
                print("Invalid choice. Please select a number between 1 and 8.")

        except ValueError:
            print("Please enter a valid number.")

        # Pause to let user read the output
        input("\nPress Enter to continue...")


# Run the program if this file is executed directly
if __name__ == "__main__":
    main()
