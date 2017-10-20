# CS4501 Project - Used Clothing App

## Notes About Changes

- You guys will need to DROP & RECREATE DATABASE (like last time) as well as DELETE YOUR MIGRATIONS FOLDER. This will allow the model changes to load correctly.
- When logging in, you can't use users in the fixtures because of how the password checking works (the password needs to have been hashed, and that only happens if you create a user from a URL call).
- There are pre-existing buttons to link to the create item and log out pages once you're logged in! You can modify these to go to the correct urls in base.html (every web page should inherit from this). 

The authenticate(request) method should be called in EVERY WEB VIEW. As such:
```python
auth = authenticate(request)
if auth['logged_in']:
    resp['logged_in'] = auth['username']
```
Where resp is the dictionary of data values being returned to the rendered page. You can check if a user is logged in by doing {% if logged_in %} because that'll be true if it exists in the data, false if it doesn't. Some pages are exceptions to this rule. It's important it's on every page because it alters the look of our base.html.

## Directions for the other two parts:

### Log-Out
- Create a link through the button once logged in. 
- Should delete the cookie at the top (see specification), and make a call to the API layer to delete the authenticator in the database (this means you need to get the value of the authenticator beforehand becasue it's the primary key for the database row). 
- Should send a POST method to the API layer - finding and deleting the authenticator, doing general error checking (what if you can't find it? What if it's the wrong method type?) See other deletion methods for reference! 
- Once you're sure of success, return to the top. The page should automatically revert back to logged-out mode upon deletion of the cookie.
- Because you have to make a new API method, you also have to make tests for it! See the other Authentication tests and deletion tests to figure out how to ensure the basic use cases work. 

## Create Listing
- This page needs to ONLY render if the user is logged in, even if they directly type in the URL (see my login method for an example of this restriction).
- Create a form for item creation, using all the relevant fields (ones that need to be filled in - you don't need to fill in user because you get that by authenticating, and you don't need to fill in the date because that's automatic). 
- This will include a place to attach an image URL. 
- See Sign Up page for an example as to how to have the page render based on the form you made! Don't hard-code it!
- Because you have to go to the Model API before knowing what errors there are (see how this works in the model view, I made it so errors are returned if fields are invalid instead of failing), you'll have to send them back up and render them on the top page, I usually also just redirect them to the same blank form so they can re-submit. (See sign up page web/exp/view for an example of how to do this!) 
- They should get some kind of notification if the item is made.
- The item should appear on the home page if it's a shoe, top or bottom. 
