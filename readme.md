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
    <li>(POST) <code>/api/user/<:pk>/block/</code> - block/unblock switch (only by admin)</li>
    <hr>
    <h4>Page</h4>
    <li> (POST) <code>/api/pages/</code> - create page</li>
    <li> (PATCH) <code>/api/pages/<:pk>/</code> - update page</li>
    <li> (GET) <code>/api/pages/<:pk>/follow/</code> - follow/unfollow page switch</li>
    <li> (GET) <code>/api/pages/my-pages/</code> - your own pages</li>
    <li> (PATCH) <code>/api/pages/<:pk>/approve-requests/</code> - approve follow requests
    <li>(POST) <code>/api/page/<:pk>/block/</code> - block/unblock switch (only by moder/admin)</li>
    <p>{
    "follow_requests": [user_id]
    }</p><li> (PATCH) <code>
/api/pages/<:pk>/reject-requests/
</code> - reject follow requests
    <p>{
    "follow_requests": [user_id]
    }</p>
    </li>
    <hr>
    <h4>Post</h4>
    <li> (POST) <code>/api/posts/</code> - create post</li>
    <li> (PATCH) <code>/api/posts/<:pk>/</code> - update post</li>
    <li> (GET) <code>/api/posts/<:pk>/like/</code> - like/unlike post switch</li>
    <li> (GET) <code>/api/posts/all-liked-posts/</code> - all your liked posts</li>
    <li> (GET) <code>/api/posts/<:pk>/page-liked-posts/</code> - all your liked posts on page</li>
    
</ul>