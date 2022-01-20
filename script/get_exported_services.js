function getAppcontext(){
    const ActivityThread = Java.use("android.app.ActivityThread");
    const currentApplication = ActivityThread.currentApplication();
    return currentApplication.getApplicationContext();
}

function getExportedServices(){
    Java.perform(function() {
        const context = getAppcontext()
        const PackageManagerhandle = Java.use("android.content.pm.PackageManager")
        var GET_SERVICES = PackageManagerhandle.GET_SERVICES.value
        var packageInfo = context.getPackageManager().getPackageInfo(context.getPackageName(), GET_SERVICES)
        const servicesInfos = packageInfo.services
        let services = []
        try {
            servicesInfos.value.map(info => {
                if (info.exported.value) {
                    services.push(info.name.value)
                }
            })
        } catch (e) {

        }
        send(services)
    });
}

setTimeout(getExportedServices, 100)
