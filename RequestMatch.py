class ViewRequests:
    """
        Class for viewing friend requests
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def view(self):
        print("1. Sent Requests")
        print("2. Received Requests")
        option = input("Enter Your Option: ")
        if option == '1':
            sent_requests = db.getSentRequests(self.user_id)
            if not sent_requests:
                print("You have no sent friend requests.")
            else:
                print("Sent friend requests:")
                for r in sent_requests:
                    status = "Accepted" if r[2] == 1 else "Pending"
                    print(f"{r[0]}. {r[1]} - Status: {status}")

                req_id = input("Enter the request ID to delete or type 'back' to go back: ")
                if req_id.lower() == 'back':
                    return
                else:
                    db.deleteSentRequest(self.user_id, int(req_id))
                    print("Sent request deleted successfully.")
        elif option == '2':
            received_requests = db.getReceivedRequests(self.user_id)
            if not received_requests:
                print("You have no friend requests.")
            else:
                print("Received friend requests:")
                for r in received_requests:
                    status = "Accepted" if r[2] == 1 else "Pending"
                    print(f"{r[0]}. {r[1]} - Status: {status}")

                req_id = input("Enter the request ID to accept or reject, or type 'back' to go back: ")
                if req_id.lower() == 'back':
                    return
                else:
                    action = input("Type 'accept' or 'reject' to take action on the request: ")
                    if action.lower() == 'accept':
                        db.acceptReceivedRequest(self.user_id, int(req_id))
                        print("Request accepted successfully.")
                    elif action.lower() == 'reject':
                        db.rejectReceivedRequest(self.user_id, int(req_id))
                        print("Request rejected successfully.")
                    else:
                        print("Invalid action. Going back.")
        else:
            print("Invalid option. Going back.")

class ViewMatches:
    """
        Class for viewing matches
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def view(self):
        matches = db.getMatches(self.user_id)
        if not matches:
            print("You have no matches.")
        else:
            print("Your matches:")
            for m in matches:
                print(f"{m[0]}. {m[1]}")