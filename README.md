# GitLab backup script

This container contains a script, `backup.py`, for backing up GitLab repositories.

The script requires a GitLab token, a destination directory and the URL of your GitLab instance. It then uses the token to populate the destination directory with clones of all the repositories the token can access.

It is possible to set it to run on a schedule, and repeated runs only update the already existing backups and add new repositories, if any.

## Configuration

### Create a token
For authorization, you need to create a new personal GitLab token. You can do this from [this](https://gitlab.com/-/user_settings/personal_access_tokens) page.


When you click the **Add new token** button, enter the token creation screen. Here you should give the token a descriptive name and choose its *scopes*, which determine what the token can do.


To backup repositories, select **read_api** and **read_repository** scopes. 


After clicking the **Create personal access token** button you're presented with the generated token. Remember to store it now, as GitLab won't show it to you anymore!


## Final note
If you notice any bugs, feel free to open an Issue or a pull request.
