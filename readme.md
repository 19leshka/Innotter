<h1>Innotter</h1>
<p>Actions:</p>
<ul>
    <hr>
    <h4>Auth</h4>
    <li> (POST) /api/auth/register/ - registration</li>
    <li> (POST) /api/auth/login/ - login</li>
    <hr>
    <h4>User</h4>
    <li>(GET) /api/user/profile/ - your profile</li>
    <li>(GET) /api/user/ - all profiles</li>
    <li>(GET) /api/user/<:pk>/ - user profile</li>
    <li>(PATCH) /api/user/update_profile/ - update profile</li>
    <hr>
    <h4>Page</h4>
    <li> (POST) /api/auth/page/ - create page</li>
    <li> (PATCH) /api/auth/page/<:pk>/ - update page</li>
    <li> (get) /api/auth/page/<:pk>/follow/ - follow/unfollow/ page switch</li>
    <li> (get) /api/auth/page/my_pages/ - your own pages</li>
    
</ul>