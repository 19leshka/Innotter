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
    <li>(PATCH) <code>/api/user/update_profile/</code> - update profile</li>
    <hr>
    <h4>Page</h4>
    <li> (POST) <code>/api/auth/page/</code> - create page</li>
    <li> (PATCH) <code>/api/auth/page/<:pk>/</code> - update page</li>
    <li> (GET) <code>/api/auth/page/<:pk>/follow/</code> - follow/unfollow/ page switch</li>
    <li> (GET) <code>/api/auth/page/my_pages/</code> - your own pages</li>
    <li> (PATCH) <code>/api/auth/page/<:pk>/approve_requests/</code> - approve follow requests
    <p>{
    "follow_requests": [user_id]
    }</p><li> (PATCH) <code>/api/auth/page/<:pk>/reject_requests/</code> - reject follow requests
    <p>{
    "follow_requests": [user_id]
    }</p>
</li>
    
</ul>