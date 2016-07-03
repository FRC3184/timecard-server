#!/usr/bin/python

print("Content-Type: text/html")
print("""
<form action="create_user.py" method="POST">
    <span>Create User</span><br />
    <label for="createname">Name</label> <input type="text" name="name" id="createname" />
    <input type="submit" />
</form><br />
<form action="login.py" method="POST">
    <span>Login</span><br />
    <label for="loginname">Name</label> <input type="text" name="name" id="loginname" />
    <input type="submit" />
</form><br />
<form action="logout.py" method="POST">
    <span>Logout</span><br />
    <label for="logoutname">Name</label> <input type="text" name="name" id="logoutname" />
    <input type="submit" />
</form>
""")
