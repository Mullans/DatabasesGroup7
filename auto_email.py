def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox21492247c0a34558a909eca1d73200eb.mailgun.org/messages",
        auth=("api", "8571c86055f9c0fb4a572437d21fea58-059e099e-386b6281"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox21492247c0a34558a909eca1d73200eb.mailgun.org>",
              "to": "jonathon takes <jonathon-takes@uiowa.edu>",
              "subject": "Hello jonathon takes",
              "text": "Congratulations jonathon takes, you just sent an email with Mailgun!  You are truly awesome!"})
