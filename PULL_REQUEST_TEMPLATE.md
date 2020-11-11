#### Changes Made
1. Added file `PostForm.js` to `posts` directory.
1. Modified file `PostProvider.js` to include `createPost` and functionality.
1. Modified `ApplicationViews.js` to include path routed to `PostForm` view.
​
#### Steps to Review
1. Checkout this branch locally and run the application.
```
git fetch --all
git checkout mp-create-post
```
2. Run the application.
```
npm start
```
3. Open a new Terminal tab (⌘T) and navigate to the server directory.
```
..
server
```
4. Initialize virtual environment, and run the server.
```
pipenv shell
python manage.py runserver
```
5. Test app functionality.
> When user clicks on `New Post`, they should be redirected to a the PostForm page
> When user enters information into the form fields and clicks `Save`, the post database should be updated with new post object and user should be redirected to the PostDetails page to view the post they just created.
6. View code file.
> Confirm file modifications are present as indicated above.
> Confirm no unused code or extraneous comments exist.