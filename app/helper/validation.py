def validation_req(req, *args):
    """
    Validate the requests by passing this func and it return true or false

    Args: request (flask object), <List> target validation
    """
    if not req:
        return False

    for arg in args:
        if not req.get(arg):
            return False

    return True
