# Forum Server

Forum Server is a back-end API created with Django that utilized PostgreSQL to store and retrieve data about Posts, Comments, and Likes for the "Let's Talk" forum client application.

# Links

- Deployed Client Application: [https://areeshz.github.io/forum-client/](https://areeshz.github.io/forum-client/)
- Deployed Forum API: [https://forum-server-capstone.herokuapp.com/](https://forum-server-capstone.herokuapp.com/)
- Front-End Repository: [https://github.com/areeshz/forum-client](https://github.com/areeshz/forum-client)

## Technologies Used

- Python
- Django
- Django REST Framework
- PostgreSQL

## Entity Relationship Diagram

![IMG_2755](https://media.git.generalassemb.ly/user/27946/files/aba67380-dc23-11ea-8e24-202343d0704a)

## API End Points

| Verb   | URI Pattern               | Controller#Action |
|--------|---------------------------|-------------------|
| POST   | `/sign-up/`               | `users#signup`    |
| POST   | `/sign-in/`               | `users#signin`    |
| DELETE | `/sign-out`               | `users#signout`   |
| PATCH  | `/change-password/`       | `users#changepw`  |
| GET    | `/posts`                  | `posts#index`     |
| POST   | `/posts/`                 | `posts#create`    |
| GET    | `/posts/:id`              | `posts#show`      |
| PATCH  | `/posts/:id`              | `posts#update`    |
| DELETE | `/posts/:id`              | `posts#destroy`   |
| POST   | `/comments/`              | `comments#create` |
| PATCH  | `/comments/:id`           | `comments#update` |
| DELETE | `/comments/:id`           | `comments#destroy`|

## Planning and Execution
Development of this server came in several iterations, each adding another feature for the Let's Talk forum client application to utilize. After development of the ERD, models and views were created for the 'Post' resource. Next, models and views were created for the 'Comment' resource. Last was the 'Like' resource, which created a many-to-many relationship between users and posts.

## Next Steps
Future iterations of this server would attempt to enable additional features present in mainstream forum websites, such as allowing a user to make a comment on a comment (create threads).

## Setup Steps

1. [Fork and clone](https://git.generalassemb.ly/ga-wdi-boston/meta/wiki/ForkAndClone) this repository.
2. Run `pipenv shell` to enter the virtual environment
3. Create a database named `forum_server_dev` in PostgreSQL by running `psql` to enter the shell, and then `CREATE DATABASE forum_server_dev`
3. In your terminal, run `python manage.py makemigrations` and `python manage.py migrate` to ensure your database is up to date
4. Run `python manage.py runserver` to spin up your local server
