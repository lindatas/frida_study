import frida
import sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)
 
jscode = """
function getIMEI(){
    var count = 0;
    var TelephonyManager = Java.use("android.telephony.TelephonyManager");
    /*var Imei = TelephonyManager.$new().getImei();
    console.log('IMEI =', TelephonyManager.$new().getImei());
    console.log('PHONE =', TelephonyManager.$new().getLine1Number());*/
    TelephonyManager['getImei'].overload().implementation = function() {
                console.log("[+] Appcelerator getImei() called. Not throwing an exception.");
                count ++;
                console.log('count: ',count);
                return Imei + "abc";
    }
    TelephonyManager['getDeviceId'].overload().implementation = function() {
                console.log("[+] Appcelerator getDeviceId() called. Not throwing an exception.");
                count ++;
                console.log('count: ',count);
                return Imei + "abc";
    }
    TelephonyManager['getLine1Number'].overload().implementation = function() {
                console.log("[+] Appcelerator getLine1Number() called. Not throwing an exception.");
                return this.getLine1Number()+"cv";
    }
    
  /*  console.log('IMEI2 =', Java.use("android.telephony.TelephonyManager").$new().getImei());
    console.log('PHONE2 =', Java.use("android.telephony.TelephonyManager").$new().getLine1Number());
    */
}
Java.perform(getIMEI)
"""

#问题，code1中，不使用overload()会出错，相反code2中，使用overload()会出错
#此代码可用
jscode2 = """
function hook(){
    var ActivityCompat = Java.use("android.support.v4.app.ActivityCompat");
    ActivityCompat['requestPermissions'].implementation = function(activity, permissions, requestCode) {
        console.log('call requestPermissions');
        console.log(activity);
        console.log(permissions);
        console.log(requestCode);
        return this.requestPermissions(activity, permissions, requestCode);
    }

    ActivityCompat['checkSelfPermission'].implementation = function(context, permission) {
        console.log('call checkSelfPermission');
        console.log(context);
        console.log(permission);
        return this.checkSelfPermission(context, permission);
    }
}

Java.perform(hook)
"""

process = frida.get_usb_device().attach('com.baidu.wenku')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running script')
script.load()
sys.stdin.read()