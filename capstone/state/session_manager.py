from state.document_state import DocumentState


class SessionManager:

    def __init__(self):

        self.sessions = {}

    def create_session(self, session_id):

        self.sessions[session_id] = (
            DocumentState()
        )

        return self.sessions[session_id]

    def get_session(self, session_id):

        return self.sessions.get(session_id)