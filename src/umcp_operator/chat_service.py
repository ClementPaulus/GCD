# Operator chat service for GCD operator backend
from .types import ChatRequest, ChatResponse, OperatorAnswer, SpineState


class ChatService:
    def chat(self, payload: ChatRequest) -> ChatResponse:
        # TODO: Implement chat logic
        # For now, return a stub with a valid SpineState
        stub_spine = SpineState(contract=None, canon=None, closures=[], ledger=None, stance=None)
        return ChatResponse(
            messageId="msg_01J_stub",
            answer=OperatorAnswer(
                messageId="msg_01J_stub",
                plainText="(stub)",
                structured=stub_spine,
                usedObjects=[],
                ceAudit=None,
            ),
            usedObjects=[],
            ceAudit=None,
        )


CHAT_SERVICE = ChatService()
