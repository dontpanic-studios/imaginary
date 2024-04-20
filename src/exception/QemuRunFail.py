class QemuRunVaildationFail(Exception):
    def __str__(self):
        return "QEMU seems to be run failed, File might not be avaliable or could be problem with settings.\nPlease "