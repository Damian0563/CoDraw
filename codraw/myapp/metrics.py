from prometheus_client import Counter


class Metrics:
    create_board = Counter("create_board", "Number of boards created")
    signin = Counter("signin", "Number of signins")
    signup = Counter("signup", "Number of signups")
    try_out = Counter("try_out", "Number of try outs of demo board")
    visit_site = Counter("visit_site", "Number of visits to the site")
    search = Counter("search", "Number of searches")
    active_users = Counter("active_users", "Number of active users")
