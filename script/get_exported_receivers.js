function getAppcontext(){
    const ActivityThread = Java.use("android.app.ActivityThread");
    const currentApplication = ActivityThread.currentApplication();
    return currentApplication.getApplicationContext();
}

function getExportedReceivers(){
    Java.perform(function() {
        const context = getAppcontext()
        const PackageManagerhandle = Java.use("android.content.pm.PackageManager")
        var GET_RECEIVERS = PackageManagerhandle.GET_RECEIVERS.value
        var packageInfo = context.getPackageManager().getPackageInfo(context.getPackageName(), GET_RECEIVERS)
        const receiversInfos = packageInfo.receivers
        let receivers = []
        try {
            receiversInfos.value.map(info => {
                if (info.exported.value) {
                    receivers.push(info.name.value)
                }
            })
        } catch (e) {

        }
        send(receivers)
    });
}

setTimeout(getExportedReceivers, 100)