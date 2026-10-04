# -*- coding: utf-8 -*-

"""
============================================================
MYX / MAYAX AI
CORE BRAIN
============================================================

Architecture:

User Input
    ↓
Input Understanding
    ↓
Memory Context
    ↓
Decision
    ├── Conversation
    │      ↓
    │   AI Manager
    │      ↓
    │   Gemini / DeepSeek / OpenAI
    │
    └── Action
           ↓
       Global Action Pipeline
           ↓
       Discovery → Search → Resolve
           ↓
       Safety → Selection → Execution

Persistence:

Brain
    ↓
DatabaseManager
    ↓
SQLite

Memory:

Brain
    ↓
MemoryManager
    ↓
MemoryContext
    ↓
Persistent Memory

Responsibilities:
    - receive user input
    - understand input
    - maintain user context
    - connect database
    - connect memory
    - build memory context
    - route conversation
    - route actions
    - connect AI Manager
    - persist conversation history
    - expose health status

The Brain does NOT directly launch applications.
============================================================
"""

import os
import sys
import traceback


# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SRC_DIR = os.path.dirname(CURRENT_DIR)

PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# AI MANAGER
# ============================================================

try:

    from src.ai.ai_manager import AIManager

except Exception as e:

    AIManager = None

    print(
        f"[Brain] AI Manager import warning: {e}"
    )


# ============================================================
# INPUT UNDERSTANDING
# ============================================================

try:

    from src.core.understanding.input_understanding import (
        InputUnderstanding
    )

except Exception as e:

    InputUnderstanding = None

    print(
        f"[Brain] Input Understanding import warning: {e}"
    )


# ============================================================
# GLOBAL ACTION PIPELINE
# ============================================================

try:

    from src.system.actions.global_action_pipeline import (
        GlobalActionPipeline
    )

except Exception as e:

    GlobalActionPipeline = None

    print(
        f"[Brain] Global Pipeline import warning: {e}"
    )


# ============================================================
# DATABASE
# ============================================================

try:

    from src.database.manager import DatabaseManager

except Exception as e:

    DatabaseManager = None

    print(
        f"[Brain] Database import warning: {e}"
    )


# ============================================================
# MEMORY MANAGER
# ============================================================

try:

    from src.memory.memory_manager import MemoryManager

except Exception as e:

    MemoryManager = None

    print(
        f"[Brain] Memory Manager import warning: {e}"
    )


# ============================================================
# MEMORY CONTEXT
# ============================================================

try:

    from src.memory.memory_context import MemoryContext

except Exception as e:

    MemoryContext = None

    print(
        f"[Brain] Memory Context import warning: {e}"
    )


# ============================================================
# BRAIN
# ============================================================

class Brain:
    """
    Central MyX Brain.

    Brain connects:

        Input Understanding
        Memory
        Memory Context
        AI Manager
        Global Action Pipeline
        Database Persistence

    Brain does not directly execute applications.
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        self_router=None,
        memory=None,
        conversation=None,
        config=None,
        user_id=None,
        database=None
    ):

        # ----------------------------------------------------
        # Compatibility Components
        # ----------------------------------------------------

        self.router = self_router

        self.conversation = conversation

        self.config = config

        # ----------------------------------------------------
        # User Context
        # ----------------------------------------------------

        self.user_id = user_id

        # ----------------------------------------------------
        # Persistent Database
        # ----------------------------------------------------

        self.database = database

        if (
            self.database is None
            and DatabaseManager is not None
        ):

            try:

                self.database = DatabaseManager()

                print(
                    "[Brain] Persistent Database Connected"
                )

            except Exception as e:

                self.database = None

                print(
                    f"[Brain] Database connection warning: {e}"
                )

        # ----------------------------------------------------
        # Persistent Memory
        # ----------------------------------------------------

        self.memory = memory

        if (
            self.memory is None
            and self.database is not None
            and MemoryManager is not None
        ):

            try:

                self.memory = MemoryManager(
                    database=self.database
                )

                print(
                    "[Brain] Persistent Memory Connected"
                )

            except Exception as e:

                self.memory = None

                print(
                    f"[Brain] Memory connection warning: {e}"
                )

        # ----------------------------------------------------
        # Memory Context
        # ----------------------------------------------------

        self.memory_context = None

        if (
            self.memory is not None
            and MemoryContext is not None
        ):

            try:

                self.memory_context = MemoryContext(
                    memory_manager=self.memory
                )

                print(
                    "[Brain] Memory Context Connected"
                )

            except Exception as e:

                self.memory_context = None

                print(
                    f"[Brain] Memory Context warning: {e}"
                )

        # ----------------------------------------------------
        # Input Understanding
        # ----------------------------------------------------

        self.understanding = None

        if InputUnderstanding is not None:

            try:

                self.understanding = (
                    InputUnderstanding()
                )

                print(
                    "[Brain] Input Understanding Connected"
                )

            except Exception as e:

                print(
                    "[Brain] Input Understanding "
                    f"initialization warning: {e}"
                )

        # ----------------------------------------------------
        # Global Action Pipeline
        # ----------------------------------------------------

        self.global_pipeline = None

        if GlobalActionPipeline is not None:

            try:

                self.global_pipeline = (
                    GlobalActionPipeline()
                )

                print(
                    "[Brain] Global Action Pipeline Connected"
                )

            except Exception as e:

                print(
                    "[Brain] Global Pipeline "
                    f"initialization warning: {e}"
                )

        # ----------------------------------------------------
        # AI MANAGER
        # ----------------------------------------------------

        self.ai_manager = None

        if AIManager is not None:

            try:

                self.ai_manager = AIManager()

                print(
                    "[Brain] AI Manager Connected"
                )

            except Exception as e:

                self.ai_manager = None

                print(
                    "[Brain] AI Manager "
                    f"initialization warning: {e}"
                )

        # ----------------------------------------------------
        # Initialization State
        # ----------------------------------------------------

        self.initialized = True

        print(
            "[Brain] Core Brain Initialized"
        )

    # ========================================================
    # USER CONTEXT
    # ========================================================

    def set_user(self, user_id):

        if user_id is None:

            self.user_id = None

            return None

        self.user_id = str(
            user_id
        ).strip()

        print(
            f"[Brain] Active User: {self.user_id}"
        )

        return self.user_id

    # --------------------------------------------------------

    def get_user_id(self):

        return self.user_id

    # ========================================================
    # DATABASE STATUS
    # ========================================================

    def database_connected(self):

        return (
            self.database is not None
        )

    # ========================================================
    # MEMORY STATUS
    # ========================================================

    def memory_connected(self):

        return (
            self.memory is not None
        )

    # ========================================================
    # MEMORY CONTEXT STATUS
    # ========================================================

    def memory_context_connected(self):

        return (
            self.memory_context is not None
        )

    # ========================================================
    # AI STATUS
    # ========================================================

    def ai_connected(self):

        return (
            self.ai_manager is not None
            and self.ai_manager.is_ready()
        )

    # --------------------------------------------------------

    def ai_status(self):

        if self.ai_manager is None:

            return {
                "connected": False,
                "providers": [],
                "count": 0
            }

        try:

            status = self.ai_manager.status()

            return {
                "connected": self.ai_connected(),
                **status
            }

        except Exception as e:

            return {
                "connected": False,
                "providers": [],
                "count": 0,
                "error": str(e)
            }

    # ========================================================
    # PERSISTENCE STATUS
    # ========================================================

    def persistence_ready(self):

        return (
            self.database is not None
            and self.user_id is not None
            and str(self.user_id).strip() != ""
        )

    # ========================================================
    # MEMORY API
    # ========================================================

    def remember(
        self,
        key,
        value
    ):

        if self.memory is None:

            return False

        try:

            return self.memory.remember(
                key,
                value
            )

        except Exception as e:

            print(
                f"[Brain] Memory write warning: {e}"
            )

            return False

    # --------------------------------------------------------

    def recall(
        self,
        key,
        default=None
    ):

        if self.memory is None:

            return default

        try:

            return self.memory.recall(
                key,
                default
            )

        except Exception as e:

            print(
                f"[Brain] Memory recall warning: {e}"
            )

            return default

    # --------------------------------------------------------

    def recall_all(self):

        if self.memory is None:

            return []

        try:

            return self.memory.recall_all()

        except Exception as e:

            print(
                f"[Brain] Memory list warning: {e}"
            )

            return []

    # --------------------------------------------------------

    def forget(self, key):

        if self.memory is None:

            return False

        try:

            return self.memory.forget(
                key
            )

        except Exception as e:

            print(
                f"[Brain] Memory delete warning: {e}"
            )

            return False

    # ========================================================
    # MEMORY CONTEXT
    # ========================================================

    def build_memory_context(
        self,
        user_input=None,
        limit=10
    ):

        empty_context = {

            "available": False,

            "query": (
                str(user_input)
                if user_input is not None
                else ""
            ),

            "memories": [],

            "count": 0,
        }

        if self.memory_context is None:

            return empty_context

        try:

            return self.memory_context.build_context(
                user_input=user_input,
                limit=limit
            )

        except Exception as e:

            print(
                f"[Brain] Memory context warning: {e}"
            )

            return empty_context

    # --------------------------------------------------------

    def get_memory_context_text(
        self,
        user_input=None,
        limit=10
    ):

        context = self.build_memory_context(
            user_input=user_input,
            limit=limit
        )

        if self.memory_context is None:

            return ""

        try:

            return self.memory_context.format_context(
                context
            )

        except Exception as e:

            print(
                f"[Brain] Memory context format warning: {e}"
            )

            return ""

    # ========================================================
    # PROCESS
    # ========================================================

    def process(self, user_input):

        return self.think(
            user_input
        )

    # ========================================================
    # THINK
    # ========================================================

    def think(self, user_input):

        # ----------------------------------------------------
        # Normalize
        # ----------------------------------------------------

        if user_input is None:

            return (
                "I didn't receive any input."
            )

        user_input = str(
            user_input
        ).strip()

        if not user_input:

            return (
                "I didn't receive any input."
            )

        # ----------------------------------------------------
        # Input Understanding
        # ----------------------------------------------------

        understanding = {

            "type": "conversation",

            "is_action": False,

            "is_conversation": True,
        }

        if self.understanding is not None:

            try:

                result = self.understanding.analyze(
                    user_input
                )

                if isinstance(
                    result,
                    dict
                ):

                    understanding = result

            except Exception as e:

                print(
                    "[Brain] Understanding warning: "
                    f"{e}"
                )

                understanding = {

                    "type": "conversation",

                    "is_action": False,

                    "is_conversation": True,
                }

        print(
            "[Brain] Input Type: "
            f"{understanding.get('type', 'conversation')}"
        )

        # ----------------------------------------------------
        # Memory Context
        # ----------------------------------------------------

        memory_context = (
            self.build_memory_context(
                user_input=user_input
            )
        )

        # ----------------------------------------------------
        # Conversation
        # ----------------------------------------------------

        if understanding.get(
            "is_conversation",
            False
        ):

            response = (
                self._conversation_response(
                    user_input,
                    memory_context
                )
            )

            self._store_conversation(
                user_input,
                response
            )

            return response

        # ----------------------------------------------------
        # Action
        # ----------------------------------------------------

        response = self._process_action(
            user_input
        )

        self._store_conversation(
            user_input,
            response
        )

        return response

    # ========================================================
    # ACTION PROCESSING
    # ========================================================

    def _process_action(
        self,
        user_input
    ):

        # ----------------------------------------------------
        # Global Action Pipeline
        # ----------------------------------------------------

        if self.global_pipeline is not None:

            try:

                result = (
                    self.global_pipeline.process(
                        user_input
                    )
                )

                # Dictionary result

                if isinstance(
                    result,
                    dict
                ):

                    success = result.get(
                        "success",
                        False
                    )

                    message = result.get(
                        "message"
                    )

                    stage = result.get(
                        "stage"
                    )

                    if success:

                        if message:

                            return str(
                                message
                            )

                        return (
                            "Command completed successfully."
                        )

                    if message:

                        return str(
                            message
                        )

                    if stage:

                        return (
                            "Command could not be "
                            f"completed at stage: {stage}"
                        )

                # String result

                if isinstance(
                    result,
                    str
                ):

                    return result

                # Boolean result

                if result is True:

                    return (
                        "Command completed successfully."
                    )

            except Exception as e:

                print(
                    "[Brain] Global Action Pipeline "
                    f"warning: {e}"
                )

        # ----------------------------------------------------
        # Legacy Router
        # ----------------------------------------------------

        if self.router is not None:

            try:

                result = self.router.route(
                    user_input
                )

                if result is not None:

                    return str(
                        result
                    )

            except Exception as e:

                print(
                    "[Brain] Legacy router warning: "
                    f"{e}"
                )

        # ----------------------------------------------------
        # Final Action Fallback
        # ----------------------------------------------------

        return (
            "I understood the command, "
            "but I could not complete it: "
            f"{user_input}"
        )

    # ========================================================
    # CONVERSATION
    # ========================================================

    def _conversation_response(
        self,
        user_input,
        memory_context=None
    ):

        text = str(
            user_input
        ).strip().lower()

        # ----------------------------------------------------
        # Greetings
        # ----------------------------------------------------

        if text in (
            "hi",
            "hello",
            "hey"
        ):

            return (
                "Hello! How can I help you?"
            )

        if text == "good morning":

            return (
                "Good morning! How can I help you?"
            )

        if text == "good afternoon":

            return (
                "Good afternoon! How can I help you?"
            )

        if text == "good evening":

            return (
                "Good evening! How can I help you?"
            )

        # ----------------------------------------------------
        # Memory Status
        # ----------------------------------------------------

        if text in (
            "what do you remember",
            "what do you remember about me",
            "show my memories",
            "show memories",
        ):

            memories = self.recall_all()

            if not memories:

                return (
                    "I don't have any stored memories yet."
                )

            lines = []

            for item in memories:

                try:

                    if hasattr(
                        item,
                        "keys"
                    ):

                        key = item["key"]

                        value = item["value"]

                    elif (
                        isinstance(
                            item,
                            (tuple, list)
                        )
                        and len(item) >= 3
                    ):

                        key = item[1]

                        value = item[2]

                    else:

                        continue

                    lines.append(
                        f"{key}: {value}"
                    )

                except Exception:

                    continue

            if not lines:

                return (
                    "I have stored memories, "
                    "but I couldn't format them."
                )

            return (
                "Here is what I remember:\n"
                + "\n".join(lines)
            )

        # ----------------------------------------------------
        # AI Conversation
        # ----------------------------------------------------

        if self.ai_manager is not None:

            try:

                memory_text = ""

                if memory_context:

                    try:

                        memory_text = (
                            self.get_memory_context_text(
                                user_input=user_input
                            )
                        )

                    except Exception:

                        memory_text = ""

                prompt = self._build_ai_prompt(
                    user_input=user_input,
                    memory_text=memory_text
                )

                response = (
                    self.ai_manager.auto_generate(
                        prompt
                    )
                )

                if response:

                    response = str(
                        response
                    ).strip()

                    # Do not return provider failure
                    # messages as normal AI answers.

                    if not response.startswith(
                        "No AI provider"
                    ) and not response.startswith(
                        "AI provider "
                    ) and not response.startswith(
                        "Gemini Error:"
                    ) and not response.startswith(
                        "DeepSeek Error:"
                    ) and not response.startswith(
                        "OpenAI Error:"
                    ):

                        return response

            except Exception as e:

                print(
                    "[Brain] AI conversation warning: "
                    f"{e}"
                )

        # ----------------------------------------------------
        # Deterministic Fallback
        # ----------------------------------------------------

        return (
            f"I understand you said: {user_input}"
        )

    # ========================================================
    # AI PROMPT
    # ========================================================

    def _build_ai_prompt(
        self,
        user_input,
        memory_text=""
    ):

        prompt = f"""
You are MYX, a personal AI assistant.

Answer the user's request naturally, clearly,
and directly.

Do not claim to perform computer actions unless
the action pipeline has actually performed them.

User message:
{user_input}
"""

        if memory_text:

            prompt += f"""

Relevant persistent memory:
{memory_text}
"""

        prompt += """

Give only the useful assistant response.
"""

        return prompt.strip()

    # ========================================================
    # CONVERSATION STORAGE
    # ========================================================

    def _store_conversation(
        self,
        user_input,
        response
    ):

        # ----------------------------------------------------
        # Legacy Conversation
        # ----------------------------------------------------

        if self.conversation is not None:

            try:

                self.conversation.add(
                    "User",
                    user_input
                )

                self.conversation.add(
                    "MAYAX",
                    str(response)
                )

            except Exception as e:

                print(
                    f"[Memory Warning] {e}"
                )

        # ----------------------------------------------------
        # Persistent Database
        # ----------------------------------------------------

        if not self.persistence_ready():

            return

        try:

            self.database.query.save_message(
                self.user_id,
                "user",
                str(user_input)
            )

            self.database.query.save_message(
                self.user_id,
                "assistant",
                str(response)
            )

            print(
                "[Brain] Conversation persisted"
            )

        except Exception as e:

            print(
                "[Brain] Conversation persistence "
                f"warning: {e}"
            )

    # ========================================================
    # CONVERSATION HISTORY
    # ========================================================

    def get_conversation_history(
        self,
        user_id=None
    ):

        target_user = (
            user_id
            if user_id is not None
            else self.user_id
        )

        if self.database is None:

            return []

        if target_user is None:

            return []

        try:

            return self.database.query.get_history(
                target_user
            )

        except Exception as e:

            print(
                "[Brain] History read warning: "
                f"{e}"
            )

            return []

    # ========================================================
    # HEALTH
    # ========================================================

    def health(self):

        ai_info = self.ai_status()

        return {

            "brain": True,

            "initialized": self.initialized,

            "database": (
                self.database_connected()
            ),

            "memory": (
                self.memory_connected()
            ),

            "memory_context": (
                self.memory_context_connected()
            ),

            "understanding": (
                self.understanding is not None
            ),

            "global_pipeline": (
                self.global_pipeline is not None
            ),

            "ai": (
                ai_info["connected"]
            ),

            "ai_providers": (
                ai_info.get(
                    "providers",
                    []
                )
            ),

            "ai_provider_count": (
                ai_info.get(
                    "count",
                    0
                )
            ),

            "persistence": (
                self.persistence_ready()
            ),

            "user_id": self.user_id,
        }

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        if self.database is not None:

            try:

                self.database.close()

                print(
                    "[Brain] Database Closed"
                )

            except Exception as e:

                print(
                    "[Brain] Database close warning: "
                    f"{e}"
                )

        self.initialized = False


# ============================================================
# BRAIN INTEGRATION TEST
# ============================================================

def run_brain_test():

    print()

    print(
        "=" * 60
    )

    print(
        "          MYX BRAIN INTEGRATION TEST"
    )

    print(
        "=" * 60
    )

    brain = None

    try:

        # ----------------------------------------------------
        # Initialization
        # ----------------------------------------------------

        brain = Brain(
            user_id="test_user"
        )

        # ----------------------------------------------------
        # Test 1
        # ----------------------------------------------------

        if brain.understanding is not None:

            print(
                "[1] Input Understanding : PASS"
            )

        else:

            print(
                "[1] Input Understanding : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 2
        # ----------------------------------------------------

        if brain.global_pipeline is not None:

            print(
                "[2] Global Pipeline : PASS"
            )

        else:

            print(
                "[2] Global Pipeline : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 3
        # ----------------------------------------------------

        if brain.database_connected():

            print(
                "[3] Database Connection : PASS"
            )

        else:

            print(
                "[3] Database Connection : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 4
        # ----------------------------------------------------

        if brain.memory_connected():

            print(
                "[4] Memory Manager : PASS"
            )

        else:

            print(
                "[4] Memory Manager : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 5
        # ----------------------------------------------------

        if brain.memory_context_connected():

            print(
                "[5] Memory Context : PASS"
            )

        else:

            print(
                "[5] Memory Context : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 6
        # ----------------------------------------------------

        response = brain.process(
            "hi"
        )

        if isinstance(
            response,
            str
        ) and response.strip():

            print(
                "[6] Conversation : PASS"
            )

        else:

            print(
                "[6] Conversation : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 7
        # ----------------------------------------------------

        brain.set_user(
            "test_user"
        )

        if (
            brain.get_user_id()
            == "test_user"
        ):

            print(
                "[7] User Context : PASS"
            )

        else:

            print(
                "[7] User Context : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 8
        # ----------------------------------------------------

        if brain.persistence_ready():

            print(
                "[8] Persistence Ready : PASS"
            )

        else:

            print(
                "[8] Persistence Ready : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 9
        # ----------------------------------------------------

        test_key = (
            "__myx_brain_test_memory__"
        )

        test_value = (
            "MyX Brain memory integration works."
        )

        if brain.remember(
            test_key,
            test_value
        ):

            print(
                "[9] Memory Write : PASS"
            )

        else:

            print(
                "[9] Memory Write : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 10
        # ----------------------------------------------------

        recalled = brain.recall(
            test_key
        )

        if recalled == test_value:

            print(
                "[10] Memory Recall : PASS"
            )

        else:

            print(
                "[10] Memory Recall : FAIL"
            )

            print(
                "     Value:",
                recalled
            )

            return False

        # ----------------------------------------------------
        # Test 11
        # ----------------------------------------------------

        context = (
            brain.build_memory_context(
                user_input="memory test"
            )
        )

        if (
            isinstance(
                context,
                dict
            )
            and context.get(
                "available"
            ) is True
            and context.get(
                "count",
                0
            ) >= 1
        ):

            print(
                "[11] Memory Context Build : PASS"
            )

        else:

            print(
                "[11] Memory Context Build : FAIL"
            )

            print(
                "     Context:",
                context
            )

            return False

        # ----------------------------------------------------
        # Test 12
        # ----------------------------------------------------

        context_text = (
            brain.get_memory_context_text(
                user_input="memory test"
            )
        )

        if (
            isinstance(
                context_text,
                str
            )
            and test_key in context_text
        ):

            print(
                "[12] Memory Context Format : PASS"
            )

        else:

            print(
                "[12] Memory Context Format : FAIL"
            )

            print(
                "     Context:",
                context_text
            )

            return False

        # ----------------------------------------------------
        # Test 13
        # ----------------------------------------------------

        before = len(
            brain.get_conversation_history()
        )

        response = brain.process(
            "hello"
        )

        after = len(
            brain.get_conversation_history()
        )

        if (
            after >= before + 2
            and isinstance(
                response,
                str
            )
        ):

            print(
                "[13] Conversation Persistence : PASS"
            )

        else:

            print(
                "[13] Conversation Persistence : FAIL"
            )

            print(
                f"     Before: {before}"
            )

            print(
                f"     After : {after}"
            )

            print(
                f"     Response: {response}"
            )

            return False

        # ----------------------------------------------------
        # Test 14 — Brain Health
        # ----------------------------------------------------

        health = brain.health()

        if (
            health.get("brain") is True
            and health.get("database") is True
            and health.get("memory") is True
            and health.get("memory_context") is True
            and health.get("understanding") is True
            and health.get("global_pipeline") is True
        ):

            print(
                "[14] Brain Health : PASS"
            )

        else:

            print(
                "[14] Brain Health : FAIL"
            )

            print(
                "     Health:",
                health
            )

            return False

        # ----------------------------------------------------
        # Test 15
        # ----------------------------------------------------

        if brain.forget(
            test_key
        ):

            print(
                "[15] Memory Cleanup : PASS"
            )

        else:

            print(
                "[15] Memory Cleanup : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 16
        # ----------------------------------------------------

        if (
            brain.recall(
                test_key
            )
            is None
        ):

            print(
                "[16] Memory Cleanup Verify : PASS"
            )

        else:

            print(
                "[16] Memory Cleanup Verify : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 17 — AI Manager
        # ----------------------------------------------------

        if brain.ai_manager is not None:

            print(
                "[17] AI Manager : PASS"
            )

        else:

            print(
                "[17] AI Manager : FAIL"
            )

            return False

        # ----------------------------------------------------
        # Test 18 — AI Provider
        # ----------------------------------------------------

        ai_status = brain.ai_status()

        print(
            "[18] AI Providers : "
            f"{ai_status.get('providers', [])}"
        )

        # ----------------------------------------------------
        # Final
        # ----------------------------------------------------

        print(
            "=" * 60
        )

        print(
            "       MYX BRAIN + AI INTEGRATION : PASS"
        )

        print(
            "=" * 60
        )

        return True

    except Exception as e:

        print()

        print(
            "=" * 60
        )

        print(
            "[BRAIN TEST] FAIL"
        )

        print(
            "=" * 60
        )

        print(
            "Error:",
            e
        )

        traceback.print_exc()

        return False

    finally:

        if brain is not None:

            brain.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    success = run_brain_test()

    raise SystemExit(
        0 if success else 1
    )
