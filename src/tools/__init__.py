def __init__(
    self,
    search=None,
    planner=None,
    safety=None,
    selection=None,
    executor=None,
    audit=None,
    tool_router=None,
):

    self.search = (
        search
        if search is not None
        else GlobalSearchIntelligence(
            RealGlobalSearch()
        )
    )

    # Real resolver is intentionally outside actions/.
    self.planner = (
        planner
        if planner is not None
        else _safe_construct(
            "src.system.real_global_action_resolver",
            ("RealGlobalActionResolver",),
        )
    )

    self.safety = (
        safety
        if safety is not None
        else _safe_construct(
            "src.system.actions.global_action_safety_manager",
            ("GlobalActionSafetyManager",),
        )
    )

    self.selection = (
        selection
        if selection is not None
        else _safe_construct(
            "src.system.actions.global_selection_manager",
            ("GlobalSelectionManager",),
        )
    )

    self.executor = (
        executor
        if executor is not None
        else _safe_construct(
            "src.system.actions.global_action_executor",
            ("GlobalActionExecutor",),
        )
    )

    self.audit = (
        audit
        if audit is not None
        else _safe_construct(
            "src.system.actions.global_action_audit",
            ("GlobalActionAudit",),
        )
    )

    # ----------------------------------------------------
    # Local Tool Router
    # ----------------------------------------------------

    self.tool_router = (
        tool_router
        if tool_router is not None
        else ToolRouter()
    )

    print("[GlobalActionPipeline] Initialized")