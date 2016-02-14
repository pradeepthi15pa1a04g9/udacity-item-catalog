"""Script to make a user with a specified email address an admin"""

from catalog.database import db_session
from catalog.models import User
import sys

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print "Insufficient arguments"
        exit()

    command = sys.argv[1].lower()
    email_address = sys.argv[2]

    if command not in ("grant", "revoke"):
        print "command not recognised"
        exit()

    print "Looking for a user with email address: %s" % email_address
    
    users = db_session.query(User).filter_by(email=email_address).all()

    print "Found the following users:"
    print
    for user in users:
        print user
    print

    confirmation = "%s admin privileges? (y/n): " % command.capitalize()
    decision = raw_input(confirmation).lower()
    if not decision.startswith("y"):
        print "Aborting"
        exit()

    if command == "grant":
        priv = True
    else:
        priv = False
    
    for user in users:
        user.admin = priv

    db_session.commit()

    print "Admin privileges changed."
    print
    for user in users:
        print user
    print
    print "Goodbye"
    print