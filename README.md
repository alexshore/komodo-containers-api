# Komodo Containers API

I wanted an API to show all currently running and stopped containers as well as a total count so I could create a custom widget in homepage.
Unfortunately the endpoint that I would use doesn't exist natively in Komodo so this is just a quick FastAPI middleman that requests data from
`ListAllDockerContainers` and then tallies the information from there.
