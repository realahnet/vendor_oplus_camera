package com.oplus.wrapper.os;

import android.os.IBinder;

public class ServiceManager {
  public static void addService(String paramString, IBinder paramIBinder) {
    android.os.ServiceManager.addService(paramString, paramIBinder);
  }
  
  public static IBinder checkService(String paramString) {
    return android.os.ServiceManager.checkService(paramString);
  }
  
  public static IBinder getService(String paramString) {
    return android.os.ServiceManager.getService(paramString);
  }
}
