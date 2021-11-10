# Task - *VOTING APP*

🛠️ Difficulty Level: Intermediate
🗓️ Start: November 5th
🗓️ Deadline: November 11th 16:00 (4PM) GMT

📝 Project Description
Allow users to vote give multiple choices

📔 User Stories
1. User must enter their name to take part in a poll
2. User is shown multiple polls that they can choose from
3. After clicking on a poll, user is shown a voting screen where they can vote on that poll
4. Store items and votes in a database
5. After voting, the user should see the results from everyone
6. User can only vote once per poll

⭐ Bonus features
1. Only allow authenticated users to vote
2. User can create their own polls 

🏆 Submission
Submit your application to the website:
Link coming soon

🛠️  Tools
https://firebase.google.com/
https://www.heroku.com/postgres



# Total time spent on this project - *14 hours*

# API
## [#] Allow voters decide whether their vote will be public or hidden
## [#] Block user from voting twice
## [*] Never let a user be able to see the results without voting
    Which means that the polls will be up infinetely or until author deletes it

# Client 
## [*] When already voted see total votes on right side of option (always)
### [*] Allow user which already voted to switch between displaying "option body" or "option votings" (a bunch of small avatars) on single tap
## [] Poll Deletion button if state user.username === poll.username
## [] Poll Creation (always on top of screen)
## [*] Register
## [*] Login
## [] Animations
## [] Responsiveness
## [*] Add ability to set up custom profile image while registering
## [*] Fix 'poll' components not rerendering after logout 



*key mistake in frotnend*
components have problems rerendering because of the way they receive data. next time i will do this on a parent components and have its children not worry about fetching data or at least limit it