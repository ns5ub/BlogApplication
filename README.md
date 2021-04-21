# BlogApplication

**Problem Statement**: "Using any language or framework, we ask that you design and build an article or blog post on which others can submit comments. Your code should touch on both the front end and the back end."

This is a simple blog created using the Django full-stack framework primarily in Python. Bootstrap was used for the visual design of the code.


## Design Process:
This application takes the MVC style of development to heart. As such, I designed the application with this in mind.

### Model

Essentially an interface to the data in the actual database. These models allow for the developer to define the underlying database, setup relations, ecetra. This simple blog revolves around two main models. This information is stored in "models.py"

- Blog Post: The model to store the data relevant to any given post: title, body, date of creation. Currently, posts are associated to some superuser as defined by Django. In addition, these superusers have the ability to make posts hiddent or not. An extremely simple blog post that includes a title, body, and a date of creation.
  - Markdown? Currently, this model does not include markdown - each body is simply text.
  - Users? A more robust user system could be created using, for example, google authentication. This could allow users to be classified as authors, and post to the blog as well. 
- Comment: This model includes similar basic information as above. Most relevant however - each comment must be associated with a post. When a post is deleted, all associated comments are also deleted. In addition, in order to facilitate replies, a parent field was created.
  - Multithreaded Comments? As of now, the blog simply allows you to reply to original comments. Multithreaded replies could benefit from some sort of tree structure in the backend database.
  - Like/Dislike: This could be accomplished by creating counters for likes within the comment model, and restricting this option based on whether the user is logged in or not. 

### Controller

The controller decides what is exposed to the View, and performs any logic required. "view.py"

- List Blog Posts: One controller must simply output the list of blog posts in cronological order, filtering out those that are not visibile.
- View Post Details: This controller must both display the appropriate post as well as any associated comments. In addition, it must handle the logic in taking in any new comments. This comments should be cleaned before being stored in the database.

### View

What the end user sees

- List Blog Posts: A list of blog posts, with links allowing them to view individual blog posts. Could include pagination, search, filters. For now, is a simple ListView - aka, a list of all the posts.
- Post Details: Should display a particular post fully, as well as any comments. Should have a place to leave your own comments, view previous comments, and reply to those previous comments.
