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

function startReceiver(){
    Java.perform(function(){
        const context = getAppcontext()
        const intenthandle = Java.use("android.content.Intent").$new()
        var receiver_from_recv;
        recv(function (received_json_object) {
            receiver_from_recv = receiver_from_recv.receiver;
            console.log("receiver_from_recv: " + receiver_from_recv);
        }).wait(); //收到数据之后，再执行下去
        intenthandle.setClassName(context, receiver_from_recv)
        intenthandle.putExtra("flag", "Jussi")
        intenthandle.putExtra("xp_text", createSerialiZable())
        intenthandle.setAction("android")
        context.sendBroadcast(intenthandle)
    })
}