import os
import sys
import importlib
import traceback


# ============================================================
# MYX PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# MODULES TO VERIFY
# ============================================================

MODULES = [
    "src.system.discovery.app_discovery",
    "src.system.discovery.start_menu_discovery",
    "src.system.discovery.start_apps_discovery",
    "src.system.discovery.application_record",
    "src.system.discovery.application_registry",
    "src.system.discovery.application_resolver",

    "src.system.storage.file_discovery",
    "src.system.storage.folder_discovery",
    "src.system.storage.storage_discovery",
    "src.system.storage.file_index",
    "src.system.storage.indexing_pipeline",
    "src.system.storage.user_storage_indexer",
    "src.system.storage.storage_index_manager",
    "src.system.storage.file_search",
    "src.system.storage.file_search_intelligence",
    "src.system.storage.file_action_resolver",
    "src.system.storage.file_action_executor",
    "src.system.storage.file_open_executor",
    "src.system.storage.file_selection_manager",
    "src.system.storage.file_response_formatter",

    "src.system.discovery.file_discovery_provider",
    "src.system.discovery.storage_discovery_provider",

    # NOTE:
    # discovery_provider_manager is currently still located
    # directly under src/system.
    "src.system.discovery_provider_manager",

    "src.system.file_operation_controller",
]


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print("=" * 60)
    print("        MYX CONSOLIDATED DISCOVERY INTEGRATION")
    print("=" * 60)

    passed = 0
    failed = []

    # --------------------------------------------------------
    # 1. MODULE IMPORTS
    # --------------------------------------------------------

    print("\n[1] MODULE IMPORTS")

    for module in MODULES:

        try:
            importlib.import_module(module)

            print("[PASS]", module)
            passed += 1

        except Exception as e:

            print("[FAIL]", module, "->", e)
            failed.append(module)

    # --------------------------------------------------------
    # 2. DISCOVERY PROVIDER MANAGER
    # --------------------------------------------------------

    print("\n[2] DISCOVERY PROVIDER MANAGER")

    try:

        from src.system.discovery_provider_manager import (
            DiscoveryProviderManager
        )

        manager = DiscoveryProviderManager()

        print("[PASS] Manager initialization")
        passed += 1

        records = manager.discover_all()

        print(
            "[PASS] Real discovery:",
            len(records),
            "records"
        )
        passed += 1

        print(
            "[PASS] Providers:",
            list(manager.providers.keys())
        )
        passed += 1

        chrome_results = manager.search("Chrome")

        print(
            "[PASS] Chrome search:",
            len(chrome_results),
            "results"
        )
        passed += 1

    except Exception as e:

        print("[FAIL] Discovery chain:", e)
        traceback.print_exc()

        failed.append("discovery_provider_manager")

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print("PASSED :", passed)
    print("FAILED :", len(failed))

    if failed:

        print("FAILURES:")

        for item in failed:
            print(" -", item)

        print("RESULT : FAIL")

    else:

        print("RESULT : PASS")

    print("=" * 60)

    return 0 if not failed else 1


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    raise SystemExit(main())
