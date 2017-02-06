BUGS
===

1. Usernames are case-sensitive. That shouldn't matter.
juan should be same as Juan or jUan or JUAN etc.

2. Important fields are not enforced when committing
to database. In user, for example, nickname and 
email should be present before committing. 

3. Timestamps should be added automatically in the db,
not in the code.

4. a last_changed field is missing in every model which
also should be automatically updated. A create method
is also missing. The create method would allow inserting
entities in the database without have to do the 
db.session.add(x); db.session.commit journey. 

5. Replaace custom async decorator for Python's standard
asyn decorator. 


TODO
===

1. Allow blocking users. A user cannot see the posts
from another user who blocked her.

2. Allow creating groups. Users in a group can see
all posts in the group without being friends. When
a user is in the group view, only posts in the group
are shown. 

3. Include a chat with Ejabberd. Create a view that
lists all your conversations, and another view to
list all messages exchanged with a specific user. Load 
data on demand, not all messages at once. 

4. Bring Bootstrap to the UI.

5. Bring Angular2 to the UI.

6. Allow filtering posts by user, topic, or date of
publication. 

7. Include a view that lists all users you're following.

8. Include a view that lists all of your followers.

9. Limit the amount of retrieved in a single hit. Load
more on demand with AJAX requests. 

10. Allow reposting.

12. Change the elements in the post template as 
follows: user, post, and date of posting should become
JavaScript objects. 

13. Include in the post object how many people read
the post and how many reposted.

14. Create a view for the most popular posts. 

15. Allow users to decide who can see certain posts.

16. Allow users to decide when or whether posts should 
disappear after a certain amount of time. 

17. Include link to denounce abusive users or posts.

18. Create a view of most influential users, those 
with the most outreaching posts. 

19. Allow login with facebook 

20. Add login with simple user + password with email
verification link 

21. Allow including more complex information in the user
profile

22. Include geolocation of posts and users

23. Make visualizations with posts and maps 

24. Allow video streaming

25. Expose Restful API so that people can automate posting,
for example when posting news or data. This needs to be
done with a secure token

26. Auto update state of the views. If another user
makes a comment to our post, we should see it 
inmediately. 
