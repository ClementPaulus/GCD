# Operator session store for GCD operator backend
from datetime import UTC

from .types import CreateSessionRequest, OperatorSession


class SessionStore:
    def __init__(self) -> None:
        self.sessions: dict[str, OperatorSession] = {}

    def create(self, payload: CreateSessionRequest) -> OperatorSession:
        import uuid
        from datetime import datetime

        from .types import SessionMemory

        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        now = datetime.now(UTC).replace(microsecond=0).isoformat()
        session = OperatorSession(
            sessionId=session_id,
            mode=payload.mode,
            activeContractId=payload.activeContractId,
            activeClosureIds=payload.activeClosureIds or [],
            activeCasepackId=payload.activeCasepackId,
            workingSet=[],
            currentRunId=None,
            currentWeldId=None,
            memory=SessionMemory(),
            createdAt=now,
            updatedAt=now,
        )
        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> OperatorSession | None:
        return self.sessions.get(session_id)

    def update_contract(self, session_id: str, contract_id: str) -> OperatorSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(f"Session not found: {session_id}")
        session.activeContractId = contract_id
        self.sessions[session_id] = session
        return session

    def save(self, session: OperatorSession) -> OperatorSession:
        self.sessions[session.sessionId] = session
        return session


SESSION_STORE = SessionStore()
