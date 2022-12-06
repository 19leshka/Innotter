<h1>Innotter</h1>
<p>Actions:</p>
<ul>
    <hr>
    <h4>Auth</h4>
    <li> (POST) <code>/api/auth/register/</code> - registration</li>
    <li> (POST) <code>/api/auth/login/</code> - login</li>
    <hr>
    <h4>User</h4>
    <li>(GET) <code>/api/user/profile/</code> - your profile</li>
    <li>(GET) <code>/api/user/</code> - all profiles</li>
    <li>(GET) <code>/api/user/<:pk>/</code> - user profile</li>
    <li>(PATCH) <code>/api/user/update-profile/</code> - update profile</li>
    <hr>
    <h4>Page</h4>
    <li> (POST) <code>/api/page/</code> - create page</li>
    <li> (PATCH) <code>/api/page/<:pk>/</code> - update page</li>
    <li> (GET) <code>/api/page/<:pk>/follow/</code> - follow/unfollow page switch</li>
    <li> (GET) <code>/api/page/my-pages/</code> - your own pages</li>
    <li> (PATCH) <code>/api/page/<:pk>/approve-requests/</code> - approve follow requests
    <p>{
    "follow_requests": [user_id]
    }</p><li> (PATCH) <code>
/api/page/<:pk>/reject-requests/
</code> - reject follow requests
    <p>{
    "follow_requests": [user_id]
    }</p>
    </li>
    <li> (GET) <code>/api/page/all-liked-posts/</code> - all your liked posts</li>
    <li> (GET) <code>/api/page/<:pk>/page-liked-posts/</code> - all your liked posts on page</li>
<hr>
<h4>Post</h4>
<li> (POST) <code>/api/post/</code> - create post</li>
<li> (PATCH) <code>/api/post/<:pk>/</code> - update post</li>
<li> (GET) <code>/api/post/<:pk>/like/</code> - like/unlike post switch</li>
    
</ul>