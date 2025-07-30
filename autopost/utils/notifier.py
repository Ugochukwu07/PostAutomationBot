"""
Notification utilities for the Automated Daily Poster Bot.

This module handles system notifications and alerts for bot events.
"""

import logging
import subprocess
import platform
from typing import Optional, Dict, Any

try:
    from plyer import notification

    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False


def send_notification(title: str, message: str, timeout: int = 10) -> bool:
    """
    Send a system notification

    Args:
        title: Notification title
        message: Notification message
        timeout: Timeout in seconds

    Returns:
        bool: True if notification was sent successfully
    """
    logger = logging.getLogger(__name__)

    try:
        # Try plyer first (cross-platform)
        if PLYER_AVAILABLE:
            return _send_plyer_notification(title, message, timeout)

        # Fallback to platform-specific methods
        system = platform.system().lower()

        if system == "linux":
            return _send_linux_notification(title, message, timeout)
        elif system == "darwin":  # macOS
            return _send_macos_notification(title, message, timeout)
        elif system == "windows":
            return _send_windows_notification(title, message, timeout)
        else:
            logger.warning(f"Unsupported platform for notifications: {system}")
            return False

    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        return False


def _send_plyer_notification(title: str, message: str, timeout: int) -> bool:
    """Send notification using plyer library"""
    try:
        notification.notify(title=title, message=message, timeout=timeout)
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Plyer notification failed: {e}")
        return False


def _send_linux_notification(title: str, message: str, timeout: int) -> bool:
    """Send notification on Linux using notify-send"""
    try:
        subprocess.run(
            [
                "notify-send",
                "-t",
                str(timeout * 1000),  # Convert to milliseconds
                title,
                message,
            ],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.getLogger(__name__).warning(f"Linux notification failed: {e}")
        return False


def _send_macos_notification(title: str, message: str, timeout: int) -> bool:
    """Send notification on macOS using osascript"""
    try:
        script = f"""
        display notification "{message}" with title "{title}"
        """
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.getLogger(__name__).warning(f"macOS notification failed: {e}")
        return False


def _send_windows_notification(title: str, message: str, timeout: int) -> bool:
    """Send notification on Windows using PowerShell"""
    try:
        script = f"""
        Add-Type -AssemblyName System.Windows.Forms
        $notification = New-Object System.Windows.Forms.NotifyIcon
        $notification.Icon = [System.Drawing.SystemIcons]::Information
        $notification.BalloonTipTitle = "{title}"
        $notification.BalloonTipText = "{message}"
        $notification.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
        $notification.Visible = $true
        $notification.ShowBalloonTip({timeout * 1000})
        Start-Sleep -Seconds {timeout + 1}
        $notification.Dispose()
        """
        subprocess.run(
            ["powershell", "-Command", script], check=True, capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.getLogger(__name__).warning(f"Windows notification failed: {e}")
        return False


def send_bot_status_notification(status: Dict[str, Any]) -> bool:
    """
    Send a notification with bot status information

    Args:
        status: Bot status dictionary

    Returns:
        bool: True if notification was sent successfully
    """
    title = "🤖 AutoPost Bot Status"

    # Create status message
    lines = []
    lines.append(f"Running: {'✅ Yes' if status.get('is_running') else '❌ No'}")
    lines.append(f"Posts Today: {status.get('posts_today', 0)}")
    lines.append(f"Random Posts: {status.get('random_posts_today', 0)}")
    lines.append(f"Scheduled Posts: {status.get('scheduled_posts_today', 0)}")

    last_post = status.get("last_post_time")
    if last_post:
        lines.append(f"Last Post: {last_post}")

    message = "\n".join(lines)

    return send_notification(title, message)


def send_post_notification(
    post_type: str, success: bool, content_preview: str = None
) -> bool:
    """
    Send a notification about a post attempt

    Args:
        post_type: Type of post (RANDOM, SCHEDULED, etc.)
        success: Whether the post was successful
        content_preview: Preview of the posted content

    Returns:
        bool: True if notification was sent successfully
    """
    if success:
        title = f"✅ {post_type} Post Successful"
        message = f"Successfully posted {post_type.lower()} content"
    else:
        title = f"❌ {post_type} Post Failed"
        message = f"Failed to post {post_type.lower()} content"

    if content_preview:
        # Truncate content preview if too long
        if len(content_preview) > 100:
            content_preview = content_preview[:97] + "..."
        message += f"\n\nContent: {content_preview}"

    return send_notification(title, message)


def send_error_notification(error_message: str, context: str = "Bot Error") -> bool:
    """
    Send a notification about an error

    Args:
        error_message: Error message
        context: Context where the error occurred

    Returns:
        bool: True if notification was sent successfully
    """
    title = f"⚠️ {context}"

    # Truncate error message if too long
    if len(error_message) > 200:
        error_message = error_message[:197] + "..."

    message = f"An error occurred:\n{error_message}"

    return send_notification(title, message, timeout=15)


def is_notification_supported() -> bool:
    """
    Check if notifications are supported on the current platform

    Returns:
        bool: True if notifications are supported
    """
    if PLYER_AVAILABLE:
        return True

    system = platform.system().lower()

    if system == "linux":
        try:
            subprocess.run(
                ["notify-send", "--version"], check=True, capture_output=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    elif system == "darwin":  # macOS
        try:
            subprocess.run(
                ["osascript", "-e", "return"], check=True, capture_output=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    elif system == "windows":
        try:
            subprocess.run(
                ["powershell", "-Command", "return"], check=True, capture_output=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    return False
