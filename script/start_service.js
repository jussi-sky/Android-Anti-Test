function createSerialiZable(){
    var mySerialiZable = Java.registerClass({
        name: 'com.example.mySerialiZable',
        implements: [Java.use("java.io.Serializable")],
        methods: {
        }
      })
    var result = mySerialiZable.$new()
    // console.log(result)
    return result
}

function getAppcontext(){
    const ActivityThread = Java.use("android.app.ActivityThread");
    const currentApplication = ActivityThread.currentApplication();
    return currentApplication.getApplicationContext();
}

function startService(){
    Java.perform(function(){
        const context = getAppcontext()
        const intenthandle = Java.use("android.content.Intent").$new()
        var service_from_recv;
        recv(function (received_json_object) {
            service_from_recv = received_json_object.service;
            console.log("service_from_recv: " + service_from_recv);
        }).wait(); //收到数据之后，再执行下去
        service_from_recv = Java.use("java.lang.String").$new(service_from_recv);
        intenthandle.setClassName(context, service_from_recv)
        intenthandle.putExtra("flag", "Jussi")
        intenthandle.putExtra("xp_text", createSerialiZable())
        context.startService(intenthandle)
    })
}

setTimeout(startService, 100)
