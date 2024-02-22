package android.hardware;

import android.os.Binder;
import android.os.IBinder;
import android.os.IInterface;
import android.os.Parcel;
import android.os.RemoteException;

/* loaded from: classes.dex */
public interface IAONHECallbacks extends IInterface {
    public static final String DESCRIPTOR = "android.hardware.IAONHECallbacks";
    public static final int ERROR_AON_DISABLED = 2;
    public static final int ERROR_AON_FORCE_CLOSE = 3;
    public static final int ERROR_AON_IN_CLOSED = 0;
    public static final int ERROR_AON_IN_USE = 1;
    public static final int ERROR_AON_NO_INDEX = -1;

    void onClosed() throws RemoteException;

    void onError(int i) throws RemoteException;

    void onHEDetected() throws RemoteException;

    void onOpened() throws RemoteException;

    /* loaded from: classes.dex */
    public static class Default implements IAONHECallbacks {
        @Override // android.hardware.IAONHECallbacks
        public void onOpened() throws RemoteException {
        }

        @Override // android.hardware.IAONHECallbacks
        public void onClosed() throws RemoteException {
        }

        @Override // android.hardware.IAONHECallbacks
        public void onError(int errorCode) throws RemoteException {
        }

        @Override // android.hardware.IAONHECallbacks
        public void onHEDetected() throws RemoteException {
        }

        @Override // android.os.IInterface
        public IBinder asBinder() {
            return null;
        }
    }

    /* loaded from: classes.dex */
    public static abstract class Stub extends Binder implements IAONHECallbacks {
        static final int TRANSACTION_onClosed = 2;
        static final int TRANSACTION_onError = 3;
        static final int TRANSACTION_onHEDetected = 4;
        static final int TRANSACTION_onOpened = 1;

        public Stub() {
            attachInterface(this, IAONHECallbacks.DESCRIPTOR);
        }

        public static IAONHECallbacks asInterface(IBinder obj) {
            if (obj == null) {
                return null;
            }
            IInterface iin = obj.queryLocalInterface(IAONHECallbacks.DESCRIPTOR);
            if (iin != null && (iin instanceof IAONHECallbacks)) {
                return (IAONHECallbacks) iin;
            }
            return new Proxy(obj);
        }

        @Override // android.os.IInterface
        public IBinder asBinder() {
            return this;
        }

        public static String getDefaultTransactionName(int transactionCode) {
            switch (transactionCode) {
                case 1:
                    return "onOpened";
                case 2:
                    return "onClosed";
                case 3:
                    return "onError";
                case 4:
                    return "onHEDetected";
                default:
                    return null;
            }
        }

        public String getTransactionName(int transactionCode) {
            return getDefaultTransactionName(transactionCode);
        }

        @Override // android.os.Binder
        public boolean onTransact(int code, Parcel data, Parcel reply, int flags) throws RemoteException {
            if (code >= 1 && code <= 16777215) {
                data.enforceInterface(IAONHECallbacks.DESCRIPTOR);
            }
            switch (code) {
                case 1598968902:
                    reply.writeString(IAONHECallbacks.DESCRIPTOR);
                    return true;
                default:
                    switch (code) {
                        case 1:
                            onOpened();
                            break;
                        case 2:
                            onClosed();
                            break;
                        case 3:
                            int _arg0 = data.readInt();
                            data.enforceNoDataAvail();
                            onError(_arg0);
                            break;
                        case 4:
                            onHEDetected();
                            break;
                        default:
                            return super.onTransact(code, data, reply, flags);
                    }
                    return true;
            }
        }

        /* loaded from: classes.dex */
        private static class Proxy implements IAONHECallbacks {
            private IBinder mRemote;

            Proxy(IBinder remote) {
                this.mRemote = remote;
            }

            @Override // android.os.IInterface
            public IBinder asBinder() {
                return this.mRemote;
            }

            public String getInterfaceDescriptor() {
                return IAONHECallbacks.DESCRIPTOR;
            }

            @Override // android.hardware.IAONHECallbacks
            public void onOpened() throws RemoteException {
                Parcel _data = Parcel.obtain(asBinder());
                try {
                    _data.writeInterfaceToken(IAONHECallbacks.DESCRIPTOR);
                    this.mRemote.transact(1, _data, null, 1);
                } finally {
                    _data.recycle();
                }
            }

            @Override // android.hardware.IAONHECallbacks
            public void onClosed() throws RemoteException {
                Parcel _data = Parcel.obtain(asBinder());
                try {
                    _data.writeInterfaceToken(IAONHECallbacks.DESCRIPTOR);
                    this.mRemote.transact(2, _data, null, 1);
                } finally {
                    _data.recycle();
                }
            }

            @Override // android.hardware.IAONHECallbacks
            public void onError(int errorCode) throws RemoteException {
                Parcel _data = Parcel.obtain(asBinder());
                try {
                    _data.writeInterfaceToken(IAONHECallbacks.DESCRIPTOR);
                    _data.writeInt(errorCode);
                    this.mRemote.transact(3, _data, null, 1);
                } finally {
                    _data.recycle();
                }
            }

            @Override // android.hardware.IAONHECallbacks
            public void onHEDetected() throws RemoteException {
                Parcel _data = Parcel.obtain(asBinder());
                try {
                    _data.writeInterfaceToken(IAONHECallbacks.DESCRIPTOR);
                    this.mRemote.transact(4, _data, null, 1);
                } finally {
                    _data.recycle();
                }
            }
        }

        public int getMaxTransactionId() {
            return 3;
        }
    }
}
