adb root
adb remount
adb push build/outputs/apk/release/SystemUI.apk /system/system_ext/priv-app/SystemUI/SystemUI.apk

adb reboot
#adb shell stop
#adb shell start
