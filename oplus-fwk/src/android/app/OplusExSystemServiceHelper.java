package android.app;

import android.content.ComponentName;
import android.content.Intent;
import android.os.Handler;
import android.text.TextUtils;
import android.util.Log;
//import com.oplus.multiapp.BaseOplusMultiAppManager;

/* loaded from: classes.dex */
public class OplusExSystemServiceHelper {
    private static final String ATHENA_SYSTEM_SERVICE_CLASSNAME = "com.oplus.athena.systemservice.OplusAthenaSystemService";
    public static final String COREAPPFEATURE_SYSTEM_SERVICE_CLASSNAME = "com.oplus.customize.coreapp.service.OplusCoreAppFeatureService";
    public static final String EX_SYSTEM_SERVICE_CLASSNAME = "com.oplus.exsystemservice.OplusSharedSystemService";
    public static final String EX_SYSTEM_SERVICE_PKGNAME = "com.oplus.exsystemservice";
    private static final String TAG = OplusExSystemServiceHelper.class.getSimpleName();
    private static volatile OplusExSystemServiceHelper sIntance;

    public static OplusExSystemServiceHelper getInstance() {
        if (sIntance == null) {
            synchronized (OplusExSystemServiceHelper.class) {
                if (sIntance == null) {
                    sIntance = new OplusExSystemServiceHelper();
                }
            }
        }
        return sIntance;
    }

    public boolean checkOplusExSystemService(boolean systemThread, String className) {
        if (TextUtils.isEmpty(className)) {
            Log.w(TAG, "checkOplusExSystemService className is null or empty str");
            return false;
        } else if (!systemThread) {
            return false;
        } else {
            try {
                if (!EX_SYSTEM_SERVICE_CLASSNAME.equals(className) && !COREAPPFEATURE_SYSTEM_SERVICE_CLASSNAME.equals(className)) {
                    if (!ATHENA_SYSTEM_SERVICE_CLASSNAME.equals(className)) {
                        return false;
                    }
                }
                return true;
            } catch (Exception e) {
                Log.e(TAG, "checkOplusExSystemService e = " + e);
                return false;
            }
        }
    }

    public boolean checkOplusExSystemService(boolean systemThread, Intent intent) {
        if (intent == null) {
            Log.w(TAG, "checkOplusExSystemService intent is null");
            return false;
        } else if (intent.getComponent() == null) {
            Log.w(TAG, "checkOplusExSystemService intent getComponent is null");
            return false;
        } else {
            return checkOplusExSystemService(systemThread, intent.getComponent().getClassName());
        }
    }

    public boolean checkOplusExSystemService(Handler handler, String className) {
        return checkOplusExSystemService(true, className);
    }

    public ComponentName getComponentName() {
        return new ComponentName(EX_SYSTEM_SERVICE_PKGNAME, EX_SYSTEM_SERVICE_CLASSNAME);
    }
    /*
    public void ensureMediaProviderPriority(Handler activityThread, ComponentName name, Runnable runConnection) {
        if (name.getClassName().contains(BaseOplusMultiAppManager.MEDIA_PROVIDER_PACKAGE_NAME)) {
            Log.i(TAG, "connected :" + name.getClassName());
        }
        if (checkOplusExSystemService(activityThread, name.getClassName())) {
            runConnection.run();
        } else if (name.getClassName().contains(BaseOplusMultiAppManager.MEDIA_PROVIDER_PACKAGE_NAME)) {
            activityThread.postAtFrontOfQueue(runConnection);
        } else {
            activityThread.post(runConnection);
        }
    }
    */
}
