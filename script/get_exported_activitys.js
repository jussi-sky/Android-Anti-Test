function getAppcontext(){
    const ActivityThread = Java.use("android.app.ActivityThread");
    const currentApplication = ActivityThread.currentApplication();
    return currentApplication.getApplicationContext();
}

function getActivityInfos(){
    const context = getAppcontext()
    const PackageManagerhandle = Java.use("android.content.pm.PackageManager")
    var GET_ACTIVITIES = PackageManagerhandle.GET_ACTIVITIES.value
    var packageInfo = context.getPackageManager().getPackageInfo(context.getPackageName(), GET_ACTIVITIES)
    return packageInfo.activities
}

function getExportedActivitys(){
    Java.perform(function() {
        const activityInfos = getActivityInfos()
        let activitys = []
        try{
            activityInfos.value.map(info => {
                if (info.exported.value) {
                    activitys.push(info.name.value)
                }
            })
        }catch (e) {

        }
        send(activitys)
    });
}

setTimeout(getExportedActivitys, 100)