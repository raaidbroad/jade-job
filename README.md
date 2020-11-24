# jade-job
A simple tool to be notified of when a Jade (Terra Data Repo) job has completed.

Status: 2020/11/24 | In development

## CLI V0
At a minimum, here are the requirements:

Inputs:
- Jade environment (dev | prod)
- Job ID

Outputs:
- Status code
- Status message

At least to start with, auth should be handled through google. So if a user is using the dev environment, they need to make sure that they have run the following command:
`gcloud auth application-default login`

And have selected their dev account.

This could look like this:
`> jadejobs dev myfakejobid123`
`...running`
`Job finished: 201, succeeded`

And:
`> jadejobs prod myfakejobid456`
`Error: my.fake.dev.account@gmail.com is not authorized for prod`

## CLI V1
Cool, we have it up and running! But all we've really done is that instead of hitting "execute" repeatedly on Swagger, we just keep checking terminal until the job is done. Better, but not by a whole lot.

Enter notifications. For Mac users (who are our primary audience since pretty much every developer in DSP is on a Mac), we can very simple create a a notification with AppleScript. We can call it from Python too: https://stackoverflow.com/questions/3489297/how-to-run-an-applescript-from-within-a-python-script

Boom, notifications added.

## V2: Slackbot
Now having a simple async CLI thing is nice and all, but we all use slack and it'd be awesome to be able to type this in slack:
`/jadejob dev myfakejobid123`
TODO
