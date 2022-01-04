from resources.authors import LoginAuthor, RegisterAuthor, UpdateAuthor
from resources.editors import LoginEditor, RegisterEditor, UpdateEditor
from resources.clients import LoginClient, RegisterClient, UpdateClient
from resources.admins import LoginAdmin, RegisterAdmin
from resources.posts import Posts, UpdatePost, AuthorPosts, ClientPosts

routes = (
    (Posts, "/posts"),
    (UpdatePost, "/posts/<int:pk>"),
    (LoginAuthor, "/authors/login"),
    (RegisterAuthor, "/authors/register"),
    (UpdateAuthor, "/authors/<int:pk>"),
    (AuthorPosts, "/authors/<int:pk>/posts"),
    (LoginEditor, "/editors/login"),
    (RegisterEditor, "/editors/register"),
    (UpdateEditor, "/editors/<int:pk>"),
    (LoginClient, "/clients/login"),
    (RegisterClient, "/clients/register"),
    (UpdateClient, "/clients/<int:pk>"),
    (ClientPosts, "/clients/<int:pk>/posts"),
    (LoginAdmin, "/admins/login"),
    (RegisterAdmin, "/admins/register"),
)
