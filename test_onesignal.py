#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flet as ft
import flet_onesignal as fos
import time
import threading

# ✅ Replace with your actual OneSignal App ID
ONESIGNAL_APP_ID = "6bb7df1b-6014-498a-ac2e-67abb63e4751"

def main(page: ft.Page):
    page.title = "OneSignal Registration Test"
    page.padding = 20
    page.scroll = "auto"
    
    # ============================================
    # UI COMPONENTS
    # ============================================
    platform_text = ft.Text(
        f"📱 Platform: {page.platform}", 
        size=16, 
        weight="bold",
        color="blue"
    )
    
    status_text = ft.Text(
        "Status: Ready to test", 
        size=14,
        color="grey"
    )
    
    player_id_text = ft.TextField(
        label="OneSignal Player ID (Subscription ID)",
        read_only=True,
        multiline=True,
        min_lines=3,
        max_lines=5,
        border_color="blue"
    )
    
    external_id_text = ft.TextField(
        label="External User ID",
        read_only=True,
        border_color="green"
    )
    
    log_text = ft.TextField(
        label="Debug Log",
        multiline=True,
        min_lines=8,
        max_lines=15,
        read_only=True,
        value="",
        border_color="orange"
    )
    
    # Store OneSignal control reference
    onesignal_ref = {"control": None}
    
    # ============================================
    # HELPER FUNCTIONS
    # ============================================
    def add_log(message):
        """Add message to debug log"""
        timestamp = time.strftime("%H:%M:%S")
        current = log_text.value
        log_text.value = f"{current}\n[{timestamp}] {message}"
        print(f"[TEST-APP] {message}")
        page.update()
    
    # ============================================
    # STEP 1: INITIALIZE ONESIGNAL
    # ============================================
    def init_onesignal(e=None):
        try:
            add_log("=" * 50)
            add_log("STEP 1: Initializing OneSignal...")
            add_log(f"App ID: {ONESIGNAL_APP_ID[:8]}...")
            add_log(f"Platform: {page.platform}")
            
            status_text.value = "⏳ Creating OneSignal control..."
            status_text.color = "orange"
            page.update()
            
            # Create OneSignal control
            onesignal = fos.OneSignal(
                settings=fos.OneSignalSettings(app_id=ONESIGNAL_APP_ID),
                on_notification_opened=lambda e: add_log(f"Notification opened: {e.notification_opened}"),
                on_notification_received=lambda e: add_log(f"Notification received: {e.notification_received}"),
            )
            
            add_log("✅ OneSignal control created")
            
            # Add to page overlay (required!)
            page.overlay.append(onesignal)
            onesignal_ref["control"] = onesignal
            
            add_log("✅ OneSignal added to page.overlay")
            add_log("✅ Initialization complete!")
            
            status_text.value = "✅ OneSignal initialized successfully!"
            status_text.color = "green"
            page.update()
            
            add_log("")
            add_log("Next: Wait 5-10 seconds, then click 'Get Player ID'")
            
        except Exception as ex:
            add_log(f"❌ ERROR: {ex}")
            import traceback
            add_log(traceback.format_exc())
            
            status_text.value = f"❌ Error: {ex}"
            status_text.color = "red"
            page.update()
    
    # ============================================
    # STEP 2: GET PLAYER ID
    # ============================================
    def get_player_id(e):
        try:
            add_log("=" * 50)
            add_log("STEP 2: Getting Player ID...")
            
            if not onesignal_ref["control"]:
                add_log("❌ OneSignal not initialized! Click 'Initialize' first.")
                player_id_text.value = "Not initialized"
                return
            
            status_text.value = "⏳ Fetching Player ID..."
            status_text.color = "orange"
            page.update()
            
            # Try to get Player ID
            player_id = onesignal_ref["control"].get_onesignal_id()
            
            add_log(f"get_onesignal_id() returned: {player_id}")
            
            if player_id:
                add_log("✅ SUCCESS! Device is registered with OneSignal!")
                add_log(f"Player ID: {player_id}")
                
                player_id_text.value = player_id
                status_text.value = "✅ Device registered!"
                status_text.color = "green"
                
                add_log("")
                add_log("Next: Check OneSignal Dashboard → Audience → All Users")
                add_log("You should see 1 user there!")
                
            else:
                add_log("⚠️ Player ID is None")
                add_log("This means device hasn't registered with OneSignal yet.")
                add_log("Possible reasons:")
                add_log("  1. Not enough time passed (need 5-10 seconds)")
                add_log("  2. No internet connection")
                add_log("  3. OneSignal App ID is incorrect")
                add_log("  4. Firebase FCM not configured in OneSignal")
                
                player_id_text.value = "⚠️ Not registered yet (Player ID is None)"
                status_text.value = "⏳ Not ready - wait 5 more seconds and retry"
                status_text.color = "orange"
                
                add_log("")
                add_log("Action: Wait 5 more seconds, then click 'Get Player ID' again")
            
            page.update()
            
        except Exception as ex:
            add_log(f"❌ ERROR: {ex}")
            import traceback
            add_log(traceback.format_exc())
            
            player_id_text.value = f"Error: {ex}"
            status_text.value = "❌ Error occurred"
            status_text.color = "red"
            page.update()
    
    # ============================================
    # STEP 3: LOGIN WITH EXTERNAL USER ID
    # ============================================
    def login_test(e):
        try:
            add_log("=" * 50)
            add_log("STEP 3: Logging in with External User ID...")
            
            if not onesignal_ref["control"]:
                add_log("❌ OneSignal not initialized!")
                return
            
            test_user_id = "test_user_12345"
            add_log(f"Calling login('{test_user_id}')...")
            
            status_text.value = f"⏳ Logging in as {test_user_id}..."
            status_text.color = "orange"
            page.update()
            
            result = onesignal_ref["control"].login(test_user_id)
            
            add_log(f"login() returned: {result}")
            
            if result:
                add_log("✅ Login successful!")
                status_text.value = "✅ Logged in!"
                status_text.color = "green"
            else:
                add_log("⚠️ Login returned False (may still work)")
                status_text.value = "⚠️ Login may have failed"
                status_text.color = "orange"
            
            page.update()
            
            add_log("")
            add_log("Waiting 5 seconds to get Player ID...")
            
            # Auto-fetch Player ID after 5 seconds
            def delayed_get():
                time.sleep(5)
                add_log("Auto-fetching Player ID...")
                get_player_id(None)
            
            threading.Thread(target=delayed_get, daemon=True).start()
            
        except Exception as ex:
            add_log(f"❌ ERROR: {ex}")
            import traceback
            add_log(traceback.format_exc())
            
            status_text.value = f"❌ Login error"
            status_text.color = "red"
            page.update()
    
    # ============================================
    # STEP 4: CHECK EXTERNAL USER ID
    # ============================================
    def check_external_id(e):
        try:
            add_log("=" * 50)
            add_log("STEP 4: Checking External User ID...")
            
            if not onesignal_ref["control"]:
                add_log("❌ OneSignal not initialized!")
                return
            
            external_id = onesignal_ref["control"].get_external_user_id()
            
            add_log(f"get_external_user_id() returned: {external_id}")
            
            if external_id:
                add_log(f"✅ External ID: {external_id}")
                external_id_text.value = external_id
            else:
                add_log("⚠️ No external ID set (not logged in)")
                external_id_text.value = "Not set (not logged in)"
            
            page.update()
            
        except Exception as ex:
            add_log(f"❌ ERROR: {ex}")
            external_id_text.value = f"Error: {ex}"
            page.update()
    
    # ============================================
    # AUTO-INITIALIZE ON APP START
    # ============================================
    def on_app_start(e):
        add_log("=" * 50)
        add_log("🚀 OneSignal Test App Started")
        add_log(f"Platform: {page.platform}")
        add_log(f"App ID: {ONESIGNAL_APP_ID[:8]}...")
        add_log("=" * 50)
        add_log("")
        
        # Auto-initialize OneSignal
        add_log("Auto-initializing OneSignal in 2 seconds...")
        
        def delayed_init():
            time.sleep(2)
            init_onesignal()
        
        threading.Thread(target=delayed_init, daemon=True).start()
    
    page.on_connect = on_app_start
    
    # ============================================
    # BUILD UI
    # ============================================
    page.add(
        ft.Column([
            # Header
            ft.Container(
                content=ft.Column([
                    ft.Text("🔔 OneSignal Test App", size=24, weight="bold", color="white"),
                    ft.Text("Device Registration Tester", size=14, color="white"),
                ], horizontal_alignment="center"),
                bgcolor="blue",
                padding=20,
                border_radius=10
            ),
            
            ft.Container(height=10),
            
            # Platform Info
            platform_text,
            
            ft.Divider(),
            
            # Status
            status_text,
            
            ft.Container(height=10),
            
            # Test Buttons
            ft.Text("📋 Test Steps:", size=16, weight="bold"),
            
            ft.ElevatedButton(
                "1️⃣ Initialize OneSignal",
                on_click=init_onesignal,
                bgcolor="blue",
                color="white",
                width=300,
                height=50
            ),
            
            ft.Text("⏰ Wait 5-10 seconds after initialization", size=12, color="grey", italic=True),
            
            ft.ElevatedButton(
                "2️⃣ Get Player ID",
                on_click=get_player_id,
                bgcolor="green",
                color="white",
                width=300,
                height=50
            ),
            
            ft.ElevatedButton(
                "3️⃣ Login (test_user_12345)",
                on_click=login_test,
                bgcolor="orange",
                color="white",
                width=300,
                height=50
            ),
            
            ft.ElevatedButton(
                "4️⃣ Check External User ID",
                on_click=check_external_id,
                bgcolor="purple",
                color="white",
                width=300,
                height=50
            ),
            
            ft.Container(height=20),
            
            # Results
            ft.Text("📊 Results:", size=16, weight="bold"),
            player_id_text,
            external_id_text,
            
            ft.Container(height=20),
            
            # Debug Log
            ft.Text("🐛 Debug Log:", size=16, weight="bold"),
            log_text,
            
            ft.Container(height=20),
            
            # Instructions
            ft.Container(
                content=ft.Column([
                    ft.Text("📖 Instructions:", weight="bold", size=14),
                    ft.Text("1. App auto-initializes OneSignal on startup", size=12),
                    ft.Text("2. Wait 10 seconds", size=12),
                    ft.Text("3. Click 'Get Player ID'", size=12),
                    ft.Text("4. If Player ID shows, device is registered! ✅", size=12),
                    ft.Text("5. Check OneSignal Dashboard → Audience → All Users", size=12),
                    ft.Text("6. You should see 1 user there", size=12),
                    ft.Text("", size=12),
                    ft.Text("⚠️ If Player ID is None:", weight="bold", size=12),
                    ft.Text("   - Wait 5 more seconds and click 'Get Player ID' again", size=12),
                    ft.Text("   - Check internet connection", size=12),
                    ft.Text("   - Verify OneSignal App ID is correct", size=12),
                ], spacing=5),
                bgcolor="#F0F0F0",
                padding=15,
                border_radius=10
            ),
            
        ], spacing=10, scroll="auto")
    )

if __name__ == "__main__":
    ft.app(target=main)
