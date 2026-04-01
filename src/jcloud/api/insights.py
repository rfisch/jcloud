from __future__ import annotations

from jcloud.client import JumpCloudClient

INSIGHT_TABLES = [
    "apps",
    "authorized_keys",
    "battery",
    "browser_plugins",
    "certificates",
    "chrome_extensions",
    "connectivity",
    "crashes",
    "disk_encryption",
    "disk_info",
    "dns_resolvers",
    "etc_hosts",
    "firefox_addons",
    "groups",
    "interface_addresses",
    "interface_details",
    "kernel_info",
    "launchd",
    "logged_in_users",
    "logical_drives",
    "managed_policies",
    "mounts",
    "os_version",
    "patches",
    "programs",
    "python_packages",
    "safari_extensions",
    "scheduled_tasks",
    "services",
    "shared_folders",
    "shared_resources",
    "startup_items",
    "system_controls",
    "system_info",
    "uptime",
    "usb_devices",
    "user_groups",
    "user_ssh_keys",
    "users",
    "wifi_networks",
    "wifi_status",
    # Windows-specific
    "bitlocker_info",
    "ie_extensions",
    "windows_crashes",
    "windows_security_center",
    "windows_security_products",
]


def query_table(client: JumpCloudClient, table: str) -> list[dict]:
    """Query a System Insights table across all systems."""
    return client.paginate_v2(f"/systeminsights/{table}")


def query_table_for_system(client: JumpCloudClient, system_id: str, table: str) -> list[dict]:
    """Query a System Insights table for a specific system."""
    return client.paginate_v2(f"/systeminsights/{system_id}/{table}")
