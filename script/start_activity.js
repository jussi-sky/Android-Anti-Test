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

function startActivity(){
    Java.perform(function(){
        const context = getAppcontext()
        const intenthandle = Java.use("android.content.Intent").$new();
        var activity_from_recv;
        recv(function (received_json_object) {
            activity_from_recv = received_json_object.activity;
            console.log("activity_from_recv: " + activity_from_recv);
        }).wait(); //收到数据之后，再执行下去
        activity_from_recv = Java.use("java.lang.String").$new(activity_from_recv);
        intenthandle.setClassName(context, activity_from_recv)
        intenthandle.addFlags(0x10000000)
        intenthandle.putExtra("xp_text", createSerialiZable())
        // intenthandle.putExtra("test", "text")
        context.startActivity(intenthandle)
    })
}

setTimeout(startActivity, 100)
